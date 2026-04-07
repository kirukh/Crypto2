"""Smoke-Test für die CLI (Konsolen-Demo)."""

import pytest

from stateful_signatures.demo import build_parser, main


def test_help_exits_zero():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--help"])
    assert exc_info.value.code == 0


def test_demo_prints_scenario(capsys):
    main([])
    out = capsys.readouterr().out
    assert "Didaktische Demo" in out
    assert "Wiederherstellung" in out
