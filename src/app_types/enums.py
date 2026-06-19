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


ACTION_LOCATION_OPTIONS = {
    "PRESSURE_UPPER": ["UPPER"],
    "PRESSURE_MID": ["MID"],
    "PRESSURE_LOWER": ["LOWER"],

    "TURTLE_SETUP": ["TURTLE_AREA"],
    "TAKE_TURTLE": ["TURTLE_AREA"],

    "LORD_SETUP": ["LORD_AREA"],
    "TAKE_LORD": ["LORD_AREA"],

    "TAKE_UPPER_TURRET": ["UPPER"],
    "TAKE_MID_TURRET": ["MID"],
    "TAKE_LOWER_TURRET": ["LOWER"],

    "INVADE_JUNGLE": ["JUNGLE"],

    "TEAMFIGHT_SKIRMISH": [
        "UPPER",
        "MID",
        "LOWER",
        "JUNGLE",
        "TURTLE_AREA",
        "LORD_AREA",
        "BASE",
    ],

    "PICKOFF_GANK": [
        "UPPER",
        "MID",
        "LOWER",
        "JUNGLE",
    ],

    "RESET_RECALL": ["NONE"],

    "DEFEND_CLEAR": [
        "UPPER",
        "MID",
        "LOWER",
        "BASE",
    ],

    "NO_MAJOR_ACTION": ["NONE"],
    "END_GAME": ["BASE"],
}


def get_locations_for_action(action: str) -> list[str]:
    """
    Return valid locations for a given macro action.
    Some actions have fixed locations, while others need location choice.
    """
    return ACTION_LOCATION_OPTIONS.get(action, ["UNKNOWN"])


def get_candidate_decisions() -> list[tuple[str, str]]:
    """
    Generate all valid candidate decisions as:
    (current_action, action_location)
    """
    candidates: list[tuple[str, str]] = []

    for action in ACTIONS:
        for location in get_locations_for_action(action):
            candidates.append((action, location))

    return candidates