"""Keep Qt objects out of Python's interpreter-shutdown cleanup."""

import gc

import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def qapp():
    # Retain one application until all GUI tests and their teardown have finished.
    app = QApplication.instance() or QApplication([])
    yield app
    gc.collect()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


@pytest.fixture(autouse=True)
def cleanup_qt_widgets(qapp):
    yield
    # close() only hides most widgets. Delete them while QApplication and the
    # Python callbacks they reference still exist, including file dialog models
    # and their filesystem-watcher threads.
    for widget in qapp.topLevelWidgets():
        widget.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    gc.collect()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
