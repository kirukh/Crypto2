"""
Didaktische Lamport One-Time Signature (OTS) für das Seminarprojekt.

Das Modul zeigt zustandsabhängiges Signieren: Nach einer Signatur ist der
OTS-Schlüssel verbraucht. Ein Szenario simuliert Wiederherstellung aus einem
veralteten Backup (Zustand „noch nicht signiert“), obwohl bereits signiert
wurde — analog zu verlorenem/veraltetem Zählerstand bei XMSS (Theorie in der
Ausarbeitung). Kein Merkle-Baum, kein XMSS (RFC 8391).
"""

from __future__ import annotations

import copy
import hashlib
import os
from typing import List, Tuple

__all__ = ["LamportOTS", "verify_lamport", "run_demo_scenario"]

_BITS = 256


class LamportOTS:
    """
    Didaktische Lamport-OTS (Nachricht wird auf 256 Bit gehasht).

    Nur für Lehrzwecke; nicht side-channel-gehärtet.
    """

    def __init__(self) -> None:
        self._private_key: List[Tuple[bytes, bytes]] = []
        self.public_key: List[Tuple[bytes, bytes]] = []
        self.is_used = False

        for _ in range(_BITS):
            sk_0 = os.urandom(32)
            sk_1 = os.urandom(32)
            self._private_key.append((sk_0, sk_1))
            pk_0 = hashlib.sha256(sk_0).digest()
            pk_1 = hashlib.sha256(sk_1).digest()
            self.public_key.append((pk_0, pk_1))

    @staticmethod
    def _message_to_bits(message: bytes) -> str:
        msg_hash = hashlib.sha256(message).digest()
        return "".join(f"{byte:08b}" for byte in msg_hash)

    def sign(self, message: bytes) -> List[bytes]:
        """Signiert und markiert den OTS als verbraucht."""
        if self.is_used:
            raise RuntimeError(
                "SECURITY BREACH: Dieser OTS-Schlüssel wurde bereits verwendet! "
                "Zustand korrumpiert."
            )

        bits = self._message_to_bits(message)
        signature: List[bytes] = []
        for i, bit in enumerate(bits):
            signature.append(self._private_key[i][0] if bit == "0" else self._private_key[i][1])

        self.is_used = True
        return signature


def verify_lamport(
    public_key: List[Tuple[bytes, bytes]], message: bytes, signature: List[bytes]
) -> bool:
    """Prüft eine Lamport-Signatur gegen den öffentlichen Schlüssel."""
    if len(signature) != _BITS:
        return False

    bits = "".join(f"{byte:08b}" for byte in hashlib.sha256(message).digest())

    for i, bit in enumerate(bits):
        sig_part_hash = hashlib.sha256(signature[i]).digest()
        expected = public_key[i][0] if bit == "0" else public_key[i][1]
        if sig_part_hash != expected:
            return False
    return True


def run_demo_scenario() -> None:
    """
    Zeigt OTS-Wiederverwendung nach Wiederherstellung eines veralteten Zustands.

    Ablauf: eine gültige Signatur, dann Simulation „Backup/Restore“, bei dem
    der Verbrauchs-Zustand zurückgesetzt ist — zweite Signatur mit demselben
    Schlüsselmaterial wird möglich (Sicherheitsproblem).
    """
    print("=== Didaktische Demo: Lamport OTS und Zustandsrisiko ===")

    signer = LamportOTS()
    msg1 = b"Originale Nachricht A"
    print(f"\n[1] Signiere: '{msg1.decode()}'")
    signer.sign(msg1)
    print("    -> Signatur erstellt; OTS-Zustand: verbraucht (is_used=True).")

    print("\n[2] Wiederherstellung: veraltetes Backup wird eingespielt.")
    print("    Der gespeicherte Zustand kennt die Signatur noch nicht — is_used=False.")
    restored = copy.deepcopy(signer)
    restored.is_used = False

    msg2 = b"Gefaelschte Nachricht B"
    print(f"\n[3] Zweite Signatur mit demselben Schlüsselmaterial: '{msg2.decode()}'")
    restored.sign(msg2)
    print("    !!! KRITISCH: Eine zweite Signatur war möglich (OTS-Wiederverwendung).")
    print(
        "    In der Praxis entspricht das u. a. veraltetem Zählerstand / falschem "
        "Backup — bei XMSS wäre die betroffene OTS-Einheit erneut genutzt."
    )


if __name__ == "__main__":
    run_demo_scenario()
