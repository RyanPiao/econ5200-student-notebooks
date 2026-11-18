"""Build the worked example's small table: average weekday boardings per MBTA bus route, Fall 2016 to Fall 2025.

Source: MBTA Blue Book Open Data Portal, "MBTA Bus Ridership by Trip, Season, Route, Line, and Stop", ArcGIS item
8daf4a33925a4df59183f860826d29ee (73 MB zip, 1.0 GB unpacked, ten falls and Spring 2024). Each row is one stop on
one scheduled trip, and `boardings` is the average number boarding there on that trip across the sampled days, so
a route's average weekday boardings is the sum over its weekday rows.

The files come in three layouts, which is why a one-line loader breaks:
  Fall 2016-2023  season = "Fall 2016", route_id, day_type_name = weekday/saturday/sunday, boardings
  Fall 2024       season = "Fall" with a separate year column (and a byte-order mark on the first header)
  Fall 2025       "GTFS route_id", "Day Type" = Wkdy/Fri/Sat/Sun, "Boardings"; Friday is split from Wkdy
The fall comes from the file name. Route ids are read as text: "34E", "57A" and "70A" are not numbers, and "741" is a Silver Line route.

Writes mbta_route_fall_weekday.csv (route, fall, boardings): the file students load. The zip is downloaded once into
raw/ (gitignored) and never committed.

    python3 build_mbta_table.py
"""
import re
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
URL = "https://www.arcgis.com/sharing/rest/content/items/8daf4a33925a4df59183f860826d29ee/data"
ZIP = HERE / "raw" / "mbta_bus_ridership.zip"
OUT = HERE / "mbta_route_fall_weekday.csv"

LAYOUTS = {   # first year of the layout: (route column, day-type column, weekday value, boardings column)
    2016: ("route_id", "day_type_name", "weekday", "boardings"),
    2024: ("route_id", "day_type_name", "weekday", "boardings"),
    2025: ("GTFS route_id", "Day Type", "Wkdy", "Boardings"),
}


def layout(year):
    return LAYOUTS[max(y for y in LAYOUTS if y <= year)]


def main():
    if not ZIP.exists():
        ZIP.parent.mkdir(exist_ok=True)
        print("downloading", URL)
        urllib.request.urlretrieve(URL, ZIP)
    parts = []
    with zipfile.ZipFile(ZIP) as z:
        for name in sorted(z.namelist()):
            m = re.search(r"_Fall_(\d{4})\.csv$", name)
            if not m:                                        # the folder entry and Spring 2024
                continue
            year = int(m.group(1))
            route, day, weekday, boardings = layout(year)
            with z.open(name) as f:
                df = pd.read_csv(f, usecols=[route, day, boardings], dtype={route: str}, encoding="utf-8-sig")
            days = sorted(df[day].dropna().unique())
            wk = df[df[day] == weekday]
            assert len(wk), f"Fall {year}: no {weekday!r} rows in {days}"
            g = wk.groupby(wk[route].str.strip())[boardings].sum().rename("boardings").reset_index()
            g.columns = ["route", "boardings"]
            g.insert(1, "fall", year)
            parts.append(g)
            print(f"Fall {year}: {len(df):>9,} rows, day types {days}; {len(g)} routes with weekday service, "
                  f"{g['boardings'].sum():,.0f} weekday boardings")
    table = pd.concat(parts, ignore_index=True).sort_values(["route", "fall"])
    table["boardings"] = table["boardings"].round(1)
    table.to_csv(OUT, index=False)
    falls = table["fall"].nunique()
    every = (table.groupby("route")["fall"].nunique() == falls).sum()
    print(f"wrote {OUT.name}: {len(table):,} rows, {table['route'].nunique()} route ids, {every} in all {falls} falls")


if __name__ == "__main__":
    main()
