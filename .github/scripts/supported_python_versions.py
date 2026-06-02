#!/usr/bin/env python3
"""Print supported Python versions, read from pyproject.toml classifiers.

Used by .github/workflows/lint_test.yml to derive the test matrix from
[project].classifiers, avoiding duplication. Requires Python 3.11+ (tomllib).

Usage:
    python supported_python_versions.py            # JSON array of all
    python supported_python_versions.py oldest     # first element
    python supported_python_versions.py newest     # last element
"""

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
PREFIX = "Programming Language :: Python :: 3."
ENVLIST_RE = re.compile(r"^envlist\s*=\s*py3\{([\d,\s]+)\}", re.MULTILINE)


def supported_versions() -> list[str]:
    with PYPROJECT.open("rb") as f:
        data = tomllib.load(f)
    versions: set[str] = set()
    for classifier in data["project"]["classifiers"]:
        if not classifier.startswith(PREFIX):
            continue
        minor = classifier[len(PREFIX) :].strip()
        if minor.isdigit():
            versions.add(f"3.{minor}")
    return sorted(versions, key=lambda v: tuple(int(p) for p in v.split(".")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "which",
        nargs="?",
        default="all",
        choices=["all", "oldest", "newest"],
    )
    args = parser.parse_args()

    versions = supported_versions()
    if not versions:
        print(f"No '{PREFIX}X' classifiers found in {PYPROJECT}", file=sys.stderr)
        return 1

    if args.which == "all":
        json.dump(versions, sys.stdout)
    elif args.which == "oldest":
        sys.stdout.write(versions[0])
    else:
        sys.stdout.write(versions[-1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
