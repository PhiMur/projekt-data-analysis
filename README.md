# NLP-Themenextraktion aus Bürgerbeschwerden der Stadt Münster

Projekt zum Kurs **Projekt: Data Analysis (DLBDSEDA02), Aufgabe 1**. Ziel: aus den Freitext-Meldungen
des Münsteraner *Mängelmelders* (Open311-Bürgeranliegen) die am häufigsten angesprochenen Themen
extrahieren und für die Stadtverwaltung aufbereiten.

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
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Der Datensatz (Mängelmelder Münster, Open311-Schnittstelle) wird als nächster Schritt mit einem
Abruf-Skript beschafft. Die Daten selbst bleiben lokal unter `data/` und werden nicht versioniert
(`.gitignore`).
