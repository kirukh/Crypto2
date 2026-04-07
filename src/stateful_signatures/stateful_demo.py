"""
Lehr-Demo: zustandsbehaftetes Signieren mit Monotonie des Index.

Das ist bewusst kein XMSS (kein Merkle, keine echten OTS nach RFC 8391), sondern
ein minimales Modell: jede Signatur ist an einen Index gebunden; der geheime
Schlüssel zählt vorwärts. So lassen sich Zustand, Backup und Wiederverwendung
des gleichen Index anschaulich machen — passend zur schriftlichen Ausarbeitung.
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


@dataclass(frozen=True)
class Signature:
    """Signatur: Index (Zustand zum Signierzeitpunkt) + MAC über Nachricht und Index."""

    index: int
    tag: bytes


class StatefulSigner:
    """Hält einen geheimen Schlüssel und einen fortlaufenden Signaturindex."""

    def __init__(self, secret: bytes) -> None:
        if len(secret) < 16:
            raise ValueError("Geheimer Schlüssel sollte mindestens 16 Byte haben.")
        self._secret = secret
        self.index = 0

    def sign(self, message: bytes) -> Signature:
        idx = self.index
        payload = message + idx.to_bytes(8, "big", signed=False)
        tag = hmac.new(self._secret, payload, hashlib.sha256).digest()
        self.index += 1
        return Signature(index=idx, tag=tag)

    def export_state(self) -> tuple[bytes, int]:
        """Für Demo: Zustand sichern (Schlüssel + Index). In der Praxis: nur index/sicher speichern."""
        return self._secret, self.index

    @classmethod
    def from_state(cls, secret: bytes, index: int) -> StatefulSigner:
        s = cls(secret)
        s.index = index
        return s


def verify(secret: bytes, message: bytes, sig: Signature) -> bool:
    payload = message + sig.index.to_bytes(8, "big", signed=False)
    expected = hmac.new(secret, payload, hashlib.sha256).digest()
    return hmac.compare_digest(expected, sig.tag)


def run_demo_scenario() -> None:
    """Gibt eine kurze Szenario-Ausgabe auf stdout (z. B. für Präsentation / CLI)."""
    secret = b"demo-secret-key-min-16b!!"
    signer = StatefulSigner(secret)

    msg = b"Vertrag Nr. 42"
    for _ in range(3):
        signer.sign(msg)

    print("Didaktische Demo: zustandsbehaftete Signatur (Modell, kein XMSS)\n")
    print(f"Nach drei Signaturen (gleiche Nachricht): aktueller Index = {signer.index}")

    last_msg = "Letzte gültige Nachricht".encode("utf-8")
    sig_ok = signer.sign(last_msg)
    print(f"Neue Signatur: index={sig_ok.index}, verifiziert: {verify(secret, last_msg, sig_ok)}")

    # Simuliertes altes Backup: Index steht weiter hinten als ein wiederhergestellter Stand
    stale = StatefulSigner.from_state(secret, index=2)
    sig_reuse = stale.sign(b"Nach Restore")
    print(
        f"\nNach 'Wiederherstellung' eines älteren Zustands (Index={stale.index - 1}): "
        f"neue Signatur index={sig_reuse.index}"
    )
    print(
        "Hinweis: In echten OTS/XMSS würde ein erneutes Signieren mit einem "
        "bereits verbrauchten Index die Sicherheit brechen — hier nur Illustration des Zählerproblems."
    )
