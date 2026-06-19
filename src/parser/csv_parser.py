import csv
from pathlib import Path
from typing import Any

from app_types.schemas import INT_COLUMNS, REQUIRED_COLUMNS
from parser.validator import validate_rows


def parse_game_time_to_seconds(game_time: str) -> int:
    """
    Converts MM:SS into total seconds.
    Example: 01:55 -> 115
    """
    value = game_time.strip()

    if ":" not in value:
        raise ValueError(f"Invalid game_time format '{game_time}'. Expected MM:SS.")

    minutes, seconds = value.split(":", 1)
    return int(minutes) * 60 + int(seconds)


def read_csv_data(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header.")

        missing_columns = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        rows: list[dict[str, Any]] = []

        for index, row in enumerate(reader, start=2):
            cleaned = {key: value.strip() for key, value in row.items()}

            for col in INT_COLUMNS:
                try:
                    cleaned[col] = int(cleaned[col])
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid integer in row {index}, column '{col}': {cleaned[col]}"
                    ) from exc

            cleaned["game_time_seconds"] = parse_game_time_to_seconds(cleaned["game_time"])
            cleaned["_row_number"] = index

            rows.append(cleaned)

    validate_rows(rows)
    return rows