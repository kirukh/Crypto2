# Phase D — Integration: Theorie, Fallbeispiele und Demo verzahnen

**Ziel (laut Projektplan, 6 h):** Inhaltliche **Roter Faden** von der **Norm/Theorie** (XMSS, Zustand, SP 800-208, RFC 8391) zu **operativen Risiken** (Backup, Zähler) und zur **Demonstration im Code** — inklusive **klarer Grenzen** des Demonstrators. Dieses Dokument dient als **Integrationsleitfaden** für die **schriftliche Ausarbeitung** (max. 10 Seiten bei Code) und als Vorlage für die **Präsentation** (Phase E).

---

## 1. Roter Faden (eine durchgängige Storyline)

Die Arbeit soll beim Leser nicht drei getrennte Blöcke („Theorie“, „Risiko“, „Python“) hinterlassen, sondern **eine Kette**:

1. **Problemstellung:** Post-Quantum-Signaturen; hashbasierte **stateful** Verfahren (Fokus **XMSS**) verlangen **Zustandsführung** (Index / verbrauchte OTS-Einheiten) — siehe Phase A/B, Normen.
2. **Fachliche Basis:** OTS + Merkle-Baum → **RFC 8391**; **SP 800-208** betont **Zustandsdisziplin** als Sicherheitsvoraussetzung.
3. **Übergang zur Praxis:** Wo der gespeicherte Zustand **hinter** der Realität zurückbleibt (Backup, Restore, Klonen), entsteht das **Risiko der Wiederverwendung** — inhaltlich aus Phase B, Kapitel 5.
4. **Illustration:** Das Repository enthält ein **absichtlich einfaches Modell** (HMAC + Index), das **dieses Zähler-/Restore-Dilemma** sichtbar macht — **ohne** XMSS zu implementieren (Phase C).
5. **Grenze:** Was die Demo **nicht** leistet (kein Merkle, keine OTS-Sicherheit, kein Leistungsvergleich mit XMSS/ML-DSA) — Abschnitt 4 unten.

Diese fünf Schritte lassen sich in der **Einleitung** andeuten und im **Fazit** wieder aufgreifen.

---

## 2. Zuordnung: Begriff → Theorie → Demo

| Begriff / Thema | Wo in der Arbeit (Material) | Rolle des Codes (`stateful_signatures`) |
|-----------------|----------------------------|-------------------------------------------|
| Zustand / Index muss monoton | Phase B, Kapitel 3–4; Normen A | Signer erhöht `index` nach jedem `sign`. |
| Backup älter als aktueller Stand | Phase B, Kapitel 5 | `from_state(..., index=2)` nach vorherigen Signaturen — **älterer** Index wird erneut verwendet. |
| Verifikation bindet Index | Phase B, Kapitel 3–4; RFC-Kontext | `verify` nutzt `sig.index` in der MAC-Berechnung. |
| XMSS, WOTS+, Merkle | Phase A/B, **nur Text** | **Nicht** im Code; Demo explizit als Modell bezeichnen. |
| Benchmark | Phase C | Misst **nur** HMAC-Sign/Verify; **kein** XMSS-Throughput. |

Damit ist **Meilenstein M4** inhaltlich erfüllbar: Demo und Benchmark sind **mit der Theorie verzahnt**, nicht nur „Anhang mit Listing“.

---

## 3. Kurztext für die Ausarbeitung (Integrationsabschnitt, stark kürzbar)

*Zum Einfügen oder Umschreiben — auf ½–1 Seite in der End-PDF strecken oder auf 2–3 Absätze kürzen.*

Die bisherigen Kapitel haben **XMSS** und **SP 800-208** / **RFC 8391** als fachliche Grundlage beschrieben und operative Risiken benannt, die entstehen, wenn der **persistierte Signaturzustand** nicht zum tatsächlichen Gebrauch passt. Um dieses **organisatorisch-kryptographische** Spannungsfeld **anschaulich** zu machen — ohne den Umfang einer Referenzimplementierung — enthält das begleitende Repository ein **Lehr-Modell**: Eine Signaturfunktion bindet eine Nachricht an einen **fortlaufenden Index** mittels **HMAC**; der Index modelliert den **Zustand**. Die Konsole führt ein kurzes Szenario aus, in dem nach mehreren Signaturen ein **älterer Zustand** wiederhergestellt wird und erneut signiert wird. So wird das **Dilemma inkonsistenter Backups** illustriert. **Abgrenzung:** Dieses Modell ist **kein** XMSS, implementiert **keine** Einmal-Signaturen nach RFC 8391 und erlaubt **keine** Schlussfolgerungen auf reale Durchsatz- oder Sicherheitswerte von XMSS; es unterstützt die **Erklärung** des Zustandsproblems. Ein **Micro-Benchmark** misst die Laufzeit von Sign- und Verify-Operationen **in diesem Modell** und dient höchstens der Groborientierung, nicht einem Vergleich mit standardisierten PQC-Verfahren.

---

## 4. Grenzen explizit benennen (Checkliste für die PDF)

In der Ausarbeitung mindestens **ein** zusammenhängender Absatz oder eine kurze Liste:

- [ ] **Kein XMSS:** kein WOTS+, kein Merkle-Baum, keine RFC-8391-Konformität.
- [ ] **Kein Sicherheitsbeweis** für das Demo-Modell als kryptographisches Verfahren; nur **didaktische** Analogie zum Zustand.
- [ ] **Benchmark:** keine Übertragbarkeit auf XMSS/ML-DSA/SLH-DSA; keine Aussage „PQC ist schnell/langsam“ aus diesem Projekt allein.
- [ ] **Produktion:** kein HSM, keine Side-Channel-Härtung, kein Einsatz für echte Geheimnisse.

---

## 5. Präsentation (Phase E) — Anknüpfungspunkte

| Folie / Block | Inhalt |
|---------------|--------|
| Problem | Stateful braucht zuverlässigen Zähler/Index (1–2 Stichpunkte + Norm). |
| Risiko | Backup/Restore kann Zustand zurücksetzen → Wiederverwendung (qualitativ). |
| Demo | Terminal-Screenshot oder Live: `python -m stateful_signatures` — **einen Satz** „vereinfachtes Modell“. |
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
