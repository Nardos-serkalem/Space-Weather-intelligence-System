import argparse
import json
import re
import sys
from typing import Dict, List, Optional


DATE_PATTERNS = [
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"\b(\d{4})/(\d{2})/(\d{2})\b"),
    re.compile(r"\b(\d{4})\s+(\d{2})\s+(\d{2})\b"),  # NOAA format
]
TIME_PATTERN = re.compile(r"\b(\d{2}:\d{2}(?::\d{2})?(?:Z| UTC)?)\b")
CLASS_PATTERN = re.compile(r"\b([ABCMX]\d+(?:\.\d+)?)\b", re.IGNORECASE)
SOURCE_PATTERN = re.compile(r"source\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def _clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _display(value: Optional[str]) -> str:
    return value if value else "Not available"


def _event_type_from_text(text: str) -> str:
    lowered = text.lower()
    if "solar flare" in lowered or "flare" in lowered:
        return "Solar Flare"
    if "coronal mass ejection" in lowered or "cme" in lowered:
        return "Coronal Mass Ejection"
    if "particle" in lowered or "sep" in lowered or "radiation" in lowered:
        return "Solar Energetic Particle Event"
    if "sunspot" in lowered:
        return "Sunspot Activity"
    if "radio flux" in lowered:
        return "Solar Radio Flux Observation"
    if "geomagnetic" in lowered or "kp" in lowered:
        return "Geomagnetic Activity"
    return "Solar Activity Report"


def _extract_date(text: str) -> Optional[str]:
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        groups = match.groups()

        if len(groups) == 1:
            return groups[0]

        year, month, day = groups
        return f"{year}-{month}-{day}"

    


def _extract_time(text: str) -> Optional[str]:
    match = TIME_PATTERN.search(text)
    return _clean_text(match.group(1)) if match else None


def _extract_class(text: str) -> Optional[str]:
    match = CLASS_PATTERN.search(text)
    return _clean_text(match.group(1).upper()) if match else None


def _extract_source(text: str) -> Optional[str]:
    explicit = SOURCE_PATTERN.search(text)
    if explicit:
        return _clean_text(explicit.group(1))

    lowered = text.lower()
    if "donki" in lowered:
        return "NASA DONKI"
    if "nasa" in lowered:
        return "NASA"
    if "noaa" in lowered or "swpc" in lowered:
        return "NOAA SWPC"
    return None


def build_chunk(
    event_type: Optional[str],
    date: Optional[str],
    time_value: Optional[str],
    class_intensity: Optional[str],
    details: Optional[str],
    source: Optional[str],
) -> Dict[str, object]:
    chunk_text = (
        f"Solar Event: {_display(_clean_text(event_type))}\n"
        f"Date: {_display(_clean_text(date))}\n"
        f"Time: {_display(_clean_text(time_value))}\n"
        f"Class/Intensity: {_display(_clean_text(class_intensity))}\n"
        f"Details: {_display(_clean_text(details))}\n"
        f"Source: {_display(_clean_text(source))}"
    )

    metadata = {
        "event_type": _clean_text(event_type),
        "date": _clean_text(date),
        "class": _clean_text(class_intensity),
        "source": _clean_text(source),
        "confidence": "high",
    }

    return {"text": chunk_text, "metadata": metadata}


def _split_units(raw_text: str) -> List[str]:
    text = raw_text.replace("\r\n", "\n").strip()
    if not text:
        return []

    units = [u.strip() for u in re.split(r"\n\s*\n+", text) if u.strip()]
    if len(units) > 1:
        return units

    single = units[0]
    lines = [line.strip("-* \t") for line in single.splitlines() if line.strip()]
    dated_lines = [line for line in lines if _extract_date(line)]
    if len(dated_lines) >= 2:
        return dated_lines
    return units


def chunk_raw_solar_text(raw_text: str) -> List[Dict[str, object]]:
    chunks: List[Dict[str, object]] = []
    for unit in _split_units(raw_text):
        source = _extract_source(unit)
        event_type = _event_type_from_text(unit)
        date = _extract_date(unit)
        time_value = _extract_time(unit)
        class_intensity = _extract_class(unit)
        details = _clean_text(" ".join(line.strip() for line in unit.splitlines()))

        chunks.append(
            build_chunk(
                event_type=event_type,
                date=date,
                time_value=time_value,
                class_intensity=class_intensity,
                details=details,
                source=source,
            )
        )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk raw solar activity text.")
    parser.add_argument(
        "--input-file",
        type=str,
        default=None,
        help="Optional path to a raw text file. If omitted, read from stdin.",
    )
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        raw_text = sys.stdin.read().strip()

    print(json.dumps(chunk_raw_solar_text(raw_text), indent=2))


if __name__ == "__main__":
    main()
