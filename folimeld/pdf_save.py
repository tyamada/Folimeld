"""Save an independent PDF in a spawned process while Qt handles events."""
import multiprocessing
import logging
import tempfile
import traceback
from pathlib import Path

import fitz
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QProgressDialog


class SaveProgressDialog(QProgressDialog):
    """The model must finish writing or handle failure before leaving save."""
    def reject(self):
        pass

    def closeEvent(self, event):
        event.ignore()


def save_worker(source, destination, options, connection):
    try:
        with fitz.open(source) as document:
            document.save(destination, **options)
        connection.send(('done', None))
    except Exception as exc:
        connection.send(('error', str(exc), traceback.format_exc()))
    finally:
        connection.close()


def save_with_progress(document, destination, options, parent, label):
    # Only staging is synchronous. The worker owns a separate PDF and writes
    # only to the model's temporary output; the model commits it afterwards.
    with tempfile.TemporaryDirectory(prefix='folimeld-save-') as directory:
        source = Path(directory) / 'source.pdf'
        source.write_bytes(document.tobytes(encryption=fitz.PDF_ENCRYPT_NONE, no_new_id=True))
        context = multiprocessing.get_context('spawn')
        receiver, sender = context.Pipe(duplex=False)
        process = context.Process(target=save_worker,
                                  args=(str(source), str(destination), options, sender))
        progress = SaveProgressDialog(label, '', 0, 0, parent)
        progress.setWindowTitle(label)
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setCancelButton(None)
        progress.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        result = []
        timer = QTimer(progress)

        def poll():
            try:
                if receiver.poll():
                    result.append(receiver.recv())
                    progress.accept()
                    return
            except (EOFError, OSError):
                pass
            if not process.is_alive():
                # The process may have sent its result between the first poll
                # and the liveness check. Drain it before reporting a crash.
                try:
                    message = receiver.recv() if receiver.poll() else None
                except (EOFError, OSError):
                    message = None
                result.append(message or ('error', 'PDF save process stopped.'))
                progress.accept()

        try:
            process.start()
            sender.close()
            timer.timeout.connect(poll)
            timer.start(25)
            progress.exec()
            if not result or result[0][0] != 'done':
                if result and len(result[0]) > 2:
                    logging.getLogger(__name__).error('PDF save worker failed:\n%s', result[0][2])
                raise OSError(result[0][1] if result else 'PDF save interrupted.')
        finally:
            timer.stop()
            if process.pid is not None:
                process.join(timeout=0.2)
                if process.is_alive():
                    process.terminate()
                    process.join()
            receiver.close()
            sender.close()
            progress.deleteLater()
