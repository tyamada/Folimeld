"""Read widgets across a process boundary so native crashes remain test failures."""

import json
import os
import subprocess
import sys

import pytest


FORM_READER = """
import json
import sys

try:
    import resource
except ImportError:
    pass
else:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

import pymupdf as fitz

kind, reopen = sys.argv[1:]
document = fitz.open()
page = document.new_page()
widget = fitz.Widget()
widget.field_name = 'field'
widget.rect = fitz.Rect(30, 30, 160, 60)
if kind == 'text':
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.field_value = 'Preserved field'
elif kind == 'checkbox':
    widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_value = 'Off'
else:
    widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
    widget.field_value = 'Alpha'
    widget.choice_values = ['Alpha', 'Beta']
annotation = page.add_widget(widget)
if kind == 'empty_combo':
    document.xref_set_key(annotation.xref, 'Opt', '[]')
    document.xref_set_key(annotation.xref, 'V', '()')
if reopen == 'yes':
    data = document.tobytes()
    document.close()
    document = fitz.open(stream=data, filetype='pdf')
    page = document[0]
widgets = list(page.widgets())
assert len(widgets) == 1
print(json.dumps({'value': widgets[0].field_value,
                  'choices': widgets[0].choice_values}))
document.close()
"""


@pytest.mark.parametrize('reopen', ['no', 'yes'])
@pytest.mark.parametrize('kind', ['text', 'checkbox', 'combo', 'empty_combo'])
def test_widget_reading_survives_native_boundary(tmp_path, kind, reopen):
    result = subprocess.run(
        [sys.executable, '-c', FORM_READER, kind, reopen],
        cwd=tmp_path,
        env={**os.environ, 'PYTHONFAULTHANDLER': '1'},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f'Widget reader exited with {result.returncode}:\n'
        f'{result.stdout}\n{result.stderr}'
    )
    assert json.loads(result.stdout) == {
        'value': {'text': 'Preserved field', 'checkbox': 'Off',
                  'combo': 'Alpha', 'empty_combo': ''}[kind],
        'choices': ['Alpha', 'Beta'] if kind == 'combo' else None,
    }
