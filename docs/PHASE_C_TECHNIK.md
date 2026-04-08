# Phase C — Technik: Demo, Benchmark, Textbausteine für die Ausarbeitung

**Ziel (laut Projektplan):** Demo und Benchmark **pflegen**, Ergebnisse **einordnen**, in der **kurzen** schriftlichen Dokumentation (max. **10 Seiten** bei Code) nur das Nötige beschreiben. Dieses Dokument ist die **Arbeitsgrundlage** für Phase C; die **Integration** Theorie ↔ Code ist Phase D.

---

## 1. Software-Stack

| Komponente | Version / Hinweis |
|------------|-------------------|
| Python | 3.10+ (im Projekt getestet: siehe eigene Umgebung) |
| Paket | `stateful_signatures` (editable: `pip install -e ".[dev]"`) |
| Demo | Nur **Standardbibliothek** (`hashlib`, `os`, `copy`) |
| Tests / Benchmark | `pytest`, `pytest-benchmark` (nur Entwicklungsabhängigkeiten) |

---

## 2. Architektur des Codes (Überblick)

```
src/stateful_signatures/
├── __init__.py
├── __main__.py          # Einstieg: python -m stateful_signatures
├── demo.py              # CLI (Hilfe, ruft Szenario auf)
└── stateful_demo.py     # LamportOTS, verify_lamport, run_demo_scenario
tests/
├── test_stateful_demo.py
├── test_demo_cli.py
└── test_benchmark_stateful.py
```

**Abgrenzung:** `stateful_demo.py` implementiert **kein** XMSS, **keinen** Merkle-Baum, **keine** WOTS+ nach RFC 8391. Es enthält eine **didaktische Lamport One-Time Signature (OTS)** über SHA-256 (256 Bit Nachrichtenhash → 256 Geheimnisteile). Der **Zustand** ist `is_used`: nach einer Signatur ist der Schlüssel verbraucht. Ein Szenario simuliert **Wiederherstellung** eines Zustands, in dem „noch nicht signiert“ gilt — **OTS-Wiederverwendung** — und damit das gleiche **operative Risiko** wie veralteter Index/Backup bei XMSS (in der **Ausarbeitung** mit der Norm verknüpfen).

---

## 3. Konsolen-Demo

### 3.1 Aufruf

```text
python -m stateful_signatures
```

Hilfe (Optionen der Standardbibliothek):

```text
python -m stateful_signatures --help
```

### 3.2 Was das Szenario zeigt

1. Eine **erste Signatur** mit frischem Lamport-OTS (Zustand wechselt auf „verbraucht“).
2. **Wiederherstellung** eines Zustands, in dem der OTS noch als **unbenutzt** gilt (`is_used=False`), obwohl bereits signiert wurde — analog zu veraltetem Backup / fehlendem Zählerstand.
3. Eine **zweite Signatur** mit demselben Schlüsselmaterial wird möglich: **OTS-Wiederverwendung** (im echten XMSS-Kontext: gleiche Index-Position erneut — Sicherheitsproblem).

### 3.3 Für Präsentation / Video

Terminal mit großer Schrift, oder Ausgabe in Datei umleiten (`> demo.txt`). Kurz **mündlich** einordnen: Lamport-OTS als **kleinste** Einheit; XMSS in der Theorie = viele OTS + Merkle + Index; Demo **illustriert** nur Zustand und Reuse.

---

## 4. Benchmark

### 4.1 Befehle

Alle Tests (ohne Benchmark-Statistik, schneller):

```text
python -m pytest tests/ --benchmark-disable -v
```

Nur Micro-Benchmarks (Sign / Verify im Demo-Modell):

```text
python -m pytest tests/test_benchmark_stateful.py --benchmark-only -v
```

**Ergebnisse als JSON** (z. B. für Archiv oder spätere Grafik — optional):

```text
python -m pytest tests/test_benchmark_stateful.py --benchmark-only --benchmark-json=benchmark_results.json
```

Die Datei `benchmark_results.json` kann ins Repository **oder nur lokal** gelegt werden (bei Abgabe klären, ob Messwerte festgehalten werden sollen).

### 4.2 Was gemessen wird

| Test | Operation |
|------|-----------|
| `test_benchmark_sign` | `LamportOTS.sign` mit fester Nachricht (neuer Signer pro Runde wegen Zustand) |
| `test_benchmark_verify` | `verify_lamport` mit fester Nachricht und vorher erzeugter Signatur |

**Ausgabe:** pytest-benchmark liefert u. a. **Min / Max / Mean / Median**, **Rounds**, **OPS** (Operationen pro Sekunde, reziprok zum Mittelwert). Die absoluten Zahlen hängen von **CPU, Last, Python-Version** ab.

### 4.3 Einordnung (wichtig für die Arbeit)

- Der Benchmark misst **nur** die Geschwindigkeit der **didaktischen Lamport-OTS** (KeyGen + Sign bzw. Verify).
- **Kein** Rückschluss auf XMSS-Leistung, **kein** Vergleich mit ML-DSA/SLH-DSA ohne separate, sauber parametrisierte Messung — das war in Phase A/B bereits konzeptionell begründet.
- Sinnvolle Nutzung: **Kurz** in der Ausarbeitung („wir haben Sign/Verify im Demo gemessen; Größenordnung … auf Referenzrechner X“) — oder **ein** Satz, dass Messwerte **reproduzierbar** mit `benchmark_results.json` und genannter Umgebung sind.

---

## 5. Kurztext für die schriftliche Dokumentation (Baustein, ≤ 1 Seite)

*Die folgenden Absätze kannst du straffen und für die 10-Seiten-PDF kürzen.*

**Implementierung.** Im Repository liegt ein Python-Paket `stateful_signatures`. Es enthält eine **didaktische Lamport-OTS**: 256 Bit-Blöcke aus dem privaten Schlüssel werden je nach gehashtem Nachrichtenbit offengelegt; nach einer Signatur ist der Schlüssel **verbraucht** (`is_used`). Es handelt sich **nicht** um XMSS gemäß RFC 8391 (kein Merkle, kein Index über viele OTS) — die theoretische Einordnung von XMSS, WOTS+ und SP 800-208 erfolgt im **theoretischen Teil**.

**Demonstration.** Die Konsole führt ein Szenario aus: Signatur, dann **Wiederherstellung** eines Zustands ohne Kenntnis des Verbrauchs — **zweite Signatur** mit demselben Material. Das illustriert **OTS-Wiederverwendung** und das Backup-/Zählerproblem qualitativ.

**Benchmark.** Mit `pytest-benchmark` wurden **Sign** und **Verify** im Demo gemessen. Die Werte dienen der **Illustration der Rechenkosten** dieser minimalen OTS; sie ersetzen **keine** Aussage über produktives XMSS oder andere PQC-Verfahren.

---

## 6. Reproduzierbarkeit (Checkliste)

- [ ] `python --version` notieren  
- [ ] Betriebssystem und Rechnermodell (optional)  
- [ ] Commit-Hash des Repositories (wenn eingecheckt)  
- [ ] Bei JSON-Export: `benchmark_results.json` mit Datum versehen  

---

## 7. Meilenstein M4 (Projektplan)

| Kriterium | Erfüllt durch |
|-----------|----------------|
| Demo beschrieben und ausführbar | Abschnitt 3, Code `run_demo_scenario` |
| Benchmark beschrieben | Abschnitt 4 |
| Theorie ↔ Demo verzahnt | Kurztext Abschnitt 5; **vertiefte** Verzahnung: **Phase D** |

---

## Nächste Schritte (Phase D / E)

- **Phase D:** **[PHASE_D_INTEGRATION.md](PHASE_D_INTEGRATION.md)** — Roter Faden, Integrationsabsatz, Grenzen, Präsentations-Anker.
- **Phase E:** Folien; **10-Seiten-Limit** bei der PDF weiter beachten; Details ggf. in der Präsentation.
