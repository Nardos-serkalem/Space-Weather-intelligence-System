import pandas as pd
import os

MASTER_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/master_combined.csv"
)

OUTPUT_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/master_cleaned.csv"
)


def clean_dataset():
    df = pd.read_csv(MASTER_PATH)

    print("Original rows:", len(df))

    # Normalize date
    df["datetime_utc"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        utc=True
    )

    # Remove invalid dates
    df = df.dropna(subset=["datetime_utc"])

    # Remove duplicates
    df = df.drop_duplicates(
    subset=["datetime_utc", "source", "event_id"],
    keep="first"
)

    # Sort chronologically
    df = df.sort_values("datetime_utc")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Clean dataset saved:", OUTPUT_PATH)
    print("Final rows:", len(df))


if __name__ == "__main__":
    clean_dataset()
