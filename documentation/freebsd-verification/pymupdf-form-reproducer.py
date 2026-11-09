"""Reproduce the FreeBSD package crash without importing Folimeld or Qt."""

import fitz


document = fitz.open()
page = document.new_page()
widget = fitz.Widget()
widget.field_name = "name"
widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
widget.field_value = "Preserved field"
widget.rect = fitz.Rect(30, 200, 200, 230)
page.add_widget(widget)
print("Reading a text widget with PyMuPDF", fitz.VersionBind, flush=True)
print(list(page.widgets())[0].field_value, flush=True)
