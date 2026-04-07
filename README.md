# Stateful Signatures & Zustandsmanagement (Seminarprojekt)

**Neues, eigenständiges Projekt** — ohne Bezug zu älteren Repositorien oder fremdem Quellcode.

## Thema (Abstimmung mit der Betreuung)

- Überblick über **Signaturverfahren** (klassisch, PQC stateless, PQC stateful).
- **Konzeptionelle Tiefe:** stateful hashbasierte Signaturen (**XMSS**; Kontext u. a. NIST SP 800-208, RFC 8391): strenges **Zustandsmonitoring**.
- **Risiken und Praxis:** **Backups**, **Wiederherstellung**, **Verlust/Desynchronisation** des Signaturzählers — und diskutierte **Lösungsrichtungen** (z. B. zentrale Signatur, HSM, Alternativen; Grenzen eines studentischen Demonstrators).

Umfang: **ca. 60 Stunden** inklusive **schriftlicher Ausarbeitung** und **Präsentation**.

### Abgabevorgaben (festgehalten)

- **Präsentation:** Pflichtbestandteil der Abgabe.
- **Schriftliche Ausarbeitung / Dokumentation:** Enthält das Projekt **Code**, gilt eine **Obergrenze von 10 Seiten** für diese Dokumentation (Vorgabe der Betreuung/Hochschule — bei Unklarheit Format/Zählung dort abklären).

---

## Dokumentation

| Pfad | Inhalt |
|------|--------|
| **[docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)** | Zeitplan, Ordnerstruktur, Meilensteine, **Schritt-für-Schritt**-Vorgehen |
| **[docs/PHASE_A_EINLEITUNG_UND_RECHERCHE.md](docs/PHASE_A_EINLEITUNG_UND_RECHERCHE.md)** | Phase A: **Einleitung**, Kernpunkte **SP 800-208** / **RFC 8391**, OTS, Vergleich stateless/stateful |
| **[docs/OUTLINE.md](docs/OUTLINE.md)** | **Kapitelgliederung** (Entwurf) |
| **[docs/PHASE_B_THEORIE.md](docs/PHASE_B_THEORIE.md)** | Phase B: **Theorie** nach Gliederung (Signaturen/PQC, OTS/Merkle/XMSS, Zustand, Risiken, Lösungen, Fazit) |
| **[docs/PHASE_C_TECHNIK.md](docs/PHASE_C_TECHNIK.md)** | Phase C: **Demo**, **Benchmark**, Textbausteine und Einordnung für die Ausarbeitung |
| **[docs/PHASE_D_INTEGRATION.md](docs/PHASE_D_INTEGRATION.md)** | Phase D: **Integration** — Roter Faden Theorie ↔ Demo, Grenzen, Textbaustein für die PDF, Folien-Anker |
| **literature/sources.bib** | Starter-BibTeX (Normen, RFC, FIPS) |
| **presentation/** | Folien (Quelle + exportiertes PDF) |
| **literature/** | Eigene Notizen, Literaturliste/BibTeX — **keine** urheberrechtlich geschützten Volltexte ins Repository legen |

---

## Technik (Python-Demo + Benchmark)

Das Repository enthält eine **didaktische Referenzimplementierung** (kein vollständiges XMSS nach RFC 8391): ein **Modell** mit geheimem Schlüssel und **monotonem Signaturindex**, um Zustand, Verifikation und das Problem von **Backup/Restore** zu veranschaulichen. XMSS, Normen und echte Sicherheitseigenschaften bleiben in der **schriftlichen Ausarbeitung**; der Code ist als **Lehr-/Demonstrationscode** gekennzeichnet.

**Voraussetzungen:** Python **3.10+**

```text
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

**Demo (Konsolenausgabe):**

```text
python -m stateful_signatures
```

Hilfe: `python -m stateful_signatures --help`. Oder: `stateful-demo` (nach Installation; ggf. `Scripts`-Pfad beachten).

Details und **Benchmark-JSON-Export** siehe **[docs/PHASE_C_TECHNIK.md](docs/PHASE_C_TECHNIK.md)**.

**Tests:** Unter Windows ist `pytest` oft nicht im `PATH`; zuverlässig funktioniert **`python -m pytest`** (nutzt dieselbe Python-Installation wie `pip` — virtuelle Umgebung vorher aktivieren).

```text
python -m pytest tests/ -v
```

Ohne Benchmark-Statistik (schneller): `python -m pytest tests/ --benchmark-disable`

**Benchmark (pytest-benchmark):** misst Laufzeit von Signatur und Verifikation im Demo-Modell.

```text
python -m pytest tests/test_benchmark_stateful.py --benchmark-only
```

Optional Ergebnisse speichern: `python -m pytest tests/test_benchmark_stateful.py --benchmark-only --benchmark-json=benchmark_results.json`

Projektstruktur siehe `docs/PROJECT_PLAN.md` (Abschnitt Ordnerstruktur).

---

## Erste Schritte

1. `docs/PROJECT_PLAN.md` lesen und abarbeiten.
2. Virtuelle Umgebung anlegen, `pip install -e ".[dev]"` (siehe oben).
3. Literatur sammeln, Gliederung der Arbeit schreiben (`docs/`).
4. Theorie und Code (Demo/Benchmark) in der Ausarbeitung kurz und klar verknüpfen (**max. 10 Seiten** bei Code).

---

## Hinweis

Ältere Projektordner auf dem Rechner kannst du archivieren oder ignorieren — dieses Verzeichnis ist **bewusst unabhängig** neu aufgesetzt.
