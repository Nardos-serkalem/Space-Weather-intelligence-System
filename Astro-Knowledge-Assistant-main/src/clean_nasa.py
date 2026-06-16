import json
import pandas as pd
import os

RAW_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/raw/nasa_live.json"
)

OUTPUT_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/nasa_events_cleaned.csv"
)


def clean_nasa():
    with open(RAW_PATH, "r") as f:
        data = json.load(f)

    records = []

    for event in data:
        peak = event.get("peakTime", "")

        records.append({
            "date": peak.split("T")[0] if peak else None,
            "flare_class": event.get("classType"),
            "event_id": event.get("flrID"),
            "peak_time": peak,
            "source": "NASA-DONKI-LIVE"
        })

    df = pd.DataFrame(records)
    df.dropna(subset=["date"], inplace=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("✅ NASA cleaned:", len(df))


if __name__ == "__main__":
    clean_nasa()
