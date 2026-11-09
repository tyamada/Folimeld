from pathlib import Path
import os,json
import clang.cindex as c
root=Path('/home/folimeld/native-build/pymupdf-1.28.2/mupdf-1.28.2-source')
os.chdir(root)
text='#include "mupdf/extra.h"\n#include "mupdf/fitz.h"\n#include "mupdf/pdf.h"\n'
tu=c.Index.create().parse('probe.cpp',unsaved_files=[('probe.cpp',text)],args=['-Iinclude','-Iplatform/c++/include','-DMUPDF_WRAP_LIBCLANG','-DFZ_FUNCTION='],options=c.TranslationUnit.PARSE_INCOMPLETE|c.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
r={'diagnostics':[str(d) for d in tu.diagnostics],'types':{}}
for cur in tu.cursor.walk_preorder():
 if cur.kind==c.CursorKind.TYPEDEF_DECL and cur.spelling in ['fz_pixmap','fz_document','fz_colorspace','pdf_document']:
  typ=cur.type.get_canonical();dec=typ.get_declaration();definition=dec.get_definition()
  r['types'][cur.spelling]={'typedef_location':str(cur.location),'canonical':typ.spelling,'declaration':str(dec.location),'is_definition':dec.is_definition(),'fields':[f.spelling for f in typ.get_fields()],'definition':str(definition.location) if definition else None,'definition_fields':[f.spelling for f in definition.type.get_fields()] if definition else None}
print(json.dumps(r,indent=2))
