import os
import subprocess
import pandas as pd
from retriever import retrieve
from datetime import datetime, UTC

while True:

    user_question = input("\n🌞 Ask about solar activity (type exit): ")

    if user_question.lower() == "exit":
        print("👋 Exiting assistant.")
        break

    event_context = retrieve(user_question)
    today = datetime.now(UTC).strftime("%B %d, %Y")

    print("\n📚 Retrieved context:")
    print("---------------------")
    print(event_context)
    print("---------------------")

    # NOAA numeric trends
    noaa_live_path = os.path.expanduser(
        "~/astro-knowledge-assistant/data/processed/noaa_indices_cleaned.csv"
    )

    noaa_df = pd.read_csv(noaa_live_path)

    trend_context = noaa_df.tail(10).to_string(index=False)

    prompt = f"""
SYSTEM ROLE
You are the Lead Space Weather Forecaster at NASA's Space Weather Prediction Center.

Your task is to analyze real solar activity data and produce a professional space weather intelligence briefing.

IMPORTANT SCIENTIFIC RULES

GROUNDING RULE
You MUST base your answer ONLY on the provided datasets below.

STRICT DATA POLICY
• If the dataset lists an event, you MUST report it.
• Do NOT contradict dataset information.
• Do NOT invent solar events or measurements.
• If information is missing, write: "Data not available."

DATA INTERPRETATION RULES
• Solar Energetic Particle (SEP) events = Radiation Hazard
• CME speeds determine geomagnetic risk
• Sunspot numbers indicate solar activity level
• If events are linked, reconstruct the solar event chain

CURRENT DATE
{today}

===== DATASET 1 — Recent Solar Events =====

Contains:
• Solar Flares (FLR)
• Coronal Mass Ejections (CME)
• Geomagnetic Storms (GST)
• Solar Energetic Particle Events (SEP)

{event_context}

===== DATASET 2 — Solar Activity Trends =====

Contains:
• Daily Sunspot Numbers
• Solar Radio Flux

{trend_context}


USER QUESTION

{user_question}


ANALYSIS INSTRUCTIONS


Perform the following analysis steps.

1 CURRENT ALERTS

Check Dataset 1 for active threats.

• If ANY SEP events exist → Report **RADIATION HAZARD ACTIVE**
• If CME speed > 800 km/s → Warn of potential geomagnetic storm impact
• If GST events exist → Report geomagnetic storm activity

2 EVENT TIMELINE

If linked events exist, reconstruct the solar activity chain.

Example structure:

Solar Event Chain
Flare → CME → SEP Radiation Storm

Include:
• Event type
• Date/time
• Key measurements

3 RECENT SOLAR ACTIVITY

Summarize the most important recent events:

• Solar flare class and location
• CME speeds
• SEP radiation events
• Geomagnetic storm activity

Always reference dataset values.

4 SOLAR INDICES

From Dataset 2 report:

• Latest Sunspot Number
• Solar Radio Flux

Briefly explain what these indicate about solar activity levels.

5 SPACE WEATHER THREAT CLASSIFICATION

Use ONLY the following deterministic rules.

HIGH ALERT
• Sunspot Number > 120
• CME speed > 900 km/s

CAUTION
• Sunspot Number > 90
• CME speed > 500 km/s
• ANY SEP radiation event detected

NOMINAL
• Quiet solar conditions
• No major CME or SEP activity

6 FORECAST SUMMARY

Provide a short operational assessment describing:

• Satellite risk
• Astronaut radiation risk
• Geomagnetic storm potential

IMPORTANT:
If Dataset 1 does NOT contain a SEP event,
do NOT report a radiation hazard.

OUTPUT FORMAT


Write the final report as a professional operational briefing.

### OFFICIAL SPACE WEATHER BULLETIN ###

**Current Alerts**

**Solar Event Timeline**

**Recent Solar Activity**

**Solar Indices**

**Space Weather Threat Level**

**Operational Forecast**


SCIENTIFIC INTEGRITY STATEMENT


All statements MUST be supported by the provided datasets.

If information is unavailable, clearly state:
"Data not available."

Never invent events, measurements, or forecasts.
"""

    print("\n🤖 Llama-3 analyzing solar environment...")
 
    try:

        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        print("\n--- SOLAR BRIEFING ---")
        print(result.stdout)

    except Exception as e:

        print(f"\n❌ Error: {e}")