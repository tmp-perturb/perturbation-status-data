#!/usr/bin/env python3
"""Materialize one standardized perturbation-status benchmark dataset."""

import argparse
import json
import os
from pathlib import Path


def link(source: str, destination: Path) -> None:
    path = Path(source).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    if destination.exists() or destination.is_symlink():
        destination.unlink()
    destination.symlink_to(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--h5ad", required=True)
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    h5ad_out = output / f"{args.name}.h5ad"
    link(args.h5ad, h5ad_out)
    spec = {"dataset": args.name, "h5ad": os.path.abspath(h5ad_out)}
    (output / f"{args.name}.spec.json").write_text(
        json.dumps(spec, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
