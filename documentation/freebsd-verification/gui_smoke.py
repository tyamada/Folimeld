from multiprocessing import freeze_support
from pathlib import Path
import json
import sys
import traceback

import fitz
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from folimeld.app import MainWindow
from folimeld.i18n import I18n, install_qt_translator


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName('FolimeldVerification')
    app.setApplicationName('FreeBSDGuiSmoke')
    out = Path('build/freebsd-verification')
    out.mkdir(parents=True, exist_ok=True)
    source = out / 'source.pdf'
    destination = out / '\u65e5\u672c\u8a9e saved.pdf'
    with fitz.open() as document:
        for i in range(4):
            document.new_page().insert_text((72, 72), f'FreeBSD page {i + 1}')
        document.save(source)
    i18n = I18n()
    i18n.load('ja')
    _translator = install_qt_translator(app, 'ja')
    window = MainWindow(i18n)
    window.show()

    def verify():
        try:
            window.open_path(str(source))
            assert window.model.doc.page_count == 4
            window.model.rotate([0], 90)
            window.refresh()
            assert window._save_to(str(destination))
            with fitz.open(destination) as saved:
                assert saved.page_count == 4
                assert saved[0].rotation == 90
                assert saved[0].get_text().strip() == 'FreeBSD page 1'
            window.open_path(str(destination))
            assert window.model.doc[0].rotation == 90
            app.processEvents()
            assert window.grab().save(str(out / 'gui-smoke.png'))
            (out / 'gui-smoke.json').write_text(json.dumps({'passed': True, 'pages': 4, 'rotation': 90, 'saved': str(destination), 'platform': sys.platform}, indent=2), encoding='utf-8')
            print('GUI_SMOKE_PASSED', flush=True)
            window.close()
            app.exit(0)
        except Exception:
            traceback.print_exc()
            app.exit(1)

    QTimer.singleShot(1500, verify)
    return app.exec()


if __name__ == '__main__':
    freeze_support()
    raise SystemExit(main())
