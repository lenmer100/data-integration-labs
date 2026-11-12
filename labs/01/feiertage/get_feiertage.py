#!/usr/bin/env python3
"""get_feiertage.py: baut eine Feiertags- und Kalendertabelle für Köln/NRW.

Hauptquelle: Wikipedia, Artikel "Feiertag (Deutschland)" (früher "Gesetzliche
Feiertage in Deutschland", der alte Titel leitet dorthin weiter), CC BY-SA 4.0.
Abgleich:    Python-Paket `holidays` und https://feiertage-api.de
Zusätzlich:  NRW-Schulferien (Schulministerium NRW, dl-de/by-2-0; Abgleich OpenHolidays API),
             Kölner Karnevalstage (aus Aschermittwoch abgeleitet, keine Feiertage).
             Heimspiele des 1. FC Köln (OpenLigaDB, ODbL 1.0) werden bewusst nicht
             eingelesen: ODbL und CC BY-SA sind beide Share-Alike und lassen sich
             in einer gemeinsamen Tabelle nicht sauber mischen.

Aufruf: python3 get_feiertage.py
Ergebnis: siehe OUT_* unten, Rohdaten in raw/.
"""
import io
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import holidays
import pandas as pd
import requests
from bs4 import BeautifulSoup

START = date(2024, 7, 1)    # erster Monat der DB-Daten (piebro/deutsche-bahn-data)
END = date(2027, 12, 31)
YEARS = range(START.year, END.year + 1)

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)
OUT_FEIERTAGE = HERE / "feiertage_de_2024-2027.csv"
OUT_KALENDER = HERE / "kalender_koeln_2024-07-01_2027-12-31.csv"
OUT_EVENTS = HERE / "events_koeln_2024-2027.csv"
OUT_FERIEN = HERE / "schulferien_nrw_2024-2027.csv"

UA = {"User-Agent": "data-integration-labs/lenmer100 (TH Koeln, student project)"}
WIKI_API = "https://de.wikipedia.org/w/api.php"
WIKI_TITLE = "Feiertag (Deutschland)"
LAENDER = ["BW", "BY", "BE", "BB", "HB", "HH", "HE", "MV",
           "NI", "NW", "RP", "SL", "SN", "ST", "SH", "TH"]
MONATE = {"Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
          "Juli": 7, "August": 8, "September": 9, "Oktober": 10,
          "November": 11, "Dezember": 12}
WOCHENTAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def log_source(url, out):
    with open(RAW / "SOURCES.txt", "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {url} -> {out}\n")


def get_json(url, params=None, out=None):
    r = requests.get(url, params=params, headers=UA, timeout=60)
    r.raise_for_status()
    if out:
        (RAW / out).write_text(r.text)
        log_source(r.url, f"raw/{out}")
    return r.json()


# ---------------------------------------------------------------- Wikipedia
def fetch_wikipedia():
    d = get_json(WIKI_API, {"action": "parse", "page": WIKI_TITLE, "prop": "text|revid",
                            "format": "json", "formatversion": 2, "redirects": 1},
                 out="wikipedia_feiertag_deutschland.json")["parse"]
    meta = get_json(WIKI_API, {"action": "query", "prop": "revisions", "revids": d["revid"],
                               "rvprop": "timestamp", "format": "json", "formatversion": 2})
    ts = meta["query"]["pages"][0]["revisions"][0]["timestamp"]
    print(f"Wikipedia: '{d['title']}', Version {d['revid']} vom {ts}")
    return d["text"], d["revid"], ts


def years_valid(cell_text):
    """Liest aus einer Zelle wie 'ja', 'seit 2019', 'nur 2020/2025', 'bis 1994',
    in welchen Jahren unseres Zeitraums der Feiertag gilt."""
    t = re.sub(r"\[A\s*\d+\]", "", cell_text).strip()
    if t.lower() == "ja":
        return set(YEARS)
    if m := re.fullmatch(r"seit\s*(\d{4})", t):
        return {y for y in YEARS if y >= int(m.group(1))}
    if m := re.fullmatch(r"nur\s*([\d/ ]+)", t):
        return {int(y) for y in m.group(1).split("/")} & set(YEARS)
    return set()  # 'bis 1994', '2017', leer, nur Fußnote


def parse_overview(html):
    """Tabelle 'Übersicht aller gesetzlichen Feiertage': Feiertag x Bundesland.
    Farben laut Legende: hintergrundfarbe9 = landesweit, hintergrundfarbe8 = regional,
    keine Farbe + nur Fußnote = nur schulfrei (zählt nicht als Feiertag)."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")
    regeln = []
    for tr in rows[2:]:
        cells = tr.find_all(["td", "th"])
        if len(cells) != 17:
            continue
        name_raw = cells[0].get_text(" ", strip=True)
        if name_raw.startswith(("Gesamtzahl", "davon")):
            continue
        name_raw = re.sub(r"\[\s*A\s*\d+\s*\]", "", name_raw).strip()
        name_raw = re.sub(r"\s+,", ",", re.sub(r"\s{2,}", " ", name_raw))
        if not name_raw:   # Wiederholung der Kopfzeile am Tabellenende
            continue
        regel = {"wiki_bezeichnung": name_raw, "landesweit": {}, "regional": {}}
        for land, c in zip(LAENDER, cells[1:]):
            txt = c.get_text(strip=True)
            cls = " ".join(c.get("class") or [])
            if "hintergrundfarbe8" in cls:          # regional, Fußnote erklärt wo
                regel["regional"][land] = set(YEARS)
            else:
                ys = years_valid(txt)
                if ys:
                    regel["landesweit"][land] = ys
        regeln.append(regel)
    return regeln


def parse_moving(html):
    """Tabelle 'Bewegliche Feiertage' (Datum je Jahr, ab 2025)."""
    tables = pd.read_html(io.StringIO(html))
    t = next(x for x in tables if str(x.columns[0]) == "Bezeichnung" and "Fronleichnam" in x.iloc[:, 0].astype(str).str.cat())
    t2 = next(x for x in tables if str(x.columns[0]) == "Bezeichnung" and "Aschermittwoch" in x.iloc[:, 0].astype(str).str.cat())
    out = {}
    for tab in (t, t2):
        for _, r in tab.iterrows():
            name = re.sub(r"\s+", " ", re.sub(r"\(\d\)", "", str(r["Bezeichnung"]))).strip()
            for col in tab.columns:
                if re.fullmatch(r"\d{4}", str(col)):
                    dd, mm = str(r[col]).strip(".").split(".")
                    out[(name, int(col))] = date(int(col), int(mm), int(dd))
    return out


def easter(y):  # Gauß/Meeus, nur für Jahre, die die Wikipedia-Tabelle nicht hat
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(y, month, day)


OSTER_ABSTAND = {"Gründonnerstag": -3, "Karfreitag": -2, "Ostersonntag": 0,
                 "Ostermontag": 1, "Christi Himmelfahrt": 39, "Pfingstsonntag": 49,
                 "Pfingstmontag": 50, "Fronleichnam": 60, "Aschermittwoch": -46}
# Zeilennamen der Übersicht -> Namen in der Tabelle der beweglichen Feiertage
BEWEGLICH = {"Gründonnerstag": "Gründonnerstag", "Karfreitag": "Karfreitag",
             "Ostersonntag": "Ostersonntag", "Ostermontag": "Ostermontag",
             "Himmelfahrt": "Christi Himmelfahrt", "Pfingstsonntag": "Pfingstsonntag",
             "Pfingstmontag": "Pfingstmontag", "Fronleichnam": "Fronleichnam",
             "Buß- und Bettag": "Buß- und Bettag"}


def moving_date(name, y, wiki_dates):
    if (name, y) in wiki_dates:
        return wiki_dates[(name, y)], "wikipedia"
    if name == "Buß- und Bettag":   # Mittwoch vor dem 23. November
        d = date(y, 11, 22)
        while d.weekday() != 2:
            d -= timedelta(days=1)
        return d, "berechnet"
    return easter(y) + timedelta(days=OSTER_ABSTAND[name]), "berechnet"


def build_feiertage(regeln, wiki_dates, revid):
    rows = []
    for r in regeln:
        raw = r["wiki_bezeichnung"]
        m = re.match(r"(\d{1,2})\.\s*(\w+)\s*–\s*(.+)", raw)
        for y in YEARS:
            if m:  # festes Datum
                d = date(y, MONATE[m.group(2)], int(m.group(1)))
                name, typ, quelle = m.group(3).strip(), "fest", "wikipedia"
            else:
                key = next(k for k in BEWEGLICH if k in raw)
                name = BEWEGLICH[key]
                d, quelle = moving_date(name, y, wiki_dates)
                typ = "beweglich"
            lw = sorted(l for l, ys in r["landesweit"].items() if y in ys)
            rg = sorted(l for l, ys in r["regional"].items() if y in ys)
            if not lw and not rg:
                continue
            if not (START <= d <= END):
                continue
            rows.append({
                "datum": d.isoformat(), "jahr": y, "wochentag": WOCHENTAGE[d.weekday()],
                "name": name, "typ": typ,
                "geltung": "bundesweit" if len(lw) == 16 else "regional",
                "anzahl_laender": len(lw),
                "laender_landesweit": ";".join(lw),
                "laender_teilweise": ";".join(rg),
                "is_nrw": "NW" in lw,
                "datum_quelle": quelle,
                "wiki_revid": revid,
            })
    df = pd.DataFrame(rows)
    # Name aus der Übersicht kürzen, z. B. 'Neujahr(stag)' -> 'Neujahr'
    df["name"] = (df["name"].str.replace(r"\(.*?\)", "", regex=True)
                  .str.replace(r"\s*–.*$", "", regex=True).str.strip())
    return df.sort_values(["datum", "name"]).reset_index(drop=True)


# ---------------------------------------------------------------- Abgleich
def crosscheck(df):
    probleme = []
    wiki_nw = set(df.loc[df.is_nrw, "datum"])
    # 1) holidays-Paket, NRW
    pk = holidays.Germany(subdiv="NW", years=YEARS)
    pk_nw = {d.isoformat() for d in pk if START <= d <= END}
    for d in sorted(wiki_nw ^ pk_nw):
        probleme.append(f"holidays-Paket NW weicht ab: {d}")
    # 2) holidays-Paket, alle Länder: Zahl der Länder je Datum
    for land in LAENDER:
        pkl = {d.isoformat() for d in holidays.Germany(subdiv=land, years=YEARS) if START <= d <= END}
        wl = set(df.loc[df.laender_landesweit.str.contains(land), "datum"])
        for d in sorted(wl ^ pkl):
            probleme.append(f"holidays-Paket {land} weicht ab: {d} "
                            f"({'nur Wikipedia' if d in wl else 'nur Paket'})")
    # 3) feiertage-api.de, NRW
    api_nw = set()
    for y in YEARS:
        j = get_json("https://feiertage-api.de/api/", {"jahr": y, "nur_land": "NW"},
                     out=f"feiertage-api_NW_{y}.json")
        api_nw |= {v["datum"] for v in j.values() if START.isoformat() <= v["datum"] <= END.isoformat()}
    for d in sorted(wiki_nw ^ api_nw):
        probleme.append(f"feiertage-api.de NW weicht ab: {d}")
    return probleme, len(pk_nw), len(api_nw)


# ---------------------------------------------------------------- Zusatzdaten
FERIEN_CSV = "https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/Schulferien/OpenData_Ferientermine.csv"
FERIEN_KEY = "https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/Schulferien/key_Ferienbezeichner.csv"


def read_msb_csv(url, out):
    """CSV des Schulministeriums: erste Zeile 'sep=;' (Excel-Hinweis), Semikolon am Zeilenende."""
    r = requests.get(url, headers=UA, timeout=60)   # leitet auf apps.schulministerium.nrw.de um
    r.raise_for_status()
    (RAW / out).write_bytes(r.content)
    log_source(r.url, f"raw/{out}")
    df = pd.read_csv(io.BytesIO(r.content), sep=";", skiprows=1, dtype=str, index_col=False)
    return df.loc[:, ~df.columns.str.startswith("Unnamed")]


def fetch_schulferien():
    """Hauptquelle: Ministerium für Schule und Bildung NRW (Open.NRW, dl-de/by-2-0).
    Abgleich: OpenHolidays API (ODbL 1.0)."""
    f = read_msb_csv(FERIEN_CSV, "msb_ferientermine.csv")
    key = read_msb_csv(FERIEN_KEY, "msb_key_ferienbezeichner.csv")
    f = f.merge(key, on="FerienID", how="left")
    f["start"] = pd.to_datetime(f.ErsterTagSort, format="%Y%m%d").dt.date.astype(str)
    f["ende"] = pd.to_datetime(f.LetzterTagSort, format="%Y%m%d").dt.date.astype(str)
    f = f[(f.ende >= START.isoformat()) & (f.start <= END.isoformat())]
    f = f.rename(columns={"Schuljahr": "schuljahr", "Ferienbezeichnung": "name"})
    f["name"] = f["name"].map({"Sommer": "Sommerferien", "Herbst": "Herbstferien",
                               "Weihnachten": "Weihnachtsferien", "Ostern": "Osterferien",
                               "Pfingsten": "Pfingstferien"})
    f = f[["schuljahr", "name", "start", "ende"]].sort_values("start").reset_index(drop=True)
    # Abgleich mit OpenHolidays
    oh = set()
    for a, b in [("2024-07-01", "2026-06-30"), ("2026-07-01", "2027-12-31")]:  # API: max. 1095 Tage
        j = get_json("https://openholidaysapi.org/SchoolHolidays",
                     {"countryIsoCode": "DE", "subdivisionCode": "DE-NW", "validFrom": a,
                      "validTo": b, "languageIsoCode": "DE"}, out=f"openholidays_ferien_NW_{a[:4]}.json")
        oh |= {(x["startDate"], x["endDate"]) for x in j}
    msb = set(zip(f.start, f.ende))
    f["openholidays_gleich"] = [(a, b) in oh for a, b in zip(f.start, f.ende)]
    return f, sorted(msb ^ oh)


def karneval(wiki_dates):
    rows = []
    for y in YEARS:
        asch = wiki_dates.get(("Aschermittwoch", y)) or easter(y) + timedelta(days=-46)
        q = "wikipedia (Aschermittwoch)" if ("Aschermittwoch", y) in wiki_dates else "berechnet"
        for name, off in [("Weiberfastnacht", -6), ("Karnevalssonntag", -3),
                          ("Rosenmontag", -2), ("Veilchendienstag", -1)]:
            rows.append({"datum": (asch + timedelta(days=off)).isoformat(), "name": name,
                         "kategorie": "karneval", "uhrzeit": "", "ort": "Köln",
                         "ist_gesetzlicher_feiertag": False, "quelle": q})
        rows.append({"datum": date(y, 11, 11).isoformat(), "name": "Sessionseröffnung (11.11.)",
                     "kategorie": "karneval", "uhrzeit": "11:11", "ort": "Köln",
                     "ist_gesetzlicher_feiertag": False, "quelle": "festes Datum"})
    df = pd.DataFrame(rows)
    return df[(df.datum >= START.isoformat()) & (df.datum <= END.isoformat())]


# ---------------------------------------------------------------- Kalender
def build_kalender(fe, ferien, events):
    k = pd.DataFrame({"datum": pd.date_range(START, END, freq="D")})
    k["datum"] = k.datum.dt.date.astype(str)
    d = pd.to_datetime(k.datum)
    k["wochentag"] = [WOCHENTAGE[x] for x in d.dt.day_of_week]
    k["ist_wochenende"] = d.dt.day_of_week >= 5
    nw = fe[fe.is_nrw].groupby("datum")["name"].agg(" / ".join)
    k["ist_feiertag_nrw"] = k.datum.isin(nw.index)
    k["feiertag_nrw"] = k.datum.map(nw).fillna("")
    anz = fe.groupby("datum")["anzahl_laender"].max()
    k["anzahl_laender_mit_feiertag"] = k.datum.map(anz).fillna(0).astype(int)
    k["ist_feiertag_bundesweit"] = k.anzahl_laender_mit_feiertag == 16
    # Tagtyp wie im Fahrplan: Feiertage fahren meist wie Sonntage
    k["tagtyp"] = "Werktag"
    k.loc[d.dt.day_of_week == 5, "tagtyp"] = "Samstag"
    k.loc[(d.dt.day_of_week == 6) | k.ist_feiertag_nrw, "tagtyp"] = "Sonn-/Feiertag"
    # Brückentag: Werktag zwischen NRW-Feiertag und Wochenende
    frei = k.ist_wochenende | k.ist_feiertag_nrw
    k["ist_brueckentag_nrw"] = (~frei) & frei.shift(1, fill_value=False) & frei.shift(-1, fill_value=False)
    # Schulferien
    k["schulferien_nrw"] = ""
    for _, f in ferien.iterrows():
        m = (k.datum >= f.start) & (k.datum <= f.ende)
        k.loc[m, "schulferien_nrw"] = f["name"]
    k["ist_schulferien_nrw"] = k.schulferien_nrw != ""
    kv = events[events.kategorie == "karneval"].groupby("datum")["name"].agg(" / ".join)
    k["karneval_koeln"] = k.datum.map(kv).fillna("")
    k["ist_karneval_koeln"] = k.karneval_koeln != ""
    return k


def main():
    (RAW / "SOURCES.txt").unlink(missing_ok=True)
    html, revid, ts = fetch_wikipedia()
    regeln = parse_overview(html)
    wiki_dates = parse_moving(html)
    fe = build_feiertage(regeln, wiki_dates, revid)
    probleme, n_pk, n_api = crosscheck(fe)
    ferien, ferien_diff = fetch_schulferien()
    events = karneval(wiki_dates).sort_values("datum").reset_index(drop=True)
    kal = build_kalender(fe, ferien, events)

    fe.to_csv(OUT_FEIERTAGE, index=False)
    kal.to_csv(OUT_KALENDER, index=False)
    events.to_csv(OUT_EVENTS, index=False)
    ferien.to_csv(OUT_FERIEN, index=False)

    # ---- kurzer Qualitätsbericht
    print(f"\nFeiertage (alle Länder): {len(fe)} Zeilen, {fe.datum.nunique()} Tage, "
          f"{fe.datum.min()} bis {fe.datum.max()}")
    print(f"  davon NRW: {fe.is_nrw.sum()}, bundesweit: {(fe.geltung == 'bundesweit').sum()}, "
          f"regional: {(fe.geltung == 'regional').sum()}")
    print(f"  Datum berechnet statt aus Wikipedia: {(fe.datum_quelle == 'berechnet').sum()}")
    print(f"  Duplikate (datum+name): {fe.duplicated(['datum', 'name']).sum()}, "
          f"leere Zellen: {int(fe.drop(columns=['laender_teilweise']).isna().sum().sum())}")
    # Wikipedia-Ostertabelle gegen eigene Berechnung
    diff = [(n, y) for (n, y), d in wiki_dates.items() if n in OSTER_ABSTAND
            and easter(y) + timedelta(days=OSTER_ABSTAND[n]) != d]
    print(f"  Wikipedia-Tabelle bewegliche Feiertage vs. Osterformel: {len(diff)} Abweichungen {diff}")
    print(f"Abgleich NRW: holidays-Paket {n_pk} Tage, feiertage-api.de {n_api} Tage, "
          f"Wikipedia {fe.is_nrw.sum()} Tage")
    print("  Abweichungen:", "keine" if not probleme else "")
    for p in probleme:
        print("   -", p)
    print(f"Kalender: {len(kal)} Zeilen ({kal.datum.min()} bis {kal.datum.max()}), "
          f"Lücken: {len(pd.date_range(START, END)) - len(kal)}, Duplikate: {kal.datum.duplicated().sum()}")
    print(f"  NRW-Feiertage: {kal.ist_feiertag_nrw.sum()}, davon am Wochenende: "
          f"{(kal.ist_feiertag_nrw & kal.ist_wochenende).sum()}, Brückentage: {kal.ist_brueckentag_nrw.sum()}")
    print(f"  Schulferientage NRW: {kal.ist_schulferien_nrw.sum()}, Karnevalstage: {kal.ist_karneval_koeln.sum()}")
    print(f"Events: {len(events)} Zeilen, Schulferien: {len(ferien)} Zeiträume, "
          f"Abweichungen Schulministerium vs. OpenHolidays: {ferien_diff or 'keine'}")


if __name__ == "__main__":
    sys.exit(main())
