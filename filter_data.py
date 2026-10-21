#2.1 Wrangling dan EDA
# Poin 1–2: Periode dan filter
# Timestamp RetailRocket berupa milidetik (UTC). Data dipecah menjadi dua periode dengan `filter_data.py`:
# - P1 (training): 2 Juni – 2 Agustus 2015 → 1.316.260 baris
# - P2 (testing): 11 – 26 Agustus 2015 → 286.662 baris
# Hasil disimpan ke `events_p1.csv` dan `events_p2.csv`, lalu P1 diimpor ke Neo4j (database `utsgsd`) dengan `import_data.py`.


import argparse
import os

import pandas as pd


def to_ms(date_str):
    """Ubah tanggal (YYYY-MM-DD) ke milidetik epoch (UTC)."""
    return int(pd.Timestamp(date_str, tz="UTC").timestamp() * 1000)


def parse_arguments():
    p = argparse.ArgumentParser(description="Filter events.csv per periode.")
    p.add_argument("--source", default="data")
    p.add_argument("--p1-start", required=True)
    p.add_argument("--p1-end", required=True)
    p.add_argument("--p2-start", required=True)
    p.add_argument("--p2-end", required=True)
    return p.parse_args()


def filter_period(df, start, end):
    start_ms = to_ms(start)
    end_ms = to_ms(end) + 24 * 3600 * 1000
    return df[(df["timestamp"] >= start_ms) & (df["timestamp"] < end_ms)]


def main():
    args = parse_arguments()
    df = pd.read_csv(os.path.join(args.source, "events.csv"))
    print("Total baris asli:", len(df))

    for name, s, e in [
        ("p1", args.p1_start, args.p1_end),
        ("p2", args.p2_start, args.p2_end),
    ]:
        sub = filter_period(df, s, e)
        out = os.path.join(args.source, f"events_{name}.csv")
        sub.to_csv(out, index=False)
        print(f"{name.upper()} ({s} s/d {e}): {len(sub)} baris -> {out}")
        print(sub["event"].value_counts().to_string())


if __name__ == "__main__":
    main()