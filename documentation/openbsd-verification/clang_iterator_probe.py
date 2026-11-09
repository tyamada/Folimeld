from pathlib import Path
import os,json
import clang.cindex as c
root=Path('/home/folimeld/native-build/pymupdf-1.28.2/mupdf-1.28.2-source')
os.chdir(root)
text='#include "mupdf/extra.h"\n#include "mupdf/fitz.h"\n#include "mupdf/pdf.h"\n'
tu=c.Index.create().parse('probe.cpp',unsaved_files=[('probe.cpp',text)],args=['-Iinclude','-Iplatform/c++/include','-DMUPDF_WRAP_LIBCLANG','-DFZ_FUNCTION='],options=c.TranslationUnit.PARSE_INCOMPLETE|c.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
r={'diagnostics':[str(d) for d in tu.diagnostics],'types':{}}
for cur in tu.cursor.walk_preorder():
 if cur.kind==c.CursorKind.TYPEDEF_DECL and cur.spelling in ['fz_stext_block','fz_stext_line','fz_stext_page']:
  typ=cur.type.get_canonical();dec=typ.get_declaration();definition=dec.get_definition()
  r['types'][cur.spelling]={'typedef_location':str(cur.location),'canonical':typ.spelling,'declaration':str(dec.location),'is_definition':dec.is_definition(),'fields':[f.spelling for f in typ.get_fields()],'definition':str(definition.location) if definition else None,'definition_fields':[f.spelling for f in definition.type.get_fields()] if definition else None}
import sys
sys.path.insert(0,str(root/'scripts'))
from wrap import parse,state
state.state_.show_details=lambda name:False
r['iterators']={}
for cur in tu.cursor.walk_preorder():
 if cur.kind==c.CursorKind.TYPEDEF_DECL and cur.spelling in ['fz_stext_block','fz_stext_line','fz_stext_page']:
  name={'fz_stext_block':'u.t.first_line','fz_stext_line':'first_char','fz_stext_page':'first_block'}[cur.spelling]
  found=parse.find_name(cur,name)
  r['iterators'][cur.spelling]={'name':name,'found':str(found.location) if found else None,'members':[(f.spelling,str(f.kind),f.type.spelling) for f in parse.get_members(cur)]}
for cur in tu.cursor.walk_preorder():
 if cur.kind==c.CursorKind.TYPEDEF_DECL and cur.spelling=='fz_stext_block':
  r['nested']={}
  for name in ['u','u.t','u.t.first_line']:
   f=parse.find_name(cur,name)
   r['nested'][name]=None if not f else {'location':str(f.location),'kind':str(f.kind),'type_kind':str(f.type.kind),'type':f.type.spelling,'members':[(m.spelling,str(m.kind),m.type.spelling) for m in parse.get_members(f)],'fields':[(m.spelling,str(m.kind)) for m in f.type.get_canonical().get_fields()]}
print(json.dumps(r,indent=2))
