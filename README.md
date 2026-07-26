# NLP-Themenextraktion aus Bürgerbeschwerden der Stadt Münster

Projekt zum Kurs **Projekt: Data Analysis (DLBDSEDA02), Aufgabe 1**. Ziel: aus den Freitext-Meldungen
des Münsteraner *Mängelmelders* (Open311-Bürgeranliegen) die am häufigsten angesprochenen Themen
extrahieren und für die Stadtverwaltung aufbereiten.

## Datensatz

**Quelle:** Stadt Münster / Beteiligung NRW, Open311-Schnittstelle.
**Lizenz:** Datenlizenz Deutschland Namensnennung 2.0 (DL-DE-BY-2.0).

Zentrale Spalte ist der Freitext `description` (die eigentliche Bürgermeldung). `service_name` ist die
von der Stadt vergebene Kategorie. Die Daten liegen lokal unter `data/muenster_maengelmelder.csv`
(per `.gitignore` von der Versionierung ausgenommen) und werden mit dem Abruf-Skript erzeugt:

```bash
python scripts/01_fetch_muenster_maengelmelder.py
```
Das Skript ruft die Open311-API monatsweise ab (behandelt das 1000-Treffer-Limit pro Aufruf) und
schreibt die CSV.

## Geplante Pipeline (aus dem Konzept)

1. Daten laden & sichten (`pandas`)
2. Vorverarbeitung zu „sauberen Texten“: Kleinschreibung, Bereinigung (`re`),
   Tokenisierung + deutsche Stoppwörter (`nltk`), Wortnormalisierung mit `nltk` `SnowballStemmer('german')`
3. Vektorisierung mit zwei Verfahren: Bag-of-Words + TF-IDF (`scikit-learn`)
4. Kurzvergleich der beiden Vektorisierungen
5. Themenextraktion mit zwei Verfahren: LSA + LDA (`scikit-learn`: `TruncatedSVD`, `LatentDirichletAllocation`)
6. Darstellung & Diskussion (Top-Wörter je Thema als Balkendiagramm, `matplotlib`)

## Einrichtung

```bash
# 1. Virtuelle Umgebung anlegen und aktivieren
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Datensatz beschaffen (erzeugt data/muenster_maengelmelder.csv)
python scripts/01_fetch_muenster_maengelmelder.py
```
