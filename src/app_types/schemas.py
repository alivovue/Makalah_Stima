REQUIRED_COLUMNS = [
    "match_id",
    "game_time",
    "team",
    "opponent",
    "upper_lane_role",
    "mid_lane_role",
    "lower_lane_role",
    "team_gold",
    "enemy_gold",

    "ally_jungle_alive",
    "ally_roam_alive",
    "ally_mid_alive",
    "ally_exp_alive",
    "ally_gold_alive",

    "enemy_jungle_alive",
    "enemy_roam_alive",
    "enemy_mid_alive",
    "enemy_exp_alive",
    "enemy_gold_alive",

    "next_objective_type",
    "next_objective_timer_seconds",
    "objective_side",

    "lord_status",
    "lord_lane",

    "ally_upper_t1_alive",
    "ally_upper_t2_alive",
    "ally_upper_t3_alive",
    "ally_mid_t1_alive",
    "ally_mid_t2_alive",
    "ally_mid_t3_alive",
    "ally_lower_t1_alive",
    "ally_lower_t2_alive",
    "ally_lower_t3_alive",

    "enemy_upper_t1_alive",
    "enemy_upper_t2_alive",
    "enemy_upper_t3_alive",
    "enemy_mid_t1_alive",
    "enemy_mid_t2_alive",
    "enemy_mid_t3_alive",
    "enemy_lower_t1_alive",
    "enemy_lower_t2_alive",
    "enemy_lower_t3_alive",

    "action_location",
    "current_action",
]

INT_COLUMNS = [
    "team_gold",
    "enemy_gold",
    "next_objective_timer_seconds",

    "ally_jungle_alive",
    "ally_roam_alive",
    "ally_mid_alive",
    "ally_exp_alive",
    "ally_gold_alive",

    "enemy_jungle_alive",
    "enemy_roam_alive",
    "enemy_mid_alive",
    "enemy_exp_alive",
    "enemy_gold_alive",

    "ally_upper_t1_alive",
    "ally_upper_t2_alive",
    "ally_upper_t3_alive",
    "ally_mid_t1_alive",
    "ally_mid_t2_alive",
    "ally_mid_t3_alive",
    "ally_lower_t1_alive",
    "ally_lower_t2_alive",
    "ally_lower_t3_alive",

    "enemy_upper_t1_alive",
    "enemy_upper_t2_alive",
    "enemy_upper_t3_alive",
    "enemy_mid_t1_alive",
    "enemy_mid_t2_alive",
    "enemy_mid_t3_alive",
    "enemy_lower_t1_alive",
    "enemy_lower_t2_alive",
    "enemy_lower_t3_alive",
]

ALLY_ALIVE_COLUMNS = [
    "ally_jungle_alive",
    "ally_roam_alive",
    "ally_mid_alive",
    "ally_exp_alive",
    "ally_gold_alive",
]

ENEMY_ALIVE_COLUMNS = [
    "enemy_jungle_alive",
    "enemy_roam_alive",
    "enemy_mid_alive",
    "enemy_exp_alive",
    "enemy_gold_alive",
]

ALLY_TOWER_COLUMNS = [
    "ally_upper_t1_alive",
    "ally_upper_t2_alive",
    "ally_upper_t3_alive",
    "ally_mid_t1_alive",
    "ally_mid_t2_alive",
    "ally_mid_t3_alive",
    "ally_lower_t1_alive",
    "ally_lower_t2_alive",
    "ally_lower_t3_alive",
]

ENEMY_TOWER_COLUMNS = [
    "enemy_upper_t1_alive",
    "enemy_upper_t2_alive",
    "enemy_upper_t3_alive",
    "enemy_mid_t1_alive",
    "enemy_mid_t2_alive",
    "enemy_mid_t3_alive",
    "enemy_lower_t1_alive",
    "enemy_lower_t2_alive",
    "enemy_lower_t3_alive",
]