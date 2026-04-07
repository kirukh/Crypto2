# Projektplan: Signaturverfahren & Zustand bei stateful Schemes (XMSS)

**Eigenständiges Projekt** — kein technischer oder inhaltlicher Bezug zu früheren Repositorien.

**Umfang:** ca. **60 Stunden** (inkl. Dokumentation und Präsentation).

---

## 1. Ziele (Abgabe)

| Ergebnis | Beschreibung |
|----------|----------------|
| **Schriftliche Arbeit** | Einordnung der Signaturfamilien; Fokus **stateful** (XMSS): Zustand, SP 800-208 / RFC 8391; operative Risiken (**Backup**, **Zähler**); Lösungsansätze und Grenzen. |
| **Präsentation** | Nachvollziehbare Storyline mit mind. einem **konkreten Szenario** (z. B. OTS-Wiederverwendung nach Restore — später ggf. durch Demo illustriert). |
| **Technik (optional)** | Nur wenn du willst: kleiner Demonstrator (Sprache/Bibliothek **selbst wählen**); in der Arbeit klar als **Lehr-/Demonstrationsimplementierung** kennzeichnen. |

---

## 2. Ordnerstruktur (dieses Repository)

```
Stateful-Signatures-Project/
├── README.md
├── docs/
│   └── PROJECT_PLAN.md      # dieser Plan
├── presentation/            # Folien
├── literature/            # Notizen, BibTeX (keine geschützten PDFs committen)
├── src/                   # optional: spätere Implementierung (aktuell leer)
└── .gitignore
```

Erweiterungen (wenn du Technik einführst): `tests/`, `requirements.txt`, `pyproject.toml`, … — dokumentieren in `README.md`.

---

## 3. Zeitplan (60 h)

| Phase | Std. | Inhalt |
|-------|------|--------|
| **A. Recherche & Gliederung** | 10 | SP 800-208, RFC 8391 (Auszüge); OTS-Idee; Vergleich stateless vs. stateful PQC; Literaturliste; Kapitelentwurf. |
| **B. Theorie schreiben** | 14 | Signaturen-Überblick; XMSS & Zustand; Kapitel zu Backup/Zählerverlust und Lösungsideen. |
| **C. Technik (optional)** | 10 | Stack wählen; minimale Demo oder Messung; dokumentieren, was genau gezeigt wird. |
| **D. Integration** | 6 | Theorie ↔ Demo/Fallbeispiele verzahnen; Grenzen benennen. |
| **E. Präsentation** | 8 | Folien, Probevortrag. |
| **F. Ausarbeitung finalisieren** | 8 | Format, Quellen, Korrektur. |
| **G. Puffer** | 4 | Verzögerungen, Rückfragen Betreuung. |

---

## 4. Meilensteine

- [ ] **M1:** Gliederung steht; Kernquellen gesichtet (mind. SP 800-208, RFC 8391).
- [ ] **M2:** Erstfassung Kapitel „Stateful / XMSS / Zustand“.
- [ ] **M3:** Kapitel „Backup & Zähler“ mit klarem Bedrohungsbild.
- [ ] **M4:** Optional: Demo oder strukturiertes Gedankenexperiment dokumentiert.
- [ ] **M5:** Präsentation fertig; Probezeit eingehalten.
- [ ] **M6:** Finale Abgabe (PDF + Folien + Repo wie gefordert).

---

## 5. Schritt für Schritt — was du jetzt tun sollst

### Schritt 1 — Orientierung (Tag 1)

- Dieses Dokument und `README.md` lesen.
- In `literature/` eine Datei `notes.md` oder `sources.bib` anlegen und **erste Quellen** eintragen.

### Schritt 2 — Gliederung (Tag 2–3)

- In `docs/` eine Datei `OUTLINE.md` mit **4–7 Hauptkapiteln** (z. B. Einleitung, Signaturüberblick, Stateful/XMSS, Zustandsmanagement, Backups/Zähler, Lösungsansätze, Fazit).

### Schritt 3 — Theorie (Woche 2)

- Kapitel für Kapitel ausarbeiten; Abbildungen aus Normen/RFCs **mit Quellenangabe**.
- Kein Plagiat: eigene Formulierungen, Zitate kennzeichnen.

### Schritt 4 — Technik nur, wenn klar (ab Woche 2–3)

- **Entscheidung:** brauchst du Code, oder reicht ein **durchgerechnetes / erzähltes Szenario**?
- Wenn Code: minimales Ziel definieren (eine nachvollziehbare Illustration), Stack wählen, in `README.md` dokumentieren.

### Schritt 5 — Präsentation (letzte Woche vor Abgabe)

- Storyline: Problem → XMSS/Zustand → Backup-Falle → Lehren → offene Punkte.
- `presentation/` mit Quelldatei + exportiertem PDF.

### Schritt 6 — Abgabe

- PDF der Arbeit, PDF der Folien, ggf. Repository-Link nach Vorgabe der Hochschule.

---

## 6. Was du nicht leisten musst (Scope)

- Kein produktionsreifer HSM- oder Cloud-Entwurf.
- Keine neue Kryptographie erfinden.
- Kein Zwang zu einem bestimmten Programmiersprachen-Stack — **du** legst fest, ob und was implementiert wird.

---

## 7. Unabhängigkeit

Dieses Projekt ist **von Grund auf** gedacht: keine Übernahme fremder Projektstruktur, kein Mischen alter Repositorien. Alles, was du hier einfügst, dokumentierst du **in diesem Ordner** und in deiner Arbeit.
