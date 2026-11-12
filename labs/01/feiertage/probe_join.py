"""Kurzer Join-Test: DB-Halte Köln Hbf (piebro/deutsche-bahn-data) x kalender_koeln.csv."""
import pandas as pd
kal = pd.read_csv("kalender_koeln_2024-07-01_2027-12-31.csv")
rows = []
for m in ["2025-05", "2026-02"]:
    d = pd.read_parquet(f"data-{m}.parquet", columns=["station_name", "time", "delay_in_min",
                        "arrival_is_canceled", "departure_is_canceled", "train_type"])
    d = d[d.station_name == "Köln Hbf"]
    d["datum"] = d.time.dt.date.astype(str)
    d["ausfall"] = d.arrival_is_canceled | d.departure_is_canceled
    g = d.groupby("datum").agg(halte=("delay_in_min", "size"),
                               verspaetung_mittel=("delay_in_min", "mean"),
                               anteil_ab_6min=("delay_in_min", lambda s: (s >= 6).mean()),
                               anteil_ausfall=("ausfall", "mean")).reset_index()
    rows.append(g)
t = pd.concat(rows).merge(kal, on="datum", how="left", validate="one_to_one")
print("Tage ohne Kalender-Treffer:", t.wochentag.isna().sum(), "von", len(t))
cols = ["datum", "wochentag", "feiertag_nrw", "karneval_koeln", "schulferien_nrw", "halte",
        "verspaetung_mittel", "anteil_ab_6min", "anteil_ausfall"]
pd.set_option("display.width", 200)
print(t[t.wochentag.isin(["Do", "Mo"])][cols].round(3).fillna("").to_string(index=False))
t.to_csv("probe_koeln_hbf_tage.csv", index=False)
