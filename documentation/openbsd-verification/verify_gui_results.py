from pathlib import Path
import hashlib,json,subprocess,platform
import pymupdf as fitz
root=Path('/home/folimeld/Folimeld');p=root/'build/openbsd-verification'
def open_pdf(name,password=None):
 d=fitz.open(p/name)
 if password:assert d.authenticate(password)
 return d
def streams(d):return [hashlib.sha256(b''.join(d.xref_stream(x) for x in q.get_contents())).hexdigest() for q in d]
def widgets(d):return [(w.field_name,w.field_type,w.field_value,w.field_flags,w.choice_values,list(w.rect)) for w in d[0].widgets()]
source=fitz.open(root/'testdata/tameshibu_episode3_ja.pdf')
src_hash=hashlib.sha256((root/'testdata/tameshibu_episode3_ja.pdf').read_bytes()).hexdigest()
assert src_hash=='4abfe0f4a028bbac280c7629cd64c72e5df1faac8348695e0277dfc5a9154558'
core=open_pdf('gui-manual-after.pdf');order=[streams(source).index(x)+1 for x in streams(core)]
assert order==[2,1,3,4,5,6,7,8] and [q.rotation for q in core]==[0,90,0,0,0,0,0,0]
props=open_pdf('gui-properties.pdf');cat=props.pdf_catalog()
assert props.metadata['format']=='PDF 1.7' and props.xref_get_key(cat,'PageLayout')[1]=='/SinglePage' and props.xref_get_key(cat,'ViewerPreferences/Direction')[1]=='/L2R'
form_source=open_pdf('forms-source.pdf');forms=open_pdf('gui-forms.pdf')
assert widgets(form_source)==widgets(forms) and len(widgets(forms))==3 and forms[0].rotation==270
enc=open_pdf('gui-encrypted.pdf');assert enc.needs_pass and not enc.authenticate('wrong-test-password') and enc.authenticate('OpenBSD-test-only')
changed=open_pdf('gui-password-changed.pdf');assert changed.needs_pass and not changed.authenticate('OpenBSD-test-only') and changed.authenticate('OpenBSD-changed-only')
removed=open_pdf('gui-password-removed.pdf');assert not removed.needs_pass and not removed.is_encrypted
assert widgets(form_source)==widgets(enc)==widgets(changed)==widgets(removed)
images=open_pdf('gui-images.pdf');expected=[(20,100,160),(255,155,155),(255,0,0),(0,128,0),(0,0,255),(200,100,160)]
colors=[q.get_pixmap(matrix=fitz.Matrix(.25,.25),alpha=False).pixel(74,105) for q in images]
assert len(images)==6 and all(abs(q.rect.width-595.28)<1 and abs(q.rect.height-841.89)<1 for q in images)
assert all(max(abs(a-b) for a,b in zip(actual,want))<=4 for actual,want in zip(colors,expected))
recovered=open_pdf('gui-recovered.pdf');assert [q.rotation for q in recovered]==[90,0,0,0,0,0] and streams(recovered)==streams(images)
protected_hash=hashlib.sha256((p/'readonly/existing.pdf').read_bytes()).hexdigest()
assert protected_hash=='7c87f63c22879cfca13b6ae6ab3a845466dfd231057061d2de5f7194e2332967'
japanese=open_pdf('日本語 sample.pdf');assert streams(japanese)==streams(source) and [q.rotation for q in japanese]==[90,0,0,0,0,0,0,0]
load=open_pdf('gui-load-1000.pdf');assert len(load)==1000 and [q.rotation for q in load]==[0]*999+[90] and load[-1].get_text().strip()=='OpenBSD load page 1000'
history_source=open_pdf('history-images-100.pdf');history=open_pdf('gui-history-restored.pdf');assert len(history)==100 and streams(history)==streams(history_source) and all(q.rotation==0 for q in history)
for i in [0,96,99]:assert history[i].get_pixmap().samples==history_source[i].get_pixmap().samples
def large_tmp(name):
 out=[]
 for line in Path('/home/folimeld/'+name).read_text().splitlines():
  fields=line.split()
  if '/tmp' in fields and fields[-1].isdigit() and int(fields[-1])>1024*1024:out.append(int(fields[-1]))
 return out
before=large_tmp('history-fstat-before.txt');after=large_tmp('history-fstat-after.txt');cleared=large_tmp('history-fstat-cleared.txt')
assert not before and len(after)==3 and not cleared
cases=[('gui-manual-after.pdf',None),('gui-properties.pdf',None),('gui-forms.pdf',None),('gui-encrypted.pdf','OpenBSD-test-only'),('gui-password-changed.pdf','OpenBSD-changed-only'),('gui-password-removed.pdf',None),('gui-images.pdf',None),('gui-recovered.pdf',None),('日本語 sample.pdf',None),('gui-load-1000.pdf',None),('gui-history-restored.pdf',None)]
outputs={};logs=[]
for name,password in cases:
 args=['qpdf']+([f'--password={password}'] if password else [])+['--check',str(p/name)]
 result=subprocess.run(args,capture_output=True,text=True)
 logs.extend([f'File: {name}',result.stdout,result.stderr]);assert result.returncode==0,(name,result.returncode)
 with (p/name).open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 outputs[name]={'sha256':digest,'bytes':(p/name).stat().st_size,'qpdf_exit_code':result.returncode}
(p/'qpdf-checks.txt').write_text('\n'.join(logs))
r={'platform':platform.platform(),'source_sha256_unchanged':src_hash,'manual_edit':{'pages':8,'order':order,'rotations':[q.rotation for q in core],'content_streams_match':True},'properties':{'format':props.metadata['format'],'layout':'SinglePage','direction':'L2R'},'forms':{'count':3,'values_and_attributes_preserved':True,'rotation':270},'password':{'cancel_retained_document':'observed GUI','wrong_password_reprompt':'observed GUI','change_old_rejected_new_accepted':True,'removal_confirmed':True},'images':{'files_after_gui_exclusion':['image1.jpg','image3.png','image4.tiff','image5.webp','image10.bmp'],'pages':6,'page_sizes':[list(q.rect)[2:] for q in images],'center_rgb':colors,'invalid_image_and_cancel_retained_document':'observed GUI'},'save_error':{'permission_error':'observed GUI','protected_existing_sha256':protected_hash,'recovered_pages':6,'rotations':[q.rotation for q in recovered]},'japanese_space_path':{'pages':8,'rotations':[q.rotation for q in japanese]},'load_1000':{'pages':1000,'last_rotation':90,'last_text':load[-1].get_text().strip()},'history':{'pages':100,'streams_restored':True,'all_rotations_zero':True,'render_samples_restored':[1,97,100],'large_tmp_before':before,'large_tmp_after':after,'large_tmp_after_document_switch':cleared},'settings':{'english_432_after_restart':'observed GUI, gui-settings-persisted.png','restored_config':Path('/home/folimeld/.config/Folimeld/Folimeld.conf').read_text()},'outputs':outputs}
(p/'gui-results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print('GUI_RESULTS_OK',len(outputs),'qpdf checks passed')
