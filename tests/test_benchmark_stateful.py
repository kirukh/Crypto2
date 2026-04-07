"""Micro-Benchmarks für Sign/Verify (pytest-benchmark)."""

import pytest

from stateful_signatures.stateful_demo import StatefulSigner, verify

_SECRET = b"benchmark-secret-key-32bytes!!"
_PAYLOAD = b"payload-for-benchmark"


@pytest.fixture
def signer():
    return StatefulSigner(_SECRET)


@pytest.fixture
def sample_sig(signer):
    return signer.sign(_PAYLOAD)


def test_benchmark_sign(benchmark, signer):
    benchmark(signer.sign, b"message")


def test_benchmark_verify(benchmark, sample_sig):
    benchmark(verify, _SECRET, _PAYLOAD, sample_sig)
