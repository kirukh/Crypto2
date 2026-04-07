"""CLI-Einstieg für die Konsolen-Demo."""

from __future__ import annotations

import argparse
import sys

from stateful_signatures.stateful_demo import run_demo_scenario


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog="python -m stateful_signatures",
        description=(
            "Didaktische Demo: zustandsbehaftetes Signieren mit Index "
            "(Lehr-Modell, kein XMSS/RFC 8391)."
        ),
        epilog=(
            "Benchmark (nach pip install -e \".[dev]\"): "
            "python -m pytest tests/test_benchmark_stateful.py --benchmark-only"
        ),
    )


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    parser.parse_args(argv)
    run_demo_scenario()


if __name__ == "__main__":
    main(sys.argv[1:])
