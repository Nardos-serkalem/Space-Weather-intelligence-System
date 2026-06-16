import pandas as pd
import os
import json
from solar_chunker import build_chunk

DATA_RAW = os.path.expanduser("~/astro-knowledge-assistant/data/raw/")
NASA_ARCHIVE_INPUT = os.path.join(DATA_RAW, "nasa_archive.jsonl")
OUTPUT_PATH = os.path.expanduser("~/astro-knowledge-assistant/data/processed/documents.pkl")

def process_nasa_archive():
    nasa_chunks = []
    if not os.path.exists(NASA_ARCHIVE_INPUT): return []

    with open(NASA_ARCHIVE_INPUT, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                
                # Identify Event Type and Tag
                if "flrID" in event:
                    e_tag, display_name = "FLR", "Solar Flare"
                    intensity = event.get("classType")
                    details = f"Location: {event.get('sourceLocation')}. Peak: {event.get('peakTime')}."
                
                elif "gstID" in event:
                    e_tag, display_name = "GST", "Geomagnetic Storm"
                    all_kp = [item.get("kpIndex") for item in event.get("allKp", [])]
                    max_kp = max(all_kp) if all_kp else "N/A"
                    intensity = f"Max Kp-Index: {max_kp}"
                    details = f"Storm peak Kp-index: {max_kp}. Linked Events: {event.get('linkedEvents')}."

                elif "sepID" in event:
                    e_tag, display_name = "SEP", "Solar Energetic Particle Event"
                    intensity = "Radiation Storm"
                    linked = event.get('linkedEvents', [])
                    chain = " -> ".join([link.get('activityID', '') for link in linked]) if linked else "None"
                    
                    details = (
                        f"RADIATION STORM DETECTED. "
                        f"This SEP is linked to the following activity chain: {chain}. "
                        f"High-energy protons pose immediate hazard to satellites."
                    )
                elif event.get("eventType") == "CME" or "cmeAnalyses" in event:
                    e_tag, display_name = "CME", "CME"
                    analyses = event.get("cmeAnalyses", [])
                    if analyses:
                        speed = analyses[0].get("speed")
                        intensity = f"Speed: {speed} km/s"
                        details = f"CME moving at {speed} km/s. Half-angle: {analyses[0].get('halfAngle')}."
                    else:
                        intensity, details = "N/A", "CME analysis not available."
                else:
                    continue

                time_val = event.get("eventTime") or event.get("beginTime") or event.get("startTime") or "N/A"
                date = time_val.split("T")[0] if "T" in time_val else None

                chunk = build_chunk(
                    event_type=display_name,
                    date=date,
                    time_value=time_val,
                    class_intensity=intensity,
                    details=details,
                    source="NASA DONKI"
                )
                chunk["metadata"]["event_type"] = e_tag
                nasa_chunks.append(chunk)
            except: continue
    return nasa_chunks

def build_documents():
    nasa_docs = process_nasa_archive()
    if nasa_docs:
        pd.to_pickle(nasa_docs, OUTPUT_PATH)
        print(f"✅ Indexed {len(nasa_docs)} events (Flares, CMEs, GST, SEPs).")

if __name__ == "__main__":
    build_documents()