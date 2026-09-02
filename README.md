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
schreibt die CSV. Das Abruf-Fenster ist im Skript auf den Analysestand eingefroren (bis 09.07.2026),
damit ein erneuter Abruf möglichst denselben Korpus ergibt wie die dokumentierte Analyse. Ein Hinweis
dazu: Das Portal veröffentlicht Meldungen erst nach Moderation. Ein späterer Abruf kann darum auch im
gleichen Fenster geringfügig mehr Meldungen enthalten, wodurch sich die Kennzahlen und die
Themenzusammensetzung leicht verschieben können.

## Pipeline (Notebook `notebooks/analysis.ipynb`)

1. Daten laden & sichten (`pandas`)
2. Vorverarbeitung zu „sauberen Texten“: Kleinschreibung, Bereinigung (`re`, Umlaute bleiben erhalten),
   Tokenisierung + deutsche Stoppwörter (`nltk`), Wortnormalisierung mit `nltk` `SnowballStemmer('german')`
3. Vektorisierung mit zwei Verfahren: Bag-of-Words + TF-IDF (`scikit-learn`)
4. Kurzvergleich der beiden Vektorisierungen
5. Themenextraktion mit zwei Verfahren: LSA + LDA (`scikit-learn`: `TruncatedSVD`, `LatentDirichletAllocation`)
6. Darstellung & Diskussion (Top-Wörter je Thema als Balkendiagramm, `matplotlib`)

## Ergebnisse (Kurzfassung)

Das LDA-Modell (k = 8) findet mehrere gut benennbare Themen. Übersicht mit den jeweils fünf
wichtigsten Wörtern (Wortstämme, daher verkürzt):

- Thema 1 (Müllsäcke und wilde Entsorgung): entsorgt, wurd, mullsack, mull, sack
- Thema 2 (Straßen- und Radwegschäden): strass, radweg, gefahr, viel, schlagloch
- Thema 3 (Ampeln und Kreuzungen): ampel, recht, hoh, richtung, kreuzung
- Thema 4 (ohne klares Thema, Orts- und Lageangaben): strass, str, stell, kreuzung, warendorf
- Thema 5 (Bäume und Äste): baum, ast, gross, war, gehweg
- Thema 6 (Schrotträder): gehweg, haus, fahrrad, schrottrad, rad
- Thema 7 (Ratten, Laternen, Wasser): strass, ratt, latern, viel, wass
- Thema 8 (Sperrmüll und illegale Ablagerung): mull, sperrmull, viel, illegal, leid

Der häufigste Beschwerdegrund ist die illegale Müllentsorgung, sie prägt die Themen 1 und 8. Der
Abgleich mit den amtlichen Kategorien (`service_name`, nie Modell-Input) zeigt Übereinstimmung in den
Kernen: die dominante Kategorie „Illegale Abfallablagerung“ spiegelt sich in zwei Themen, Schrotträder
und Ampeln finden ihre Kategorie wieder. Eine 1:1-Zuordnung entsteht nicht, weil die amtliche Taxonomie
feiner ist als k = 8. Im Vergleich liefert LDA besser interpretierbare Themen als LSA, dessen Komponenten
stärker überlappen.

Die Themenzahl k wurde an den Werten 5, 8 und 12 erprobt und nach zwei Kriterien festgelegt: der
Interpretierbarkeit der Themen und der Themenkohärenz (einfache UMass-Variante) als nachrechenbarer
Kennzahl. Die mittlere Kohärenz liegt bei -121.5 (k = 5), -126.4 (k = 8) und -128.2 (k = 12), die
Kennzahl bevorzugt also knapp wenige Themen. Der Abstand ist klein, und bei k = 5 geht der Bereich
Schrotträder in einem großen Straßen- und Fahrrad-Thema unter, obwohl er mit über 1.000 Meldungen eine
der größten amtlichen Kategorien ist. Bei k = 12 zersplittert der Müll dagegen auf drei Themen, und das
schwächste Thema fällt deutlich ab. Gewählt wurde deshalb k = 8. Zusätzlich weist das Notebook die
Kohärenz einzeln je Thema aus.

## So führen Sie das Projekt aus

Entwickelt und getestet mit **Python 3.14** (funktioniert ebenso mit Python 3.11–3.13).

```bash
# 1. Virtuelle Umgebung anlegen und aktivieren
python -m venv .venv
.venv\Scripts\activate   # Windows

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Datensatz beschaffen (erzeugt data/muenster_maengelmelder.csv)
python scripts/01_fetch_muenster_maengelmelder.py

# 4. (Optional) NLTK-Daten vorab laden, das Notebook macht das beim Lauf auch selbst
python -c "import nltk; [nltk.download(p, quiet=True) for p in ('punkt','punkt_tab','stopwords')]"

# 5. Notebook starten und vollständig ausführen
jupyter notebook notebooks/analysis.ipynb
```

## Reproduzierbarkeit

`requirements.txt` benennt alle benötigten Pakete, bewusst ohne Versions-Pins, damit die Installation
auch auf aktuellen Python-Versionen funktioniert. Entwickelt und geprüft wurde mit pandas 3.0.3,
scikit-learn 1.9.0, nltk 3.10.0 und matplotlib 3.11.0 unter Python 3.14. Das Notebook läuft von oben
nach unten ohne manuelle Zwischenschritte durch (die NLTK-Daten werden zur Laufzeit geladen). Geprüft mit `pruefe_repro.py`
(im übergeordneten Arbeitsordner): frische venv + `pip install -r requirements.txt` +
`nbconvert --execute` → Notebook läuft fehlerfrei durch.
