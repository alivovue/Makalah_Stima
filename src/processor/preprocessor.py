from typing import Any

from app_types.enums import START_DECISION
from processor.context_builder import build_all_contexts


def add_decision(row: dict[str, Any]) -> None:
    row["decision"] = (row["current_action"], row["action_location"])


def preprocess_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Adds:
    - decision
    - previous_decision
    - objective_context
    - advantage_context
    - structure_context
    - lord_context
    """
    processed = [dict(row) for row in rows]

    processed.sort(key=lambda row: (row["match_id"], row["team"], row["game_time_seconds"]))

    previous_by_match_team: dict[tuple[str, str], tuple[str, str]] = {}

    for row in processed:
        add_decision(row)

        key = (row["match_id"], row["team"])
        row["previous_decision"] = previous_by_match_team.get(key, START_DECISION)

        contexts = build_all_contexts(row)
        row["objective_context"] = contexts["objective"]
        row["advantage_context"] = contexts["advantage"]
        row["structure_context"] = contexts["structure"]
        row["lord_context"] = contexts["lord"]

        previous_by_match_team[key] = row["decision"]

    return processed