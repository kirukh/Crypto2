# Phase C — Technik: Demo, Benchmark, Textbausteine für die Ausarbeitung

**Ziel (laut Projektplan):** Demo und Benchmark **pflegen**, Ergebnisse **einordnen**, in der **kurzen** schriftlichen Dokumentation (max. **10 Seiten** bei Code) nur das Nötige beschreiben. Dieses Dokument ist die **Arbeitsgrundlage** für Phase C; die **Integration** Theorie ↔ Code ist Phase D.

---

## 1. Software-Stack

| Komponente | Version / Hinweis |
|------------|-------------------|
| Python | 3.10+ (im Projekt getestet: siehe eigene Umgebung) |
| Paket | `stateful_signatures` (editable: `pip install -e ".[dev]"`) |
| Demo | Nur **Standardbibliothek** (`hmac`, `hashlib`) |
| Tests / Benchmark | `pytest`, `pytest-benchmark` (nur Entwicklungsabhängigkeiten) |

---

## 2. Architektur des Codes (Überblick)

```
src/stateful_signatures/
├── __init__.py
├── __main__.py          # Einstieg: python -m stateful_signatures
├── demo.py              # CLI (Hilfe, ruft Szenario auf)
└── stateful_demo.py     # Modell: StatefulSigner, verify, run_demo_scenario
tests/
├── test_stateful_demo.py
└── test_benchmark_stateful.py
```

**Abgrenzung:** `stateful_demo.py` implementiert **kein** XMSS, **keinen** Merkle-Baum, **keine** WOTS+ nach RFC 8391. Es ist ein **Lehr-Modell**: geheimer Schlüssel + **monotoner Index**, Signatur = HMAC-SHA256 über Nachricht und Index. So lassen sich **Zustand** und **Wiederherstellung eines älteren Index** demonstrieren, ohne die Komplexität einer Referenz-XMSS-Implementierung.

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

1. Mehrere Signaturen mit fortschreitendem **Index**.
2. Gültige Verifikation einer weiteren Signatur.
3. **Simulierte Wiederherstellung** eines **älteren** Zustands (`index = 2`), obwohl der „echte“ Signaturgegenstand schon weiter war — neue Signatur mit einem Index, der in der Realität **bereits durch höhere Indizes überholt** war (illustrativ für Backup/Restore-Probleme; in echten OTS/XMSS wäre die Kollisions-/Reuse-Problematik Sicherheitskern).

### 3.3 Für Präsentation / Video

Terminal mit großer Schrift, oder Ausgabe in Datei umleiten (`> demo.txt`). Kurz **mündlich** einordnen: Modell vs. XMSS aus der Theorie.

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
| `test_benchmark_sign` | `StatefulSigner.sign` mit fester Nachricht |
| `test_benchmark_verify` | `verify` mit fester Nachricht und vorher erzeugter Signatur |

**Ausgabe:** pytest-benchmark liefert u. a. **Min / Max / Mean / Median**, **Rounds**, **OPS** (Operationen pro Sekunde, reziprok zum Mittelwert). Die absoluten Zahlen hängen von **CPU, Last, Python-Version** ab.

### 4.3 Einordnung (wichtig für die Arbeit)

- Der Benchmark misst **nur** die Geschwindigkeit des **didaktischen HMAC-Modells**.
- **Kein** Rückschluss auf XMSS-Leistung, **kein** Vergleich mit ML-DSA/SLH-DSA ohne separate, sauber parametrisierte Messung — das war in Phase A/B bereits konzeptionell begründet.
- Sinnvolle Nutzung: **Kurz** in der Ausarbeitung („wir haben Sign/Verify im Demo-Modell gemessen; Größenordnung µs auf Referenzrechner X“) — oder **ein** Satz, dass Messwerte **reproduzierbar** mit `benchmark_results.json` und genannter Umgebung sind.

---

## 5. Kurztext für die schriftliche Dokumentation (Baustein, ≤ 1 Seite)

*Die folgenden Absätze kannst du straffen und für die 10-Seiten-PDF kürzen.*

**Implementierung.** Im Repository liegt ein Python-Paket `stateful_signatures`. Es enthält ein **Lehr-Modell** zustandsbehafteten Signierens: Ein geheimer Schlüssel und ein fortlaufender **Index** werden beim Signieren verwendet; die „Signatur“ ist ein HMAC-SHA256 über die Nachricht und den Index. Es handelt sich **nicht** um eine Implementierung von XMSS gemäß RFC 8391 und **nicht** um eine normkonforme OTS — die theoretische Einordnung von XMSS, WOTS+ und SP 800-208 erfolgt ausschließlich im **theoretischen Teil**.

**Demonstration.** Die Konsolenanwendung führt ein kurzes **Szenario** aus: mehrere Signaturen, anschließend die Simulation einer **Wiederherstellung eines älteren Zählerstands**, um das Risiko inkonsistenter Backups zu veranschaulichen.

**Benchmark.** Mit `pytest-benchmark` wurden die Operationen **Sign** und **Verify** im Demo-Modell auf dem verwendeten Rechner gemessen. Die Werte dienen der **Illustration der Rechenkosten** dieses minimalen Modells; sie ersetzen **keine** Aussage über produktive XMSS- oder PQC-Verfahren.

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
