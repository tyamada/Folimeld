"""Exercise saved PDF semantics, including objects beyond page contents."""
import hashlib

import fitz
import pytest

from folimeld.model import PdfDocument


@pytest.mark.parametrize('encrypted', [False, True])
@pytest.mark.parametrize('worker', [False, True])
def test_save_preserves_images_links_annotations_forms_and_attachments(tmp_path, encrypted, worker):
    source = tmp_path / 'source.pdf'
    with fitz.open() as doc:
        first = doc.new_page()
        pixmap = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 32, 32), False)
        pixmap.clear_with(127)
        first.insert_image(fitz.Rect(10, 10, 100, 100), pixmap=pixmap)
        first.insert_text((30, 150), 'Preserved text')
        first.add_text_annot((200, 100), 'Preserved annotation')
        widget = fitz.Widget()
        widget.field_name = 'name'
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_value = 'Preserved field'
        widget.rect = fitz.Rect(30, 200, 200, 230)
        first.add_widget(widget)
        doc.new_page()
        doc[0].insert_link({'kind': fitz.LINK_GOTO, 'from': fitz.Rect(20, 140, 180, 160),
                            'page': 1, 'to': fitz.Point(0, 0)})
        doc.embfile_add('notes.txt', b'Preserved attachment')
        doc.set_toc([[1, 'Chapter', 2]])
        doc.set_metadata({'title': 'Preserved title'})
        doc.set_xml_metadata('<metadata>Preserved XMP</metadata>')
        doc.save(source)
    original = hashlib.sha256(source.read_bytes()).digest()
    model = PdfDocument()
    try:
        model.open(str(source))
        before = model.doc[0].get_pixmap().digest
        if encrypted:
            model.set_view_password('secret')
        destination = tmp_path / 'saved.pdf'
        if worker:
            from folimeld.pdf_save import save_with_progress

            model.save(str(destination), writer=lambda document, path, options:
                       save_with_progress(document, path, options, None, 'Saving'))
        else:
            model.save(str(destination))
        with fitz.open(destination) as saved:
            assert bool(saved.needs_pass) == encrypted
            if encrypted:
                assert saved.authenticate('secret')
            assert saved.page_count == 2
            assert saved[0].get_pixmap().digest == before
            assert saved[0].get_text().startswith('Preserved text')
            assert saved[0].get_links()[0]['page'] == 1
            assert list(saved[0].annots())[0].info['content'] == 'Preserved annotation'
            assert list(saved[0].widgets())[0].field_value == 'Preserved field'
            assert saved.embfile_get('notes.txt') == b'Preserved attachment'
            assert saved.get_toc() == [[1, 'Chapter', 2]]
            assert saved.metadata['title'] == 'Preserved title'
            assert saved.get_xml_metadata() == '<metadata>Preserved XMP</metadata>'
        assert hashlib.sha256(source.read_bytes()).digest() == original
    finally:
        model.close()
