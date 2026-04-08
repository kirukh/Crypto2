import pytest
from stateful_signatures.stateful_demo import LamportOTS, verify_lamport

def test_lamport_sign_and_verify():
    signer = LamportOTS()
    message = b"Testnachricht"
    sig = signer.sign(message)
    
    # Korrekte Verifikation
    assert verify_lamport(signer.public_key, message, sig) is True
    # Manipulation erkennen
    assert verify_lamport(signer.public_key, b"Gefaelscht", sig) is False

def test_ots_enforcement():
    signer = LamportOTS()
    signer.sign(b"Erste Nachricht")
    
    # Der zweite Versuch MUSS scheitern (Stateful-Schutz)
    with pytest.raises(RuntimeError, match="SECURITY BREACH"):
        signer.sign(b"Zweite Nachricht")