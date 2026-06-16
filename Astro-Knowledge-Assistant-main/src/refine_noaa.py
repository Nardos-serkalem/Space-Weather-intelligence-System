import pandas as pd
import os

# Paths
raw_file = os.path.expanduser("~/astro-knowledge-assistant/data/raw/noaa_live.txt")
output_file = os.path.expanduser("~/astro-knowledge-assistant/data/processed/noaa_indices_cleaned.csv")

def refine_data():
    cleaned = []

    with open(raw_file, "r") as f:
        for line in f:
            parts = line.split()

            # Skip headers
            if len(parts) < 16:
                continue

            # Skip lines not starting with year
            if not parts[0].isdigit():
                continue

            try:
                cleaned.append({
                    "date": f"{parts[0]}-{parts[1]}-{parts[2]}",
                    "radio_flux": parts[3],
                    "sunspot_number": parts[4],
                    "flare_C": parts[10],
                    "flare_M": parts[11],
                    "flare_X": parts[12],
                    "source": "NOAA-LIVE"
                })
            except Exception:
                continue

    df = pd.DataFrame(cleaned)
    df.to_csv(output_file, index=False)

    print(f"✅ NOAA cleaned successfully: {len(df)} rows")

if __name__ == "__main__":
    refine_data()
