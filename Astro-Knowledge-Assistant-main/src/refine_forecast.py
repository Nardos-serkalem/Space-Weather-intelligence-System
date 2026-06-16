import os
import re

# 1. Using your EXACT filename from the screenshot
raw_path = os.path.expanduser("~/astro-knowledge-assistant/data/raw/noaa_live.txt")

try:
    with open(raw_path, 'r') as f:
        content = f.read()

    # 2. Improved Regex: Looks for 'II.' then 'Geomagnetic Activity Forecast'
    # It captures everything until it hits 'III.' or the end of the file.
    # The \s+ handles one or more spaces automatically.
    forecast_match = re.search(r'II\.\s+Geomagnetic\s+Activity\s+Forecast(.*?)(?=III\.)', content, re.DOTALL | re.IGNORECASE)

    if forecast_match:
        forecast_text = forecast_match.group(1).strip()
        print("🛰️ FOUND GEOMAGNETIC FORECAST:")
        print("-" * 40)
        print(forecast_text)
        print("-" * 40)
        
        # 3. Save to your processed folder
        output_path = os.path.expanduser("~/astro-knowledge-assistant/data/processed/latest_forecast.txt")
        with open(output_path, 'w') as f:
            f.write(forecast_text)
        print(f"✅ Saved to: {output_path}")
    else:
        print("❌ Forecast section not found!")
        print("Check if the file contains the text: 'II.  Geomagnetic Activity Forecast'")

except FileNotFoundError:
    print(f"❌ File not found at: {raw_path}")