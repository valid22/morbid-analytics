"""
pipeline.py — Morbid Analytics data processor
Reads raw death counts, computes lifetime odds, outputs processed CSV.
"""

import pandas as pd
import json
import os

POPULATION = 335_000_000   # US 2022 estimate
LIFE_EXP   = 77.5          # US average life expectancy 2024


def lifetime_odds(annual_deaths: int) -> str:
    """Convert annual US death count to a lifetime odds string."""
    if annual_deaths == 0:
        return "1 in ∞"
    annual_rate = annual_deaths / POPULATION
    odds = 1 / (annual_rate * LIFE_EXP)
    return f"1 in {round(odds):,}"


def load_raw_data(path: str) -> pd.DataFrame:
    """Load and validate raw death counts CSV."""
    df = pd.read_csv(path)
    required = ["cause", "annual_us", "source", "year"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def process(df: pd.DataFrame) -> pd.DataFrame:
    """Compute lifetime odds and sort by annual deaths descending."""
    df = df.copy()
    df["lifetime_odds"] = df["annual_us"].apply(lifetime_odds)
    df["annual_rate_per_100k"] = (df["annual_us"] / POPULATION * 100_000).round(4)
    df["rank"] = df["annual_us"].rank(ascending=False, method="first").astype(int)
    return df.sort_values("rank").reset_index(drop=True)


def export_json(df: pd.DataFrame, path: str) -> None:
    """Export processed data as JSON for use in the website."""
    records = df.to_dict(orient="records")
    with open(path, "w") as f:
        json.dump(records, f, indent=2)
    print(f"  → JSON exported to {path}")


if __name__ == "__main__":
    raw_path  = "data/raw_deaths.csv"
    out_csv   = "data/processed.csv"
    out_json  = "data/processed.json"

    if not os.path.exists(raw_path):
        print(f"Raw data not found at {raw_path}")
        print("Creating example file...")
        example = pd.DataFrame([
            {"cause": "Heart disease",   "annual_us": 702880, "source": "CDC WONDER", "year": 2022},
            {"cause": "Cancer",          "annual_us": 608371, "source": "CDC WONDER", "year": 2022},
            {"cause": "Overdose",        "annual_us": 107941, "source": "CDC WONDER", "year": 2022},
            {"cause": "Car crash",       "annual_us": 42795,  "source": "NHTSA",      "year": 2022},
            {"cause": "Shark attack",    "annual_us": 1,      "source": "ISAF",       "year": 2022},
        ])
        os.makedirs("data", exist_ok=True)
        example.to_csv(raw_path, index=False)
        print(f"  → Example CSV written to {raw_path}")

    df = load_raw_data(raw_path)
    out = process(df)

    out.to_csv(out_csv, index=False)
    print(f"Processed {len(out)} causes → {out_csv}")

    export_json(out, out_json)

    print("\nSample output:")
    print(out[["rank", "cause", "annual_us", "lifetime_odds"]].head(5).to_string(index=False))

    # Sanity check
    hd_odds = lifetime_odds(702880)
    shark_odds = lifetime_odds(1)
    print(f"\nSanity check:")
    print(f"  Heart disease (702,880/yr): {hd_odds}")
    print(f"  Shark attack (1/yr):        {shark_odds}")
