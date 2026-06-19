from pathlib import Path
from typing import Any

from app_types.enums import (
    ACTIONS,
    ACTION_LOCATIONS,
    START_DECISION,
)
from app_types.schemas import (
    ALLY_ALIVE_COLUMNS,
    ENEMY_ALIVE_COLUMNS,
    ALLY_TOWER_COLUMNS,
    ENEMY_TOWER_COLUMNS,
)
from parser.csv_parser import read_csv_data
from processor.context_builder import build_all_contexts
from processor.greedy_scorer import GreedyScorer
from processor.predictor import Predictor
from processor.preprocessor import preprocess_rows


DATA_PATH = Path("data/game_data.csv")


def ask_menu(prompt: str, options: list[str], default_index: int | None = None) -> str:
    """
    Numbered menu input.
    Example:
    1. BTR
    2. ONIC
    """
    if not options:
        raise ValueError(f"No options available for: {prompt}")

    while True:
        print(f"\n{prompt}")
        for index, option in enumerate(options, start=1):
            marker = " [default]" if default_index == index else ""
            print(f"{index}. {option}{marker}")

        value = input("Choose number: ").strip()

        if value == "" and default_index is not None:
            return options[default_index - 1]

        try:
            choice = int(value)
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass

        print("Invalid choice. Please choose one of the numbers above.")


def ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{suffix}: ").strip().lower()

        if value == "" and default is not None:
            return default

        if value in ["alive", "available", "spawned"]:
            return 0

        if value in ["unknown", "none", "nothing", "no time", "n/a"]:
            return -1

        try:
            if value.endswith("k"):
                return int(float(value[:-1]) * 1000)
            return int(value)
        except ValueError:
            print("Invalid number. Examples: 5200, 12.1k, 0, -1")


def ask_binary(prompt: str, default: int = 1) -> int:
    while True:
        value = input(f"{prompt} (1/0) [{default}]: ").strip()

        if value == "":
            return default

        if value in ["1", "0"]:
            return int(value)

        print("Invalid input. Use 1 or 0.")


def ask_game_time_seconds() -> int:
    while True:
        value = input("Current game time (MM:SS): ").strip()

        if ":" not in value:
            print("Invalid format. Use MM:SS, for example 09:35.")
            continue

        try:
            minutes, seconds = value.split(":", 1)
            return int(minutes) * 60 + int(seconds)
        except ValueError:
            print("Invalid format. Use MM:SS, for example 09:35.")


def ask_previous_decision() -> tuple[str, str]:
    use_previous = ask_menu(
        "Do you know the previous macro decision?",
        ["NO", "YES"],
        default_index=1,
    )

    if use_previous == "NO":
        return START_DECISION

    action = ask_menu("Previous action", ACTIONS)
    location = ask_menu("Previous action location", ACTION_LOCATIONS)

    return (action, location)


def get_available_teams(rows: list[dict[str, Any]]) -> list[str]:
    """
    Only teams that appear as `team` in the dataset are valid prediction targets.
    """
    return sorted({row["team"] for row in rows})


def get_available_opponents(rows: list[dict[str, Any]], selected_team: str) -> list[str]:
    """
    Only opponents that appear against the selected team are valid.
    """
    return sorted({row["opponent"] for row in rows if row["team"] == selected_team})


def ask_team_and_opponent(rows: list[dict[str, Any]]) -> tuple[str, str]:
    available_teams = get_available_teams(rows)
    team = ask_menu("Choose team to predict", available_teams)

    available_opponents = get_available_opponents(rows, team)
    opponent = ask_menu(f"Choose opponent for {team}", available_opponents)

    return team, opponent


def ask_laning_roles() -> tuple[str, str, str]:
    """
    Mid is always MID.
    Only upper/lower role swap is asked.
    """
    choice = ask_menu(
        "Choose lane role setup",
        [
            "Upper = EXP, Mid = MID, Lower = GOLD",
            "Upper = GOLD, Mid = MID, Lower = EXP",
        ],
    )

    if choice == "Upper = EXP, Mid = MID, Lower = GOLD":
        return "EXP", "MID", "GOLD"

    return "GOLD", "MID", "EXP"


def ask_objective_side(prompt: str) -> str:
    side = ask_menu(prompt, ["UPPER / TOP", "LOWER / BOT"])

    if side == "UPPER / TOP":
        return "UPPER"

    return "LOWER"


def ask_turtle_info(row: dict[str, Any]) -> None:
    row["next_objective_type"] = "TURTLE"
    row["lord_status"] = "NONE"
    row["lord_lane"] = "NONE"

    turtle_state = ask_menu(
        "Turtle state",
        [
            "Spawned / alive now",
            "Not spawned yet / waiting",
            "No information",
        ],
    )

    if turtle_state == "Spawned / alive now":
        row["next_objective_timer_seconds"] = 0
        row["objective_side"] = ask_objective_side("Where is Turtle?")

    elif turtle_state == "Not spawned yet / waiting":
        row["next_objective_timer_seconds"] = ask_int("Seconds until Turtle spawns")
        row["objective_side"] = ask_objective_side("Where will Turtle spawn?")

    else:
        row["next_objective_timer_seconds"] = -1
        row["objective_side"] = "UNKNOWN"


def ask_lord_info(row: dict[str, Any], team: str, opponent: str) -> None:
    row["next_objective_type"] = "LORD"

    lord_state = ask_menu(
        "Lord state",
        [
            "Spawned / alive now",
            "Not spawned yet / waiting",
            "Already taken",
            "No information",
        ],
    )

    if lord_state == "Spawned / alive now":
        row["next_objective_timer_seconds"] = 0
        row["objective_side"] = ask_objective_side("Where is Lord?")
        row["lord_status"] = "NONE"
        row["lord_lane"] = "NONE"

    elif lord_state == "Not spawned yet / waiting":
        row["next_objective_timer_seconds"] = ask_int("Seconds until Lord spawns")
        row["objective_side"] = ask_objective_side("Where will Lord spawn?")
        row["lord_status"] = "NONE"
        row["lord_lane"] = "NONE"

    elif lord_state == "Already taken":
        taker = ask_menu(
            "Who took Lord?",
            [
                f"{team} / ally",
                f"{opponent} / enemy",
            ],
        )

        if taker == f"{team} / ally":
            row["lord_status"] = "ALLY_LORD"
        else:
            row["lord_status"] = "ENEMY_LORD"

        row["lord_lane"] = ask_menu(
            "Which lane is Lord walking?",
            ["UPPER", "MID", "LOWER", "UNKNOWN"],
        )

        row["next_objective_timer_seconds"] = -1
        row["objective_side"] = "NONE"

    else:
        row["next_objective_timer_seconds"] = -1
        row["objective_side"] = "UNKNOWN"
        row["lord_status"] = "NONE"
        row["lord_lane"] = "UNKNOWN"


def ask_objective_info(row: dict[str, Any], team: str, opponent: str) -> None:
    objective_type = ask_menu(
        "Next major objective",
        [
            "Turtle",
            "Lord",
        ],
    )

    if objective_type == "Turtle":
        ask_turtle_info(row)
    else:
        ask_lord_info(row, team, opponent)


def build_user_row(historical_rows: list[dict[str, Any]]) -> dict[str, Any]:
    print("\n=== Input Current Game State ===")

    team, opponent = ask_team_and_opponent(historical_rows)
    upper_lane_role, mid_lane_role, lower_lane_role = ask_laning_roles()

    team_gold = ask_int(f"{team} gold")
    enemy_gold = ask_int(f"{opponent} gold")

    row: dict[str, Any] = {
        "match_id": "USER_INPUT",
        "game_time": "USER_INPUT",
        "game_time_seconds": ask_game_time_seconds(),
        "team": team,
        "opponent": opponent,
        "upper_lane_role": upper_lane_role,
        "mid_lane_role": mid_lane_role,
        "lower_lane_role": lower_lane_role,
        "team_gold": team_gold,
        "enemy_gold": enemy_gold,
    }

    print("\nAlive state. Press Enter to use default 1/alive.")

    for col in ALLY_ALIVE_COLUMNS:
        row[col] = ask_binary(col, 1)

    for col in ENEMY_ALIVE_COLUMNS:
        row[col] = ask_binary(col, 1)

    ask_objective_info(row, team, opponent)

    print("\nTower state. Press Enter to use default 1/standing.")

    for col in ALLY_TOWER_COLUMNS:
        row[col] = ask_binary(col, 1)

    for col in ENEMY_TOWER_COLUMNS:
        row[col] = ask_binary(col, 1)

    row["previous_decision"] = ask_previous_decision()

    contexts = build_all_contexts(row)
    row["objective_context"] = contexts["objective"]
    row["advantage_context"] = contexts["advantage"]
    row["structure_context"] = contexts["structure"]
    row["lord_context"] = contexts["lord"]

    return row


def print_predictions(predictions: list[dict[str, Any]]) -> None:
    print("\n=== Top 5 Predicted Macro Decisions ===")

    for index, pred in enumerate(predictions, start=1):
        breakdown = pred["breakdown"]

        print(f"\n{index}. {pred['action']} at {pred['location']}")
        print(f"   Final Score       : {pred['score']:.6f}")
        print(f"   Transition        : {breakdown['transition']:.6f}")
        print(f"   Team Preference   : {breakdown['team_preference']:.6f}")
        print(f"   Objective Context : {breakdown['objective_context']:.6f}")
        print(f"   Advantage Context : {breakdown['advantage_context']:.6f}")
        print(f"   Structure Context : {breakdown['structure_context']:.6f}")
        print(f"   Lord Context      : {breakdown['lord_context']:.6f}")


def main() -> None:
    print("Loading historical data...")

    raw_rows = read_csv_data(DATA_PATH)
    processed_rows = preprocess_rows(raw_rows)

    scorer = GreedyScorer()
    scorer.fit(processed_rows)

    predictor = Predictor(scorer)

    print("Historical data loaded successfully.")
    print(f"Available teams: {', '.join(get_available_teams(processed_rows))}")

    while True:
        user_row = build_user_row(processed_rows)
        predictions = predictor.predict_top_k(user_row, k=5)
        print_predictions(predictions)

        again = ask_menu(
            "Predict another state?",
            ["NO", "YES"],
            default_index=1,
        )

        if again == "NO":
            break


if __name__ == "__main__":
    main()