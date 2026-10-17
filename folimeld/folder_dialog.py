"""Folder picker with visible files and Windows OneDrive shortcuts."""
import os
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QFileDialog


def onedrive_directories():
    if sys.platform != 'win32':
        return []
    candidates = [os.environ.get(name) for name in
                  ('OneDrive', 'OneDriveConsumer', 'OneDriveCommercial')]
    # Multiple work/school accounts may not all have environment variables.
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\OneDrive\Accounts') as accounts:
            for index in range(winreg.QueryInfoKey(accounts)[0]):
                try:
                    with winreg.OpenKey(accounts, winreg.EnumKey(accounts, index)) as account:
                        candidates.append(winreg.QueryValueEx(account, 'UserFolder')[0])
                except OSError:
                    continue
    except OSError:
        pass
    result = []
    seen = set()
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        key = os.path.normcase(str(path.resolve()))
        if path.is_dir() and key not in seen:
            result.append(path)
            seen.add(key)
    return result


def select_image_folder(parent, title, initial):
    dialog = QFileDialog(parent, title, initial)
    # Native folder pickers can hide files regardless of ShowDirsOnly.
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setOption(QFileDialog.Option.ShowDirsOnly, False)
    urls = dialog.sidebarUrls()
    for path in onedrive_directories():
        url = QUrl.fromLocalFile(str(path))
        if url not in urls:
            urls.append(url)
    dialog.setSidebarUrls(urls)
    if dialog.exec():
        selected = dialog.selectedFiles()
        if selected and Path(selected[0]).is_dir():
            return selected[0]
    return ''
