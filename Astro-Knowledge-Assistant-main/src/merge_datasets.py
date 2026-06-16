import pandas as pd
import os

base = os.path.expanduser("~/astro-knowledge-assistant/data/processed")

noaa = pd.read_csv(f"{base}/noaa_indices_cleaned.csv")
nasa = pd.read_csv(f"{base}/nasa_events_cleaned.csv")

combined = pd.concat([noaa, nasa], ignore_index=True)
combined.drop_duplicates(subset=["date", "event_id"], inplace=True)

combined.to_csv(f"{base}/master_combined.csv", index=False)

combined.drop_duplicates(inplace=True)

save_path = f"{base}/master_combined.csv"
combined.to_csv(save_path, index=False)

print("✅ Combined dataset saved:", save_path)
print("Rows:", len(combined))
