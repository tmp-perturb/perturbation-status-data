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
    parser.add_argument("--project_root", required=True)
    parser.add_argument("--mixscape_config", required=True)
    parser.add_argument("--pooled_config", required=True)
    parser.add_argument("--mixscale_config", required=True)
    parser.add_argument("--ps_input_config", required=True)
    parser.add_argument("--ps_run_config", required=True)
    parser.add_argument("--target_expression_config", required=True)
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    h5ad_out = output / f"{args.name}.h5ad"
    link(args.h5ad, h5ad_out)
    paths = {
        key: str(Path(value).resolve())
        for key, value in {
            "project_root": args.project_root,
            "mixscape_config": args.mixscape_config,
            "pooled_config": args.pooled_config,
            "mixscale_config": args.mixscale_config,
            "ps_input_config": args.ps_input_config,
            "ps_run_config": args.ps_run_config,
            "target_expression_config": args.target_expression_config,
        }.items()
    }
    missing = [value for value in paths.values() if not Path(value).exists()]
    if missing:
        raise FileNotFoundError(f"Missing configured paths: {missing}")
    spec = {"dataset": args.name, "h5ad": os.path.abspath(h5ad_out), **paths}
    (output / f"{args.name}.spec.json").write_text(
        json.dumps(spec, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
