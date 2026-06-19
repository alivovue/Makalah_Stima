from typing import Any

from app_types.enums import (
    ACTION_LOCATIONS,
    ACTIONS,
    LANE_ROLES,
    LORD_LANES,
    LORD_STATUSES,
    OBJECTIVE_SIDES,
    OBJECTIVE_TYPES,
    TEAMS,
)
from app_types.schemas import ALLY_TOWER_COLUMNS, ENEMY_TOWER_COLUMNS, ALLY_ALIVE_COLUMNS, ENEMY_ALIVE_COLUMNS


def _ensure_in(value: str, allowed: list[str], row_number: int, column: str) -> None:
    if value not in allowed:
        raise ValueError(
            f"Invalid value in row {row_number}, column '{column}': {value}. "
            f"Allowed: {allowed}"
        )


def _ensure_binary(value: int, row_number: int, column: str) -> None:
    if value not in [0, 1]:
        raise ValueError(
            f"Invalid binary value in row {row_number}, column '{column}': {value}. "
            "Allowed: 0 or 1."
        )


def validate_rows(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        row_number = int(row.get("_row_number", -1))

        _ensure_in(row["team"], TEAMS, row_number, "team")
        _ensure_in(row["opponent"], TEAMS, row_number, "opponent")

        if row["team"] == row["opponent"]:
            raise ValueError(f"Row {row_number}: team and opponent cannot be the same.")

        _ensure_in(row["upper_lane_role"], LANE_ROLES, row_number, "upper_lane_role")
        _ensure_in(row["mid_lane_role"], LANE_ROLES, row_number, "mid_lane_role")
        _ensure_in(row["lower_lane_role"], LANE_ROLES, row_number, "lower_lane_role")

        _ensure_in(row["next_objective_type"], OBJECTIVE_TYPES, row_number, "next_objective_type")
        _ensure_in(row["objective_side"], OBJECTIVE_SIDES, row_number, "objective_side")

        _ensure_in(row["lord_status"], LORD_STATUSES, row_number, "lord_status")
        _ensure_in(row["lord_lane"], LORD_LANES, row_number, "lord_lane")

        _ensure_in(row["action_location"], ACTION_LOCATIONS, row_number, "action_location")
        _ensure_in(row["current_action"], ACTIONS, row_number, "current_action")

        for col in ALLY_ALIVE_COLUMNS + ENEMY_ALIVE_COLUMNS:
            _ensure_binary(row[col], row_number, col)

        for col in ALLY_TOWER_COLUMNS + ENEMY_TOWER_COLUMNS:
            _ensure_binary(row[col], row_number, col)