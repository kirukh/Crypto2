import pytest

from stateful_signatures.stateful_demo import StatefulSigner, verify


def test_sign_advances_index():
    s = StatefulSigner(b"k" * 32)
    assert s.index == 0
    sig0 = s.sign(b"m")
    assert sig0.index == 0
    assert s.index == 1
    sig1 = s.sign(b"m")
    assert sig1.index == 1
    assert verify(b"k" * 32, b"m", sig0)
    assert verify(b"k" * 32, b"m", sig1)


def test_verify_rejects_wrong_message():
    s = StatefulSigner(b"k" * 32)
    sig = s.sign(b"original")
    assert not verify(b"k" * 32, b"tampered", sig)


def test_short_secret_rejected():
    with pytest.raises(ValueError):
        StatefulSigner(b"short")
