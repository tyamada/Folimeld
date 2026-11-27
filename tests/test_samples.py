import copy
import hashlib
import io
import json
from threading import Event
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication

from folimeld import sample_catalogue as samples
from folimeld.sample_catalogue_data import BUNDLED_CATALOGUE


PDF = b'%PDF-1.7\nverified sample fixture\n%%EOF\n'


def entry():
    value = copy.deepcopy(json.loads(BUNDLED_CATALOGUE)['entries'][0])
    value['bytes'] = len(PDF)
    value['sha256'] = hashlib.sha256(PDF).hexdigest()
    return value


def raw(entries=None):
    return json.dumps({'schema_version': 1, 'entries': entries or [entry()]}).encode()


class Response(io.BytesIO):
    def __init__(self, payload, length=None):
        super().__init__(payload)
        self.headers = {} if length is None else {'Content-Length': str(length)}


def test_bundled_catalogue_has_51_unique_fixed_release_books():
    entries = samples.parse_catalogue(BUNDLED_CATALOGUE.encode())
    assert len(entries) == 51
    assert len({e['sample_id'] for e in entries}) == 51
    assert {e['episode'] for e in entries} == {1, 2, 3}
    assert len({e['language_key'] for e in entries}) == 17
    assert all('/manga-pdf-20261103-v1/' in e['new_download_url'] for e in entries)


@pytest.mark.parametrize('payload', [b'invalid', b'[]', b'{}', b'{"schema_version":2,"entries":[]}',
    b'{"schema_version":1,"schema_version":1,"entries":[]}',
    b'{"schema_version":true,"entries":[]}', b'\xff'])
def test_invalid_json_and_schemas(payload):
    with pytest.raises((ValueError, UnicodeError)):
        samples.parse_catalogue(payload)


@pytest.mark.parametrize('key,value', [('sample_id','../escape'),('filename','../bad.pdf'),
    ('bytes',True),('bytes',samples.MAX_PDF_BYTES+1),('pages',0),('sha256','bad'),
    ('license','unknown'),('new_download_url','http://github.com/a.pdf'),
    ('title','bad\ntext')])
def test_invalid_metadata(key,value):
    item = entry(); item[key] = value
    with pytest.raises(ValueError):
        samples.parse_catalogue(raw([item]))


def test_duplicate_ids_and_filename_url_mismatch():
    with pytest.raises(ValueError):
        samples.parse_catalogue(raw([entry(),entry()]))
    item=entry();item['filename']='different.pdf'
    with pytest.raises(ValueError):
        samples.parse_catalogue(raw([item]))


@pytest.mark.parametrize('url', ['http://github.com/a','https://evil.example/a',
    'https://github.com/tyamada/manga-prompt-kit/releases/latest/download/file.pdf',
    'https://github.com/other/repo/releases/download/tag/file.pdf',
    'https://user@github.com/tyamada/manga-prompt-kit/releases/download/tag/file.pdf',
    'https://github.com/tyamada/manga-prompt-kit/releases/download/tag/%2e%2e.pdf',
    'https://github.com/tyamada/manga-prompt-kit/releases/download/tag/file.pdf?bad=1',
    'https://github.com:8000/tyamada/manga-prompt-kit/releases/download/tag/file.pdf'])
def test_reject_unapproved_urls(url):
    with pytest.raises(ValueError):
        samples.validate_url(url)


def test_redirect_allowlist():
    assert samples.validate_url('https://release-assets.githubusercontent.com/github-production-release-asset/1/2?sig=x',redirect=True)
    with pytest.raises(ValueError):
        samples.validate_url('https://release-assets.githubusercontent.com/other',redirect=True)
    with pytest.raises(ValueError):
        samples._Redirect().redirect_request(None,None,302,'',{},'http://example.com/a')


def test_valid_catalogue_cache_and_bad_refresh_preserves_previous(tmp_path):
    payload=raw()
    with patch.object(samples,'_read_catalogue',return_value=payload):
        assert samples.load_catalogue(tmp_path,Event())[1]=='online'
    cache=tmp_path/'catalogue-v1.json';original=cache.read_bytes()
    for bad in (b'not JSON',raw([entry(),entry()])):
        with patch.object(samples,'_read_catalogue',return_value=bad):
            assert samples.load_catalogue(tmp_path,Event())[1]=='cached'
        assert cache.read_bytes()==original
    with patch.object(samples,'_read_catalogue',side_effect=OSError('offline')):
        assert samples.load_catalogue(tmp_path,Event())[1]=='cached'
    cache.write_bytes(b'corrupt')
    with patch.object(samples,'_read_catalogue',side_effect=OSError('offline')):
        entries,source=samples.load_catalogue(tmp_path,Event())
    assert source=='bundled' and len(entries)==51
    assert cache.read_bytes()==b'corrupt'


def test_download_only_selected_verify_and_reuse_offline(tmp_path):
    item=entry();progress=[]
    with patch.object(samples,'open_url',return_value=Response(PDF,len(PDF))) as network:
        result=samples.download_sample(tmp_path,item,Event(),lambda d,t:progress.append((d,t)))
    network.assert_called_once_with(item['new_download_url'])
    assert result.read_bytes()==PDF
    assert progress[-1]==(len(PDF),len(PDF))
    with patch.object(samples,'open_url',side_effect=AssertionError('Must reuse offline cache')):
        assert samples.download_sample(tmp_path,item,Event())==result
    work=samples.working_copy(tmp_path,result,item,Event())
    work.write_bytes(b'User-edited document')
    assert result.read_bytes()==PDF
    assert not list(tmp_path.rglob('*.part'))


@pytest.mark.parametrize('payload,length',[ (PDF[:-1],None),(PDF+b'x',None),
    (PDF.replace(b'fixture',b'changed'),None),(PDF,len(PDF)+1),
    (b'NOTDF'+PDF[5:],None)])
def test_failed_download_never_becomes_completed_pdf(tmp_path,payload,length):
    sentinel=tmp_path/'existing-user.pdf';sentinel.write_bytes(b'keep')
    with patch.object(samples,'open_url',return_value=Response(payload,length)):
        with pytest.raises(ValueError):
            samples.download_sample(tmp_path,entry(),Event())
    assert not list((tmp_path/'originals').glob('*.pdf'))
    assert not list(tmp_path.rglob('*.part'))
    assert sentinel.read_bytes()==b'keep'


def test_cancel_and_corrupt_cache_preservation(tmp_path):
    item=entry();folder=tmp_path/'originals';folder.mkdir()
    damaged=folder/(item['sha256']+'.pdf');damaged.write_bytes(b'corrupt')
    cancel=Event()
    with patch.object(samples,'open_url',return_value=Response(PDF)):
        with pytest.raises(samples.Cancelled):
            samples.download_sample(tmp_path,item,cancel,lambda *_:cancel.set())
    assert damaged.read_bytes()==b'corrupt'
    assert not list(folder.glob('*.part'))
    with patch.object(samples,'open_url',return_value=Response(PDF)):
        result=samples.download_sample(tmp_path,item,Event())
    assert result.read_bytes()==PDF
    assert list(folder.glob('*.corrupt-*'))[0].read_bytes()==b'corrupt'


def test_entry_points_preserve_unsaved_document_and_selection_identity(tmp_path):
    import fitz
    from folimeld.app import MainWindow
    from folimeld.sample_dialog import SampleDialog
    with patch('folimeld.app.is_packaged',return_value=False):
        window=MainWindow()
    path=tmp_path/'existing.pdf'
    with fitz.open() as pdf:
        pdf.new_page();pdf.save(path)
    window.open_path(str(path));window.model.rotate([0],90)
    window.sample_dialog=SampleDialog(window.tr_,window,root=tmp_path/'cache')
    window.sample_dialog.loaded=True
    window.sample_dialog.selected.connect(window.open_path)
    window.samples_action.trigger()
    assert window.sample_dialog.isVisible() and not window.sample_dialog.isModal()
    with patch.object(window,'confirm_discard',return_value=False):
        window.sample_dialog.selected.emit(str(tmp_path/'other.pdf'))
    assert window.model.path==path and window.model.dirty
    assert path.read_bytes().startswith(b'%PDF-')
    with patch.object(window,'confirm_discard',return_value=True):
        window.close()


def test_dialog_background_results_keep_entry_ids_when_sorted(tmp_path):
    from time import monotonic
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    dialog=SampleDialog(I18n().tr,root=tmp_path)
    with patch('folimeld.sample_dialog.load_catalogue',return_value=(samples.parse_catalogue(BUNDLED_CATALOGUE.encode()),'bundled')):
        dialog.refresh_catalogue()
        deadline=monotonic()+5
        while dialog.worker is not None and monotonic()<deadline:
            QApplication.processEvents()
        assert dialog.worker is None
    dialog.language_filter.setCurrentIndex(dialog.language_filter.findData(''))
    assert dialog.tree.topLevelItemCount()==51
    dialog.tree.sortItems(2, __import__('PySide6.QtCore',fromlist=['Qt']).Qt.SortOrder.DescendingOrder)
    item=dialog.tree.topLevelItem(0)
    item.setSelected(True)
    from PySide6.QtCore import Qt
    selected=item.data(0,Qt.ItemDataRole.UserRole)
    assert item.text(2)==selected['title']
    assert item.text(1)==selected['language_key']+' / '+selected['locale']
    with patch.object(dialog,'_start') as start:
        dialog.open_selected()
    assert start.call_args.args[0]['sample_id']==selected['sample_id']
    dialog.close()


def test_fragmented_header_is_verified(tmp_path):
    class Fragmented(Response):
        def read1(self, size):
            return super().read(1)
    with patch.object(samples,'open_url',return_value=Fragmented(PDF)):
        result=samples.download_sample(tmp_path,entry(),Event())
    assert result.read_bytes()==PDF


def test_application_exit_cancels_active_sample_worker_before_close(tmp_path):
    from folimeld.app import MainWindow
    from folimeld.sample_dialog import SampleDialog
    from PySide6.QtCore import QObject,Signal
    from PySide6.QtGui import QCloseEvent
    class Worker(QObject):
        finished=Signal()
        def __init__(self):
            super().__init__();self.cancel=Event()
    with patch('folimeld.app.is_packaged',return_value=False):
        window=MainWindow()
    dialog=SampleDialog(window.tr_,window,root=tmp_path)
    window.sample_dialog=dialog
    worker=Worker();dialog.worker=worker
    event=QCloseEvent()
    window.closeEvent(event)
    assert not event.isAccepted()
    assert worker.cancel.is_set()
    dialog.worker=None
    worker.finished.emit()
    assert not window.isVisible()


def test_selected_download_cancellation_never_emits_open_path(tmp_path):
    from time import monotonic
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    item=entry()
    dialog=SampleDialog(I18n().tr,root=tmp_path)
    captured=[]
    dialog.selected.connect(captured.append)
    class CancellingResponse(Response):
        def read1(self,size=-1):
            dialog.worker.cancel.set()
            return super().read(size)
    with patch('folimeld.sample_catalogue.open_url',return_value=CancellingResponse(PDF)):
        dialog._start(item)
        deadline=monotonic()+5
        while dialog.worker is not None and monotonic()<deadline:
            QApplication.processEvents()
        assert dialog.worker is None
    assert not captured
    assert not list(tmp_path.rglob('*.part'))
    dialog.close()


@pytest.mark.parametrize('language,expected', [('ja','ja'),('en','en'),('pt-PT','pt_pt'),('zh-TW','zh_tw'),('unsupported','')])
def test_language_default_order_and_footer(tmp_path,language,expected):
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    translator=I18n();translator.load('ja')
    dialog=SampleDialog(translator.tr,root=tmp_path,language=language)
    dialog.entries=samples.parse_catalogue(BUNDLED_CATALOGUE.encode())
    dialog._update_languages();dialog._render_entries()
    assert dialog.language_filter.count()==18
    assert dialog.language_filter.currentData()==expected
    assert dialog.episode_order.currentData()=='latest'
    expected_count=3 if expected else 51
    assert dialog.tree.topLevelItemCount()==expected_count
    def episodes():
        return [int(dialog.tree.topLevelItem(i).text(0)) for i in range(dialog.tree.topLevelItemCount())]
    assert episodes()==sorted(episodes(),reverse=True)
    dialog.episode_order.setCurrentIndex(dialog.episode_order.findData('first'))
    assert episodes()==sorted(episodes())
    assert 'こまいろ日和 / Komairo Hiyori' in dialog.copyright_notice.text()
    assert '著作権者' in dialog.copyright_notice.text()
    assert 'ライセンス' in dialog.license_notice.text()
    assert 'CC BY 4.0' in dialog.license_notice.text()
    assert samples.LICENSE_URL in dialog.license_notice.text()
    assert samples.SOURCE_PAGE_URL in dialog.license_notice.text()
    assert dialog.license_notice.openExternalLinks()
    dialog.close()


def test_filter_refresh_preserves_all_choice_and_selected_identity(tmp_path):
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    from PySide6.QtCore import Qt
    dialog=SampleDialog(I18n().tr,root=tmp_path,language='ja')
    dialog.entries=samples.parse_catalogue(BUNDLED_CATALOGUE.encode())
    dialog._update_languages();dialog._render_entries()
    assert dialog.tree.topLevelItemCount()==3
    item=dialog.tree.topLevelItem(0);item.setSelected(True)
    sample_id=item.data(0,Qt.ItemDataRole.UserRole)['sample_id']
    dialog.episode_order.setCurrentIndex(1)
    assert dialog.tree.selectedItems()[0].data(0,Qt.ItemDataRole.UserRole)['sample_id']==sample_id
    dialog.language_filter.setCurrentIndex(dialog.language_filter.findData(''))
    assert dialog.tree.topLevelItemCount()==51
    dialog._update_languages();dialog._render_entries()
    assert dialog.language_filter.currentData()==''
    assert dialog.tree.topLevelItemCount()==51
    dialog.language_filter.setCurrentIndex(dialog.language_filter.findData('en'))
    assert dialog.tree.topLevelItemCount()==3
    assert not dialog.tree.selectedItems()
    assert not dialog.open_button.isEnabled()
    item=dialog.tree.topLevelItem(0);item.setSelected(True)
    with patch.object(dialog,'_start') as start:
        dialog.open_selected()
    assert start.call_args.args[0]['language_key']=='en'
    dialog._set_busy(True)
    assert not dialog.language_filter.isEnabled()
    assert not dialog.episode_order.isEnabled()
    dialog._set_busy(False)
    dialog.close()


def test_system_language_is_used_without_app_language(tmp_path):
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    from PySide6.QtCore import QLocale
    translator=I18n()
    dialog=SampleDialog(lambda key,**kwargs:translator.tr(key,**kwargs),root=tmp_path)
    dialog.entries=samples.parse_catalogue(BUNDLED_CATALOGUE.encode())
    with patch('folimeld.sample_dialog.QLocale.system',return_value=QLocale('pt_PT')):
        dialog._update_languages()
    assert dialog.language_filter.currentData()=='pt_pt'
    dialog.close()


def test_episode_order_is_numeric(tmp_path):
    from folimeld.sample_dialog import SampleDialog
    from folimeld.i18n import I18n
    dialog=SampleDialog(I18n().tr,root=tmp_path,language='ja')
    dialog.entries=samples.parse_catalogue(BUNDLED_CATALOGUE.encode())
    extra=copy.deepcopy(next(e for e in dialog.entries if e['sample_id']=='ep1_ja'))
    extra.update(sample_id='ep10_ja',episode=10,title='Episode 10 fixture')
    dialog.entries.append(extra)
    dialog._update_languages();dialog._render_entries()
    assert [int(dialog.tree.topLevelItem(i).text(0)) for i in range(4)]==[10,3,2,1]
    dialog.episode_order.setCurrentIndex(1)
    assert [int(dialog.tree.topLevelItem(i).text(0)) for i in range(4)]==[1,2,3,10]
    dialog.close()


def test_main_window_passes_active_app_language():
    from folimeld.app import MainWindow
    from folimeld.i18n import I18n
    translator=I18n();translator.load('en')
    with patch('folimeld.app.is_packaged',return_value=False):
        window=MainWindow(translator)
    with patch('folimeld.sample_dialog.SampleDialog.refresh_catalogue'):
        window.show_samples()
    assert window.sample_dialog.preferred_language=='en'
    window.close()
