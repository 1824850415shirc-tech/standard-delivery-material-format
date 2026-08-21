#!/usr/bin/env python3
"""Check whether the exact target FangSong font is installed."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys


TARGETS = ("FangSong_GB2312", "仿宋_GB2312")


def flatten_strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from flatten_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from flatten_strings(child)
    elif isinstance(value, str):
        yield value


def installed_font_text() -> str:
    system = platform.system()
    if system == "Darwin" and shutil.which("system_profiler"):
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType", "-json"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return "\n".join(flatten_strings(data))
            except json.JSONDecodeError:
                return result.stdout
    if shutil.which("fc-list"):
        result = subprocess.run(["fc-list"], check=False, capture_output=True, text=True)
        return result.stdout
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    haystack = installed_font_text().casefold()
    found = [name for name in TARGETS if name.casefold() in haystack]
    if found:
        print("PASS: installed target font:", ", ".join(found))
        return 0
    print(
        "WARN: FangSong_GB2312/仿宋_GB2312 was not found. "
        "The DOCX can still record the Windows font name, but local rendering may use a fallback."
    )
    return 2 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
