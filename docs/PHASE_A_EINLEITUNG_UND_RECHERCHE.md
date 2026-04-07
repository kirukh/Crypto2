# Phase A — Vollständige Ausarbeitung: Einleitung, Standards, Vergleich

Dieses Dokument bündelt die für **Phase A** (Recherche & Gliederung) vorgesehenen Inhalte: **Einleitung** (Rohfassung für die spätere Ausarbeitung), **Kernpunkte aus Normen und RFCs**, die **OTS-Idee**, der **Vergleich stateless vs. stateful PQC** sowie **Literaturhinweise**. Die Kapitelgliederung steht in **[OUTLINE.md](OUTLINE.md)**.

---

## 1. Einleitung (Rohfassung für die schriftliche Arbeit)

Digitale Signaturen sichern Integrität und Authentizität von Daten und sind ein zentraler Baustein moderner Kryptografie. Für die langfristige Absicherung gegen Angreifer mit großen Rechenressourcen — einschließlich der Diskussion um **quantenresistente** Verfahren — hat die Forschung und Standardisierung **post-quantum Kryptografie (PQC)** vorangetrieben. Neben Gitter- und multivariaten Ansätzen spielen **hashbasierte Signaturen** eine besondere Rolle: Ihre Sicherheit lässt sich unter geeigneten Annahmen auf die Eigenschaften kryptographischer Hashfunktionen zurückführen und gilt in der üblichen Lesart als besonders gut verstanden.

Hashbasierte Konstruktionen nutzen typischerweise **Einmal-Signaturen (one-time signatures, OTS)**: Ein geheimer Schlüsselteil darf nur **einmal** zum Signieren verwendet werden; sonst bricht die vorgesehene Sicherheit. Um dennoch viele Nachrichten signieren zu können, werden **viele** OTS-Schlüsselpaare zu einem **Merkle-Baum** organisiert; der öffentliche Schlüssel umfasst dann u. a. die Wurzel des Baums. Beim Signieren wird eine konkrete OTS-Instanz ausgewählt und mit einem **Authentifikationspfad** durch den Baum nachgewiesen, dass sie zur Wurzel gehört. Verfahren wie **XMSS** (*eXtended Merkle Signature Scheme*) präzisieren diese Idee und sind in **RFC 8391** normiert. **NIST SP 800-208** fasst Empfehlungen zu **zustandsbehafteten** (stateful) hashbasierten Schemata zusammen, darunter XMSS und das **Leighton-Micali Signature (LMS)**-System.

Der entscheidende praktische Unterschied zu vielen anderen PQC-Signaturverfahren (z. B. gitter- oder hashbasierten **stateless** Verfahren nach FIPS 204/205) liegt im **Zustand**: Bei stateful hashbasierten Schemata muss der Signaturgegenstand **fortlaufend aktualisiert** werden — typischerweise ein **Zähler** oder Index, der angibt, welche OTS-Schlüssel bereits „verbraucht“ sind. Geht dieser Zustand verloren, wird falsch gesichert oder nach einem Backup wiederhergestellt, kann es zu **Wiederverwendung** von OTS-Material kommen und die Sicherheit zu bricht. Genau dieses **Zustandsmanagement** — inklusive Backup, Wiederherstellung und Betrieb — ist Gegenstand dieser Arbeit.

**Ziel** ist es, stateful hashbasierte Signaturen am Beispiel **XMSS** einzuordnen: Rolle von **SP 800-208** und **RFC 8391**, Bedeutung des **Zustands**, operative Risiken und diskutierte Lösungsrichtungen. Eine begleitende **Demonstrationsimplementierung** im Projekt illustriert das Zustandsproblem didaktisch; sie ersetzt keine produktive XMSS-Implementierung und ist in der Ausarbeitung klar als Lehr-/Demo-Code abzugrenzen.

Der Aufbau der Arbeit folgt der in **OUTLINE.md** skizzierten Gliederung.

---

## 2. NIST SP 800-208 — wichtigste Punkte (Kurzfassung)

**Quelle:** *Recommendation for Stateful Hash-Based Signature Schemes*, NIST Special Publication 800-208 (Final, Oktober 2020). Veröffentlichung und Volltext: [CSRC NIST SP 800-208](https://csrc.nist.gov/publications/detail/sp/800/208/final).

### 2.1 Gegenstand und Abgrenzung

- SP 800-208 beschreibt **Empfehlungen** für **stateful hashbasierte Signaturverfahren** und behandelt insbesondere **LMS** (inkl. HSS, hierarchischer Mehrbaum-Variante) und **XMSS** (inkl. **XMSS^MT** als Mehrbaum-Variante).
- Die Verfahren sind **post-quantum** geeignet im Sinne der dortigen Annahmen; die Sicherheitsargumente knüpfen an Hashfunktionen und die **korrekte Verwendung** des geheimen Zustands.

### 2.2 Zustandsmanagement als Sicherheitsvoraussetzung

- **Zentrale Aussage:** Die Sicherheit stateful hashbasierter Schemata hängt wesentlich davon ab, dass der **private Zustand** (welche Einmal-Schlüssel bereits verwendet wurden) **korrekt und monoton** fortgeschrieben wird. **Fehlbedienung** — etwa Wiederverwendung eines OTS nach einem veralteten Backup — kann die Sicherheit unterlaufen.
- NIST betont, dass solche Verfahren **nicht für jeden Einsatz** geeignet sind, sondern dort, wo der private Schlüsselgebrauch **kontrolliert** werden kann und der Betrieb (Monitoring, Speicherung) den Anforderungen genügt.

### 2.3 Parameter und Algorithmen (überblick)

- Das Dokument definiert **genehmigte Parameter** (u. a. Hashfunktionen wie **SHA-256** und **SHAKE256**, verschiedene Sicherheitsstufen und Baumhöhen) und beschreibt Signatur- und Verifikationsabläufe für LMS/XMSS und deren Varianten.
- Für konkrete Implementierungen sind die **tabellarisch** und **algorithmisch** im Volltext nachzulesen — für die Einordnung in der Arbeit reicht: **Parameterwahl** bestimmt u. a. Signaturgröße, Schlüsselgröße und die **maximale Anzahl** unterzeichnbarer Nachrichten.

### 2.4 Implementierungs- und Einsatzkontext (sinngemäß)

- SP 800-208 richtet sich an **Implementierer** und benennt Anforderungen an sichere Handhabung von Schlüsselmaterial und Zustand (u. a. im Kontext kryptographischer Module — Details im Originaltext und ggf. in FIPS 140-Kontexten).
- **Praxisrelevanz:** Dokumentation, **Backup-Strategien**, die den Zustand mitführen, und Schutz vor **Desynchronisation** mehrerer Instanzen gehören zur Betrachtung — sie knüpfen direkt an dein Kapitel zu Risiken und Lösungsideen an.

---

## 3. RFC 8391 — wichtigste Punkte (Kurzfassung)

**Quelle:** Hülsing et al., *XMSS: Extended Hash-Based Signatures*, **RFC 8391** (Mai 2018). Text: [RFC Editor 8391](https://www.rfc-editor.org/rfc/rfc8391).

### 3.1 Aufbau der Spezifikation

- RFC 8391 spezifiziert **XMSS** (Einbaum) und **XMSS^MT** (Mehrbaum für sehr viele Signaturen) sowie die zugrundeliegende **WOTS+**-Einmal-Signatur.
- Zielgruppe sind **Interoperable Implementierungen**; das RFC legt Datenformate, Algorithmen und **Parameter** fest.

### 3.2 WOTS+ (Winternitz OTS Plus)

- **WOTS+** ist eine **Hashketten-basierte** Einmal-Signatur. Jede Signatur „verbraucht“ das zugehörige Geheimnis im Sinne der OTS-Definition; eine zweite Signatur mit demselben Schlüsselindex wäre sicherheitskritisch.
- Die Parameter (Winternitz-Parameter, Hashfunktion, Ausgabelängen) steuern **Signaturgröße** und **Laufzeit**.

### 3.3 XMSS-Baum und Signatur

- Viele WOTS+-Schlüsselpaare werden als **Blätter** eines **Merkle-Baums** angeordnet; der **öffentliche XMSS-Schlüssel** enthält u. a. die **Baumwurzel** (und weitere öffentliche Parameter).
- Beim **Signieren** wird ein **Blattindex** (aktueller Zustand) verwendet: Es wird eine WOTS+-Signatur erzeugt und ein **Authentifikationspfad** geliefert, der die Verifikation zur Wurzel erlaubt. Danach muss der **Zustand** (Index) **weiterschalten** — das ist die stateful Natur im operativen Sinn.

### 3.4 Sicherheit (wie im RFC gerahmt)

- Die Sicherheit wird auf Eigenschaften der Hashfunktion(en) und die **korrekte Einhaltung** der Einmaligkeit bzw. des **Fortschritts des Index** zurückgeführt (präzise Theoreme und Annahmen im RFC und zugehöriger Literatur).
- **Hinweis für die Arbeit:** Ein RFC ist eine **Spezifikation**, keine Einführungsvorlesung — für didaktische Erklärungen ergänzt du Lehrbücher oder Survey-Artikel (siehe Literatur).

---

## 4. OTS-Idee und Merkle-Konstruktion (konzeptionell)

### 4.1 Einmal-Signatur (OTS)

- Idee: Aus einem Geheimnis werden **einmalig** Werte erzeugt, die eine Nachricht binden. Wird derselbe geheime Zustand **zweimal** genutzt, kann ein Angreifer unter typischen Annahmen **Information gewinnen** und Fälschungen ermöglichen.
- **Winternitz** verdichtet mehrere Bits pro Hashketten-Schritt; **WOTS+** ist die in XMSS verwendete Weiterentwicklung mit angepassten Hashaufrufen.

### 4.2 Merkle-Baum

- Um **viele** Nachrichten zu signieren, werden viele OTS-Instanzen nummeriert und durch einen **Hashbaum** so verbunden, dass der **öffentliche Schlüssel** kompakt bleibt (Wurzel).
- Der **private Schlüssel** enthält (oder leitet) das Material für die Blätter; entscheidend ist, dass der Signaturprozess **weiß**, welche Blätter schon benutzt wurden — **Zustand**.

---

## 5. Vergleich: Stateless vs. Stateful PQC-Signaturen

Die Einordnung bezieht sich auf die **übliche Klassifikation** in der PQC-Diskussion (NIST, Übersichtsarbeiten). Konkrete FIPS-Nummern dienen der Orientierung; Parameter und Namen sollst du bei Bedarf aus den aktuellen FIPS nachlesen.

| Aspekt | Stateless PQC-Signaturen (typisch) | Stateful hashbasiert (XMSS, LMS, …) |
|--------|-----------------------------------|-------------------------------------|
| **Beispiele (Standardisierung)** | **ML-DSA** (FIPS 204), **SLH-DSA** (*SPHINCS+*, FIPS 205) u. a. | **XMSS** / **XMSS^MT** (RFC 8391; SP 800-208), **LMS** / **HSS** (SP 800-208) |
| **Geheimer Zustand beim Signieren** | Kein fortlaufender **Index** im gleichen Sinne nötig; Schlüssel wird nicht „pro Signatur“ in einer OTS-Liste weitergeschaltet. | **Zustand** (Index / welche OTS bereits genutzt) **muss** sicher mitgeführt werden. |
| **Anzahl Signaturen** | Praktisch durch Lebensdauer des Schlüssels begrenzt, nicht durch eine kleine OTS-Tabelle im gleichen Sinne. | Durch Baumgröße / Parameter **begrenzt** (maximale Anzahl Signaturen pro Schlüssel). |
| **Backup / Restore** | Wichtig für Verfügbarkeit; **keine** OTS-Wiederverwendung durch „alten Zähler“. | **Kritisch:** Backup eines **alten** Zustands kann zu **Doppelnutzung** von OTS führen. |
| **Implementierung** | Oft einfacher für „signiere beliebig oft“, aber z. B. größere Schlüssel/Signaturen (verfahrensabhängig). | Hashbasiert oft **modular** und gut verstanden; aber **Betrieb und Zustandsspeicher** sind anspruchsvoll. |

**Wichtig:** Ein reiner **Geschwindigkeitsvergleich** (Benchmark) ist möglich, aber **interpretationsbedürftig**: unterschiedliche Sicherheitsniveaus, Parameter und **kein** gleicher „Betriebsaufwand“ (stateful erfordert Zustandslogik). Für Phase A genügt die **konzeptuelle** Tabelle; optional später Messungen mit klarer Legende.

---

## 6. Literatur- und Normenverweise (Arbeitsliste Phase A)

Volltexte urheberrechtlich geschützter Bücher gehören nicht ins Repository; hier nur **Titel und Bezug**. Eine **BibTeX-Starterliste** liegt unter `literature/sources.bib`.

| Typ | Referenz | Nutzen für die Arbeit |
|-----|----------|------------------------|
| Norm | **NIST SP 800-208** — Stateful Hash-Based Signature Schemes | Zustand, LMS/XMSS, Parameter, Implementierungshinweise |
| RFC | **RFC 8391** — XMSS | Algorithmik, Datenformate, WOTS+ |
| Standard | **FIPS 204** (ML-DSA), **FIPS 205** (SLH-DSA) — Kurz zitieren zum Kontrast „stateless“ | Abgrenzung in der Übersicht |
| Paper | Hülsing et al. — zu XMSS/WOTS+ (Originalarbeiten, zitiert in RFC/NIST) | Tiefe nach Bedarf |
| Survey | Übersichtsartikel zu PQC-Signaturen (Jahr ~2020ff.) | Einordnung des Feldes |

---

## 7. Bezug zum Projektplan (Phase A abgehakt)

| Aufgabe Phase A | Erfüllt in |
|-----------------|------------|
| SP 800-208, RFC 8391 (Auszüge) | Abschnitte 2–3 dieses Dokuments |
| OTS-Idee | Abschnitt 4 |
| Vergleich stateless vs. stateful PQC | Abschnitt 5 |
| Kapitelentwurf | **[OUTLINE.md](OUTLINE.md)** |
| Literaturliste | Abschnitt 6 + `literature/sources.bib` |

**Nächste Schritte (Phase B):** siehe **[PHASE_B_THEORIE.md](PHASE_B_THEORIE.md)** — Theorie nach Gliederung (Kapitel 2–7), operative Risiken und Lösungskapitel; für die finale PDF weiterhin **10-Seiten-Grenze** beachten (dieses Material ist ein Vorrat zum Kürzen).
