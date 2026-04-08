import pytest
from stateful_signatures.stateful_demo import LamportOTS, verify_lamport

# Wir definieren Test-Daten
_PAYLOAD = b"benchmark-payload-123"

def test_benchmark_sign(benchmark):
    # Setup-Funktion: Erstellt für JEDEN Durchlauf einen neuen Signer
    def setup():
        return (LamportOTS(), _PAYLOAD), {}

    # Benchmark mit pedantic-Modus, um den State-Fehler zu umgehen
    benchmark.pedantic(
        lambda s, m: s.sign(m), 
        setup=setup, 
        rounds=100 # Begrenzt die Runden, da KeyGen Zeit kostet
    )

def test_benchmark_verify(benchmark):
    signer = LamportOTS()
    msg = _PAYLOAD
    sig = signer.sign(msg) # Einmal signieren ist okay
    
    # Verifizieren ändert den State nicht, daher normaler Benchmark möglich
    benchmark(verify_lamport, signer.public_key, msg, sig)