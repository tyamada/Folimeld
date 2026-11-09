"""Record importable native dependencies rather than relying on pip metadata."""
import json
import os
from pathlib import Path
import platform
import sys
import sysconfig

import cryptography
import PIL
import psutil
import pymupdf
import PySide6
import shiboken6
from PySide6.QtCore import qVersion


print(json.dumps({
    "platform": platform.platform(), "python": sys.version,
    "source_commit": Path("SOURCE-COMMIT").read_text().strip(),
    "dependencies": {"PySide6": PySide6.__version__, "Qt": qVersion(),
                     "shiboken6": shiboken6.__version__, "PyMuPDF": pymupdf.__version__,
                     "MuPDF": list(pymupdf.mupdf_version_tuple), "Pillow": PIL.__version__,
                     "cryptography": cryptography.__version__, "psutil": psutil.__version__},
    "extension_suffix": sysconfig.get_config_var("EXT_SUFFIX"),
    "library_path": os.environ.get("LD_LIBRARY_PATH"),
}, indent=2))
