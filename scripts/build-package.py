#!/usr/bin/env python3
"""Build dist/<name>-<version>.zip with the files APM needs to install this package."""

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = (ROOT / "apm.yml").read_text(encoding="utf-8")


def read_field(key):
    match = re.search(rf"^{key}:\s*\"?([^\"\n]+?)\"?\s*$", manifest, re.MULTILINE)
    if not match:
        sys.exit(f"apm.yml: '{key}' not found")
    return match.group(1)


name = read_field("name")
version = read_field("version")
dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
target = dist / f"{name}-{version}.zip"

files = [ROOT / "apm.yml", ROOT / "README.md", ROOT / "LICENSE"]
files += sorted(p for p in (ROOT / ".apm").rglob("*") if p.is_file())

with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for file in files:
        if file.exists():
            archive.write(file, file.relative_to(ROOT).as_posix())

print(f"Created {target.relative_to(ROOT)} with {len(files)} entries")
