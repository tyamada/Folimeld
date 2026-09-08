"""Download exact PyPI source distributions without running package build code.

Usage: python tools/fetch_dependency_sources.py PyMuPDF==1.28.2 Pillow==12.3.0
Packages without an sdist (notably PySide6) require upstream source collection.
Native libraries nested in wheels require separate verification as well.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import urlopen


def fetch(requirement, output):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+==[A-Za-z0-9_.+-]+", requirement):
        raise ValueError("Specify an exact public package version: Name==version")
    name, version = requirement.split("==")
    metadata_url = f"https://pypi.org/pypi/{name}/{version}/json"
    with urlopen(metadata_url, timeout=60) as response:
        metadata = json.load(response)
    sources = [entry for entry in metadata["urls"] if entry["packagetype"] == "sdist"]
    if not sources:
        return {"package": requirement, "status": "upstream-source-required", "metadata_url": metadata_url}
    results = []
    for entry in sources:
        name = entry["filename"]
        if Path(name).name != name or "/" in name or "\\" in name:
            raise ValueError("Unsafe source filename")
        url = entry["url"]
        if not url.startswith("https://files.pythonhosted.org/"):
            raise ValueError("Unexpected source download host")
        destination = output / name
        expected = entry["digests"]["sha256"]
        checksum = hashlib.sha256()
        temporary = output / (name + ".part")
        with urlopen(url, timeout=60) as response, temporary.open("wb") as stream:
            while chunk := response.read(1024 * 1024):
                checksum.update(chunk)
                stream.write(chunk)
        if checksum.hexdigest() != expected:
            temporary.unlink()
            raise ValueError(f"Checksum mismatch for {name}")
        temporary.replace(destination)
        results.append({"filename": name, "url": url, "sha256": expected})
    return {"package": requirement, "status": "sdist-downloaded-native-sources-not-yet-verified",
            "metadata_url": metadata_url, "files": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages", nargs="+")
    parser.add_argument("--output", type=Path, default=Path("dist/source/dependencies"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for requirement in args.packages:
        result = fetch(requirement, args.output)
        (args.output / (requirement + ".json")).write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{requirement}: {result['status']}", flush=True)


if __name__ == "__main__":
    main()
