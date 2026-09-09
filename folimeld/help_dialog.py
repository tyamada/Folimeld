from html import escape

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QTabWidget,
                               QTextBrowser, QVBoxLayout)


class HelpDialog(QDialog):
    """Offline usage guide that can remain open while editing a PDF."""

    def __init__(self, tr, actions, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("help_usage"))
        self.resize(720, 560)
        tabs = QTabWidget(self)

        def section(title, body):
            return f"<h2>{escape(tr(title))}</h2><p>{escape(tr(body))}</p>"

        def add_tab(title, html):
            browser = QTextBrowser(tabs)
            browser.setAccessibleName(tr(title))
            browser.setHtml(html)
            tabs.addTab(browser, tr(title))

        add_tab("help_basics", "".join(
            section(title, body) for title, body in (
                ("open", "help_open_text"),
                ("edit", "help_edit_text"),
                ("insert", "help_insert_text"),
                ("save", "help_save_text"),
            )
        ))
        add_tab("settings", "".join(
            section(title, body) for title, body in (
                ("properties", "help_properties_text"),
                ("set_password", "help_password_text"),
                ("settings", "help_settings_text"),
            )
        ))
        rows = []
        for action in actions:
            shortcut = action.shortcut().toString(QKeySequence.SequenceFormat.NativeText)
            if shortcut:
                rows.append(
                    f"<tr><td>{escape(action.text())}</td>"
                    f"<td>{escape(shortcut)}</td></tr>"
                )
        add_tab("help_shortcuts", f'<table cellspacing="10">{"".join(rows)}</table>')
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText(tr("support_close"))
        buttons.rejected.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(buttons)
