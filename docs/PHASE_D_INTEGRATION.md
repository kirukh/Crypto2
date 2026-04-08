# Phase D — Integration: Theorie, Fallbeispiele und Demo verzahnen

**Ziel (laut Projektplan, 6 h):** Inhaltliche **Roter Faden** von der **Norm/Theorie** (XMSS, Zustand, SP 800-208, RFC 8391) zu **operativen Risiken** (Backup, Zähler) und zur **Demonstration im Code** — inklusive **klarer Grenzen** des Demonstrators. Dieses Dokument dient als **Integrationsleitfaden** für die **schriftliche Ausarbeitung** (max. 10 Seiten bei Code) und als Vorlage für die **Präsentation** (Phase E).

---

## 1. Roter Faden (eine durchgängige Storyline)

Die Arbeit soll beim Leser nicht drei getrennte Blöcke („Theorie“, „Risiko“, „Python“) hinterlassen, sondern **eine Kette**:

1. **Problemstellung:** Post-Quantum-Signaturen; hashbasierte **stateful** Verfahren (Fokus **XMSS**) verlangen **Zustandsführung** (Index / verbrauchte OTS-Einheiten) — siehe Phase A/B, Normen.
2. **Fachliche Basis:** OTS + Merkle-Baum → **RFC 8391**; **SP 800-208** betont **Zustandsdisziplin** als Sicherheitsvoraussetzung.
3. **Übergang zur Praxis:** Wo der gespeicherte Zustand **hinter** der Realität zurückbleibt (Backup, Restore, Klonen), entsteht das **Risiko der Wiederverwendung** von OTS-Material — inhaltlich aus Phase B, Kapitel 5.
4. **Illustration:** Das Repository enthält eine **Lamport-OTS**-Demo: Ein Schlüssel darf nur **einmal** signieren; nach simulierter **Wiederherstellung** eines „unbenutzt“-Zustands wird eine **zweite Signatur** möglich — dasselbe **prinzipielle** Dilemma wie veralteter Index bei XMSS, ohne Merkle/XMSS zu implementieren (Phase C).
5. **Grenze:** Was die Demo **nicht** leistet (kein Merkle, kein Multi-OTS-XMSS, kein Leistungsvergleich mit ML-DSA) — Abschnitt 4 unten.

Diese fünf Schritte lassen sich in der **Einleitung** andeuten und im **Fazit** wieder aufgreifen.

---

## 2. Zuordnung: Begriff → Theorie → Demo

| Begriff / Thema | Wo in der Arbeit (Material) | Rolle des Codes (`stateful_signatures`) |
|-----------------|----------------------------|-------------------------------------------|
| Zustand / keine OTS-Wiederverwendung | Phase B, Kapitel 3–4; Normen | Nach `sign()` ist `is_used=True`; zweiter Aufruf auf demselben Objekt schlägt fehl. |
| Backup / veralteter Zustand | Phase B, Kapitel 5 | `copy.deepcopy(signer)` + `is_used=False` modelliert Wiederherstellung, die den Verbrauch „vergisst“. |
| Verifikation | Phase B; Lamport-Kontext | `verify_lamport` prüft Hash-Konsistenz pro Bit. |
| XMSS, WOTS+, Merkle, mehrere OTS | Phase A/B, **nur Text** | **Nicht** im Code; Demo = **eine** Lamport-Instanz als kleinste OTS-Einheit. |
| Benchmark | Phase C | Misst **nur** Lamport Sign/Verify; **kein** XMSS-Throughput. |

Damit ist **Meilenstein M4** inhaltlich erfüllbar: Demo und Benchmark sind **mit der Theorie verzahnt**, nicht nur „Anhang mit Listing“.

---

## 3. Kurztext für die Ausarbeitung (Integrationsabschnitt, stark kürzbar)

*Zum Einfügen oder Umschreiben — auf ½–1 Seite in der End-PDF strecken oder auf 2–3 Absätze kürzen.*

Die bisherigen Kapitel haben **XMSS** und **SP 800-208** / **RFC 8391** als fachliche Grundlage beschrieben und operative Risiken benannt, die entstehen, wenn der **persistierte Signaturzustand** nicht zum tatsächlichen Gebrauch passt. Um das **organisatorisch-kryptographische** Spannungsfeld **anschaulich** zu machen — ohne eine Referenz-XMSS-Implementierung — enthält das begleitende Repository eine **didaktische Lamport One-Time Signature**: Der private Signaturzustand wird nach einer Signatur als **verbraucht** markiert; wird derselbe Schlüssel nach einer **Wiederherstellung** fälschlich wieder als **frei** geführt, kann eine **weitere Signatur** erzeugt werden — **OTS-Wiederverwendung**. Das **Abgrenzung:** Dies ist **kein** XMSS (kein Merkle-Baum, keine WOTS+, keine RFC-8391-Konformität); die Lamport-Implementierung dient der **Veranschaulichung** des Zustands- und Backup-Problems. Ein **Micro-Benchmark** misst Sign- und Verify-Laufzeiten **in diesem Demo** und dient höchstens der Groborientierung, nicht einem Vergleich mit standardisierten PQC-Verfahren.

---

## 4. Grenzen explizit benennen (Checkliste für die PDF)

In der Ausarbeitung mindestens **ein** zusammenhängender Absatz oder eine kurze Liste:

- [ ] **Kein XMSS:** kein WOTS+, kein Merkle-Baum, keine RFC-8391-Konformität; nur **eine** Lamport-OTS-Instanz.
- [ ] **Lehrcode:** keine Produktionsreife, kein Sicherheitsaudit; didaktische OTS-Logik, **kein** Ersatz für die Theorie in Norm und Literatur.
- [ ] **Benchmark:** keine Übertragbarkeit auf XMSS/ML-DSA/SLH-DSA; keine Aussage „PQC ist schnell/langsam“ aus diesem Projekt allein.
- [ ] **Produktion:** kein HSM, keine Side-Channel-Härtung, kein Einsatz für echte Geheimnisse.

---

## 5. Präsentation (Phase E) — Anknüpfungspunkte

| Folie / Block | Inhalt |
|---------------|--------|
| Problem | Stateful braucht zuverlässigen Zähler/Index bzw. verbrauchte OTS (1–2 Stichpunkte + Norm). |
| Risiko | Backup/Restore kann Zustand zurücksetzen → Wiederverwendung (qualitativ). |
| Demo | Terminal-Screenshot oder Live: `python -m stateful_signatures` — **einen Satz** „Lamport-OTS als Miniaturmodell, kein XMSS“. |
| Grenze | Ein Satz: nicht XMSS, nur Illustration. |
| Fazit | Zentraler Signaturdienst / klare Backup-Politik als Richtung (aus Phase B, Kapitel 6). |

---

## 6. Bezug zu anderen Phasen

| Phase | Dokument | Beitrag zur Integration |
|-------|----------|---------------------------|
| A | [PHASE_A_EINLEITUNG_UND_RECHERCHE.md](PHASE_A_EINLEITUNG_UND_RECHERCHE.md) | Einleitung, Norm-Kurzüberblick |
| B | [PHASE_B_THEORIE.md](PHASE_B_THEORIE.md) | Tiefe Theorie, Risiken, Lösungskapitel |
| C | [PHASE_C_TECHNIK.md](PHASE_C_TECHNIK.md) | Technische Fakten zu Demo/Benchmark |
| D | *dieses Dokument* | **Verbindung** der Teile |

---

## 7. Nächste Schritte (Phase E — Präsentation)

- Folien nach Tabelle in Abschnitt 5 skizzieren; **eine** klare Demo-Szene einplanen.
- **Phase F** (Finalisierung): Literaturverzeichnis, Layout, Seitenzahl prüfen (**10 Seiten** bei Code).
