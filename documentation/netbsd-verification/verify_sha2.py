"""Compare the patched MuPDF implementation with Python's SHA-2 results."""
import hashlib
import json
import subprocess
import sys


actual = subprocess.check_output([sys.argv[1]], text=True).splitlines()
expected = [hashlib.sha256(b"abc").hexdigest(), hashlib.sha512(b"abc").hexdigest()]
assert actual == expected, {"actual": actual, "expected": expected}
print(json.dumps({"input": "abc", "sha256": actual[0], "sha512": actual[1],
                  "passed": True}, indent=2))
