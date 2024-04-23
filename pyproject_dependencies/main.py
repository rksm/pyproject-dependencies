#!/usr/bin/env python

import argparse
import pip
try:
    import toml
except Exception as err:
    pip.main(["install", "toml"])
    import toml
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Extract dependencies from pyproject.toml")
    parser.add_argument("--features", nargs="*", help="Features")
    parser.add_argument("--install",
                        "-i",
                        help="Install dependencies",
                        action="store_true")
    parser.add_argument("pyproject",
                        help="Path to pyproject.toml",
                        default="pyproject.toml",
                        type=Path,
                        nargs="?")
    args = parser.parse_args()

    features = args.features or []
    if len(features) == 1 and "," in features[0]:
        features = features[0].split(",")

    def should_install_feature(feature: str) -> bool:
        return len(features) == 0 or feature in features

    pyproject: Path = args.pyproject
    if not pyproject.exists():
        print(f"pyproject.toml not found at {pyproject}")
        exit(1)
    c = toml.load(pyproject)

    deps: set[str] = set()
    dep_list = c["project"].get("dependencies", [])
    for dep in dep_list:
        deps.add(dep)

    optional_dep_list = c["project"].get("optional-dependencies", [])
    for extra in optional_dep_list:
        if should_install_feature(extra):
            for dep in optional_dep_list[extra]:
                deps.add(dep)

    build_dep_list = c["build-system"].get("requires", [])
    for dep in build_dep_list:
        deps.add(dep)

    print("\n".join(sorted(deps)))

    if args.install:
        pip.main(["install", *deps])


if __name__ == '__main__':
    main()
