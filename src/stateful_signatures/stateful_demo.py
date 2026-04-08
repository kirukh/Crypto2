import os
import hashlib
from typing import List, Tuple

class LamportOTS:
    """
    Didaktische Implementierung einer Lamport One-Time Signature (OTS).
    Achtung: Nur für Lehrzwecke! Nicht side-channel-gehärtet.
    """
    def __init__(self):
        # 1. Schlüsselgenerierung: 256 Paare aus 32-Byte Zufallswerten
        self._private_key: List[Tuple[bytes, bytes]] = []
        self.public_key: List[Tuple[bytes, bytes]] = []
        self.is_used = False  # Unser entscheidender Zustand!

        for _ in range(256):
            # Zwei geheime 32-Byte Strings pro Bit
            sk_0 = os.urandom(32)
            sk_1 = os.urandom(32)
            self._private_key.append((sk_0, sk_1))
            
            # Der öffentliche Schlüssel besteht aus den Hashes dieser Geheimnisse
            pk_0 = hashlib.sha256(sk_0).digest()
            pk_1 = hashlib.sha256(sk_1).digest()
            self.public_key.append((pk_0, pk_1))

    def _hash_message_to_bits(self, message: bytes) -> str:
        """Hilfsfunktion: Hasht die Nachricht und gibt sie als 256-stelligen Bit-String zurück."""
        msg_hash = hashlib.sha256(message).digest()
        # Wandle jedes Byte in 8 Bits um (z.B. '01001101')
        return ''.join(f'{byte:08b}' for byte in msg_hash)

    def sign(self, message: bytes) -> List[bytes]:
        """Signiert die Nachricht und konsumiert den OTS-Zustand."""
        if self.is_used:
            # Hier greift unser operatives Risiko!
            raise RuntimeError("SECURITY BREACH: Dieser OTS-Schlüssel wurde bereits verwendet! Zustand korrumpiert.")
        
        bits = self._hash_message_to_bits(message)
        signature = []

        # Wähle für jedes Bit den passenden Teil des privaten Schlüssels
        for i, bit in enumerate(bits):
            if bit == '0':
                signature.append(self._private_key[i][0])
            else:
                signature.append(self._private_key[i][1])
                
        # ZUSTAND AKTUALISIEREN (Atomarität in der Praxis extrem wichtig!)
        self.is_used = True 
        
        return signature

def verify_lamport(public_key: List[Tuple[bytes, bytes]], message: bytes, signature: List[bytes]) -> bool:
    """Verifiziert die Signatur gegen den öffentlichen Schlüssel."""
    if len(signature) != 256:
        return False
        
    msg_hash = hashlib.sha256(message).digest()
    bits = ''.join(f'{byte:08b}' for byte in msg_hash)

    # Prüfe für jedes Bit, ob der Hash der Signatur zum öffentlichen Schlüssel passt
    for i, bit in enumerate(bits):
        sig_part_hash = hashlib.sha256(signature[i]).digest()
        
        if bit == '0':
            expected_hash = public_key[i][0]
        else:
            expected_hash = public_key[i][1]
            
        if sig_part_hash != expected_hash:
            return False
            
    return True

def run_demo_scenario():
    """Simuliert das operative Risiko: Key-Reuse durch Backup-Restore."""
    print("--- DIDAKTISCHE DEMO: LAMPORT OTS & ZUSTANDSRISIKO ---")
    
    # 1. Normaler Ablauf
    signer = LamportOTS()
    msg1 = b"Originale Nachricht A"
    print(f"\n[1] Signiere: '{msg1.decode()}'")
    sig1 = signer.sign(msg1)
    print("    -> Signatur 1 erstellt.")

    # 2. Backup-Simulation (Zustandsverlust)
    print("\n[2] SIMULATION: Ein Backup wird eingespielt.")
    print("    Der interne Zustand 'is_used' wird auf False zurückgesetzt.")
    
    # Wir 'klonen' den Signierer, um ein Backup zu simulieren
    backup_signer = LamportOTS()
    backup_signer._private_key = signer._private_key
    backup_signer.public_key = signer.public_key
    backup_signer.is_used = False # Der Fehler: Das System 'vergisst', dass schon signiert wurde
    
    # 3. Sicherheitsbruch
    msg2 = b"Gefaelschte Nachricht B"
    print(f"\n[3] Versuche zweite Signatur mit gleichem Key: '{msg2.decode()}'")
    
    # Hier zeigen wir, wie das System im Normalfall reagieren würde
    try:
        sig2 = backup_signer.sign(msg2)
        print("    !!! KRITISCHER FEHLER: Zweite Signatur wurde trotz Key-Reuse erstellt.")
        print("    Ein Angreifer kann nun Teile des privaten Schlüssels kombinieren!")
    except RuntimeError as e:
        print(f"    Schutzmechanismus aktiv: {e}")
        
# --- Testlauf für deine CLI / Demo ---
if __name__ == "__main__":
    print("--- Generiere Lamport OTS Schlüsselpaar ---")
    signer = LamportOTS()
    
    msg1 = b"Meine erste sichere Nachricht"
    print(f"\nSigniere: '{msg1.decode()}'")
    sig1 = signer.sign(msg1)
    
    is_valid = verify_lamport(signer.public_key, msg1, sig1)
    print(f"Verifikation erfolgreich? {is_valid}")
    
    print("\n--- Simuliere Backup/Zähler-Desynchronisation (erneuter Signaturversuch) ---")
    msg2 = b"Angreifer-Nachricht nach Backup-Restore"
    try:
        sig2 = signer.sign(msg2)
    except RuntimeError as e:
        print(f"Erwarteter Fehler abgefangen: {e}")