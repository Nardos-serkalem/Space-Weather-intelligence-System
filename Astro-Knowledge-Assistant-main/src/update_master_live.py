import json
import pandas as pd
import os

# Paths
nasa_json_path = os.path.expanduser("~/astro-knowledge-assistant/data/raw/nasa_live.json")
master_csv_path = os.path.expanduser("~/astro-knowledge-assistant/data/processed/master_cleaned.csv")

def update_from_live():
    # 1. Load the live NASA JSON
    with open(nasa_json_path, 'r') as f:
        data = json.load(f)
    
    # 2. Extract the important bits
    new_events = []
    for event in data:
        new_events.append({
            "date": event.get("peakTime", "").split("T")[0],
            "class": event.get("classType"),
            "event_id": event.get("flrID"),
            "peak_time": event.get("peakTime", "").split("T")[1].replace("Z", ""),
            "source": "NASA-DONKI-LIVE"
        })
    
    # 3. Create DataFrame and Merge
    new_df = pd.DataFrame(new_events)
    
    if os.path.exists(master_csv_path):
        master_df = pd.read_csv(master_csv_path)
        # Drop duplicates based on Event ID so we don't double-count
        combined_df = pd.concat([master_df, new_df]).drop_duplicates(subset=['event_id'], keep='last')
    else:
        combined_df = new_df

    # 4. Save
    combined_df.to_csv(master_csv_path, index=False)
    print(f"📈 Master Knowledge Base updated with {len(new_events)} live NASA events!")

if __name__ == "__main__":
    update_from_live()