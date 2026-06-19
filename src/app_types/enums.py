ACTIONS = [
    "PRESSURE_UPPER",
    "PRESSURE_MID",
    "PRESSURE_LOWER",
    "TURTLE_SETUP",
    "TAKE_TURTLE",
    "LORD_SETUP",
    "TAKE_LORD",
    "TAKE_UPPER_TURRET",
    "TAKE_MID_TURRET",
    "TAKE_LOWER_TURRET",
    "INVADE_JUNGLE",
    "TEAMFIGHT_SKIRMISH",
    "PICKOFF_GANK",
    "RESET_RECALL",
    "DEFEND_CLEAR",
    "NO_MAJOR_ACTION",
    "END_GAME",
]

ACTION_LOCATIONS = [
    "UPPER",
    "MID",
    "LOWER",
    "JUNGLE",
    "TURTLE_AREA",
    "LORD_AREA",
    "BASE",
    "NONE",
    "UNKNOWN",
]

OBJECTIVE_TYPES = ["TURTLE", "LORD", "NONE"]
OBJECTIVE_SIDES = ["UPPER", "LOWER", "NONE", "UNKNOWN"]

LORD_STATUSES = ["NONE", "ALLY_LORD", "ENEMY_LORD", "CONTESTED"]
LORD_LANES = ["UPPER", "MID", "LOWER", "NONE", "UNKNOWN"]

LANE_ROLES = ["EXP", "MID", "GOLD"]

TEAMS = ["BTR", "ONIC"]

START_DECISION = ("START", "NONE")


def get_candidate_decisions() -> list[tuple[str, str]]:
    """
    Candidate decisions are meaningful (action, location) pairs.
    This avoids impossible combinations like (TAKE_TURTLE, MID).
    """
    candidates: list[tuple[str, str]] = [
        ("PRESSURE_UPPER", "UPPER"),
        ("PRESSURE_MID", "MID"),
        ("PRESSURE_LOWER", "LOWER"),

        ("TURTLE_SETUP", "TURTLE_AREA"),
        ("TAKE_TURTLE", "TURTLE_AREA"),

        ("LORD_SETUP", "LORD_AREA"),
        ("TAKE_LORD", "LORD_AREA"),

        ("TAKE_UPPER_TURRET", "UPPER"),
        ("TAKE_MID_TURRET", "MID"),
        ("TAKE_LOWER_TURRET", "LOWER"),

        ("INVADE_JUNGLE", "JUNGLE"),

        ("RESET_RECALL", "NONE"),
        ("NO_MAJOR_ACTION", "NONE"),
        ("END_GAME", "BASE"),
    ]

    for location in ["UPPER", "MID", "LOWER", "JUNGLE", "TURTLE_AREA", "LORD_AREA", "BASE"]:
        candidates.append(("TEAMFIGHT_SKIRMISH", location))

    for location in ["UPPER", "MID", "LOWER", "JUNGLE"]:
        candidates.append(("PICKOFF_GANK", location))

    for location in ["UPPER", "MID", "LOWER", "BASE"]:
        candidates.append(("DEFEND_CLEAR", location))

    return candidates