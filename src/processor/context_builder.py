from typing import Any

from app_types.schemas import ALLY_ALIVE_COLUMNS, ENEMY_ALIVE_COLUMNS


def get_timer_bucket(timer: int) -> str:
    if timer == -1:
        return "UNKNOWN"
    if timer == 0:
        return "AVAILABLE"
    if 1 <= timer <= 30:
        return "SOON"
    if 31 <= timer <= 75:
        return "MID"
    return "FAR"


def get_gold_bucket(gold_diff: int) -> str:
    if gold_diff <= -3000:
        return "BIG_BEHIND"
    if -3000 < gold_diff <= -1000:
        return "BEHIND"
    if -1000 < gold_diff < 1000:
        return "EVEN"
    if 1000 <= gold_diff < 3000:
        return "AHEAD"
    return "BIG_AHEAD"


def get_alive_bucket(alive_diff: int) -> str:
    if alive_diff < 0:
        return "DOWN"
    if alive_diff == 0:
        return "EVEN"
    return "UP"


def get_jungler_state(row: dict[str, Any]) -> str:
    ally_alive = row["ally_jungle_alive"]
    enemy_alive = row["enemy_jungle_alive"]

    if ally_alive == 1 and enemy_alive == 1:
        return "BOTH_ALIVE"
    if ally_alive == 1 and enemy_alive == 0:
        return "ALLY_ONLY"
    if ally_alive == 0 and enemy_alive == 1:
        return "ENEMY_ONLY"
    return "BOTH_DEAD"


def build_objective_context(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        row["next_objective_type"],
        get_timer_bucket(row["next_objective_timer_seconds"]),
        row["objective_side"],
    )


def build_advantage_context(row: dict[str, Any]) -> tuple[str, str, str]:
    ally_alive_count = sum(row[col] for col in ALLY_ALIVE_COLUMNS)
    enemy_alive_count = sum(row[col] for col in ENEMY_ALIVE_COLUMNS)

    gold_diff = row["team_gold"] - row["enemy_gold"]
    alive_diff = ally_alive_count - enemy_alive_count

    return (
        get_gold_bucket(gold_diff),
        get_alive_bucket(alive_diff),
        get_jungler_state(row),
    )


def _destroyed_count(row: dict[str, Any], prefix: str, tier: str) -> int:
    columns = [
        f"{prefix}_upper_{tier}_alive",
        f"{prefix}_mid_{tier}_alive",
        f"{prefix}_lower_{tier}_alive",
    ]
    return sum(1 for col in columns if row[col] == 0)


def build_structure_context(row: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    enemy_outer_destroyed = _destroyed_count(row, "enemy", "t1")
    enemy_inner_destroyed = _destroyed_count(row, "enemy", "t2")
    enemy_base_destroyed = _destroyed_count(row, "enemy", "t3")

    ally_outer_destroyed = _destroyed_count(row, "ally", "t1")
    ally_inner_destroyed = _destroyed_count(row, "ally", "t2")
    ally_base_destroyed = _destroyed_count(row, "ally", "t3")

    return (
        enemy_outer_destroyed,
        enemy_inner_destroyed,
        enemy_base_destroyed,
        ally_outer_destroyed,
        ally_inner_destroyed,
        ally_base_destroyed,
    )


def build_lord_context(row: dict[str, Any]) -> tuple[str, str]:
    return (row["lord_status"], row["lord_lane"])


def build_all_contexts(row: dict[str, Any]) -> dict[str, tuple]:
    return {
        "objective": build_objective_context(row),
        "advantage": build_advantage_context(row),
        "structure": build_structure_context(row),
        "lord": build_lord_context(row),
    }