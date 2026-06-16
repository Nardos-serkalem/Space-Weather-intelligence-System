import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

BASE_PATH = os.path.expanduser("~/astro-knowledge-assistant/data/raw/")
NASA_ARCHIVE_FILE = os.path.join(BASE_PATH, "nasa_archive.jsonl")

def fetch_nasa_data(event_type="FLR"):
    """Fetches NASA DONKI data for FLR, CME, or GST"""
    print(f"🌐 Fetching NASA {event_type}...")
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://api.nasa.gov/DONKI/{event_type}?startDate=2026-01-01&endDate={today}&api_key={NASA_API_KEY}"

    try:
        response = requests.get(url, timeout=30)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ Error fetching {event_type}: {e}")
        return None

def archive_nasa_data(all_events):
    os.makedirs(BASE_PATH, exist_ok=True)
    existing_ids = set()
    
    if os.path.exists(NASA_ARCHIVE_FILE):
        with open(NASA_ARCHIVE_FILE, "r") as f:
            for line in f:
                try:
                    ev = json.loads(line)
                    # Check for all possible ID types
                    eid = ev.get("flrID") or ev.get("gstID") or ev.get("sepID") or ev.get("activityID")
                    if eid: existing_ids.add(eid)
                except: continue

    new_count = 0
    with open(NASA_ARCHIVE_FILE, "a") as f:
        for event in all_events:
            eid = event.get("flrID") or event.get("gstID") or event.get("sepID") or event.get("activityID")
            if eid and eid not in existing_ids:
                f.write(json.dumps(event) + "\n")
                new_count += 1
    print(f"📦 Archived {new_count} new events.")

if __name__ == "__main__":
    # Fetch all three
    flares = fetch_nasa_data("FLR") or []
    cmes = fetch_nasa_data("CME") or []
    gst = fetch_nasa_data("GST") or []
    seps = fetch_nasa_data("SEP") or []    
    archive_nasa_data(flares + cmes + gst + seps)