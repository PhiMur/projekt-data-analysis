#!/usr/bin/env python3
"""
Muenster 'Maengelmelder' (Buergerbeschwerden) via Open311 abrufen und lokal als CSV
speichern -- Datengrundlage fuer die NLP-Themenextraktion (IU DLBDSEDA02, Aufgabe 1).

Quelle : Stadt Muenster / Beteiligung NRW, Open311 GeoReport v2.
Lizenz : Datenlizenz Deutschland Namensnennung 2.0 (DL-DE-BY 2.0).
Hinweis: Der Endpunkt liefert max. 1000 Datensaetze pro Aufruf und filtert nach
         Datumsbereich. Deshalb wird Monat fuer Monat abgefragt. Erreicht ein Monat
         das Limit doch einmal, gibt das Skript eine Warnung aus.

Einmal ausfuehren, um data/muenster_maengelmelder.csv zu erzeugen. Das Notebook
liest danach nur diese lokale Datei (reproduzierbar, kein erneuter API-Zugriff noetig).
"""
import csv
import datetime as dt
from pathlib import Path

import requests

BASE = ("https://beteiligung.nrw.de/api/rest/public/open311/v2/"
        "beteiligung/1003255/requests.json")
CAP = 1000                       # Server-Limit pro Aufruf
START = dt.date(2022, 1, 1)      # Fensteranfang (anpassbar)
END = dt.date(2026, 7, 9)        # Fensterende = letzter vollstaendiger Kalendertag.
                                 # Eingefroren, damit ein erneuter Abruf moeglichst denselben
                                 # Korpus (17.659 Meldungen) liefert wie die dokumentierte Analyse.
OUT = Path(__file__).resolve().parents[1] / "data" / "muenster_maengelmelder.csv"

FIELDS = ["service_request_id", "requested_datetime", "service_name",
          "status", "description", "address", "zipcode", "lat", "long",
          "status_notes"]


def month_ranges(start, end):
    cur = dt.date(start.year, start.month, 1)
    while cur <= end:
        nxt = dt.date(cur.year + 1, 1, 1) if cur.month == 12 \
            else dt.date(cur.year, cur.month + 1, 1)
        yield cur, min(nxt - dt.timedelta(days=1), end)
        cur = nxt


def clean(value):
    return (value or "").replace("\r", " ").replace("\n", " ").strip()


def main():
    records = {}
    for m_start, m_end in month_ranges(START, END):
        params = {"start_date": m_start.isoformat(), "end_date": m_end.isoformat()}
        r = requests.get(BASE, params=params, timeout=60)
        r.raise_for_status()
        batch = r.json()
        if len(batch) >= CAP:
            print(f"  ! Warnung: {m_start:%Y-%m} liefert {CAP} Treffer, Monat evtl. unvollstaendig")
        for rec in batch:
            rid = rec.get("service_request_id") or rec.get("id")
            if rid is not None:
                records[str(rid)] = rec
        print(f"{m_start:%Y-%m}: +{len(batch):4d}  (gesamt {len(records)})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for rec in records.values():
            w.writerow({
                "service_request_id": rec.get("service_request_id") or rec.get("id"),
                "requested_datetime": rec.get("requested_datetime"),
                "service_name": rec.get("service_name"),
                "status": rec.get("status"),
                "description": clean(rec.get("description")),
                "address": rec.get("address") or rec.get("address_string"),
                "zipcode": rec.get("zipcode"),
                "lat": rec.get("lat") or rec.get("latitude"),
                "long": rec.get("long") or rec.get("longitude"),
                "status_notes": clean(rec.get("status_notes")),
            })

    print(f"gespeichert: {OUT} ({len(records)} Meldungen)")


if __name__ == "__main__":
    main()
