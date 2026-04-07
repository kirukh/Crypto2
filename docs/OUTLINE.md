# Gliederungsvorschlag (Kapitelentwurf)

Vorschlag mit **sieben Hauptkapiteln** — für die spätere Ausarbeitung (max. 10 Seiten bei Code) musst du Prioritäten setzen und ggf. Unterpunkte streichen oder in die Präsentation verschieben.

1. **Einleitung**  
   Motivation (PQC, Signaturbedarf), Problem stateful/hashbasiert, Ziel und Abgrenzung der Arbeit, Aufbau.

2. **Überblick digitale Signaturen und PQC**  
   Klassische und PQC-Familien kurz; Rolle von Hashfunktionen; warum hashbasierte Verfahren eine eigene Nische haben.

3. **Einmal-Signaturen und Merkle: Von der Idee zu XMSS**  
   OTS/Winternitz/WOTS+ (intuitiv), Merkle-Baum, Bedeutung des Index; Übergang zu XMSS als konkretisiertem Schema.

4. **XMSS und Zustand: Normen und Spezifikation**  
   **RFC 8391** (Aufbau, Parameter), **SP 800-208** (Empfehlungen, stateful Anforderungen); was „Zustand“ in Implementierung und Dokumentation bedeutet.

5. **Operative Risiken: Backup, Zähler, Desynchronisation**  
   Bedrohungsbild (OTS-Wiederverwendung, alte Backups); typische Fehlerszenarien; Abgrenzung zur Demo im Repository.

6. **Lösungsrichtungen und Grenzen**  
   Zentrale Signatur, HSM, klare Backup-Politik, Monitoring — kurz und kritisch; Grenzen eines studentischen Demonstrators.

7. **Fazit und Ausblick**  
   Kernerkenntnisse, offene Punkte, ggf. Verweis auf Präsentation/Demo.

---

Die **inhaltliche Erstfassung** zu diesen Kapiteln (Phase B) steht in **[PHASE_B_THEORIE.md](PHASE_B_THEORIE.md)**. Wie Kapitel **5–7** mit der **Demo** zusammenspielen (Roter Faden, Grenzen), steht in **[PHASE_D_INTEGRATION.md](PHASE_D_INTEGRATION.md)**.

*Gliederung: Phase A; bei Änderungen mit Betreuung abstimmen.*
