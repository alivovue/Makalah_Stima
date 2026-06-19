from collections import Counter, defaultdict
from typing import Any

from app_types.enums import get_candidate_decisions


class GreedyScorer:
    WEIGHTS = {
        "transition": 0.30,
        "team_preference": 0.15,
        "objective_context": 0.20,
        "advantage_context": 0.15,
        "structure_context": 0.10,
        "lord_context": 0.10,
    }

    def __init__(self) -> None:
        self.candidate_decisions = get_candidate_decisions()
        self.n_candidates = len(self.candidate_decisions)

        self.team_preference_counts: dict[str, Counter] = defaultdict(Counter)
        self.team_total_counts: Counter = Counter()

        self.global_preference_counts: Counter = Counter()
        self.global_total_count = 0

        self.transition_counts: dict[str, dict[tuple[str, str], Counter]] = defaultdict(lambda: defaultdict(Counter))
        self.transition_totals: dict[str, Counter] = defaultdict(Counter)

        self.global_transition_counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
        self.global_transition_totals: Counter = Counter()

        self.context_counts: dict[str, dict[str, dict[tuple, Counter]]] = {
            "objective": defaultdict(lambda: defaultdict(Counter)),
            "advantage": defaultdict(lambda: defaultdict(Counter)),
            "structure": defaultdict(lambda: defaultdict(Counter)),
            "lord": defaultdict(lambda: defaultdict(Counter)),
        }

        self.context_totals: dict[str, dict[str, Counter]] = {
            "objective": defaultdict(Counter),
            "advantage": defaultdict(Counter),
            "structure": defaultdict(Counter),
            "lord": defaultdict(Counter),
        }

        self.global_context_counts: dict[str, dict[tuple, Counter]] = {
            "objective": defaultdict(Counter),
            "advantage": defaultdict(Counter),
            "structure": defaultdict(Counter),
            "lord": defaultdict(Counter),
        }

        self.global_context_totals: dict[str, Counter] = {
            "objective": Counter(),
            "advantage": Counter(),
            "structure": Counter(),
            "lord": Counter(),
        }

    def fit(self, rows: list[dict[str, Any]]) -> None:
        for row in rows:
            team = row["team"]
            decision = row["decision"]
            previous_decision = row["previous_decision"]

            self.team_preference_counts[team][decision] += 1
            self.team_total_counts[team] += 1

            self.global_preference_counts[decision] += 1
            self.global_total_count += 1

            self.transition_counts[team][previous_decision][decision] += 1
            self.transition_totals[team][previous_decision] += 1

            self.global_transition_counts[previous_decision][decision] += 1
            self.global_transition_totals[previous_decision] += 1

            for context_name in ["objective", "advantage", "structure", "lord"]:
                context_key = row[f"{context_name}_context"]

                self.context_counts[context_name][team][context_key][decision] += 1
                self.context_totals[context_name][team][context_key] += 1

                self.global_context_counts[context_name][context_key][decision] += 1
                self.global_context_totals[context_name][context_key] += 1

    def _smooth(self, count: int, total: int) -> float:
        return (count + 1) / (total + self.n_candidates)

    def team_preference_score(self, team: str, decision: tuple[str, str]) -> float:
        team_total = self.team_total_counts[team]

        if team_total > 0:
            return self._smooth(self.team_preference_counts[team][decision], team_total)

        if self.global_total_count > 0:
            return self._smooth(self.global_preference_counts[decision], self.global_total_count)

        return 1 / self.n_candidates

    def transition_score(
        self,
        team: str,
        previous_decision: tuple[str, str],
        decision: tuple[str, str],
    ) -> float:
        team_total = self.transition_totals[team][previous_decision]

        if team_total > 0:
            count = self.transition_counts[team][previous_decision][decision]
            return self._smooth(count, team_total)

        global_total = self.global_transition_totals[previous_decision]

        if global_total > 0:
            count = self.global_transition_counts[previous_decision][decision]
            return self._smooth(count, global_total)

        return 1 / self.n_candidates

    def context_score(
        self,
        context_name: str,
        team: str,
        context_key: tuple,
        decision: tuple[str, str],
    ) -> float:
        team_total = self.context_totals[context_name][team][context_key]

        if team_total > 0:
            count = self.context_counts[context_name][team][context_key][decision]
            return self._smooth(count, team_total)

        global_total = self.global_context_totals[context_name][context_key]

        if global_total > 0:
            count = self.global_context_counts[context_name][context_key][decision]
            return self._smooth(count, global_total)

        return 1 / self.n_candidates

    def score(self, row: dict[str, Any], candidate: tuple[str, str]) -> dict[str, float]:
        team = row["team"]

        transition = self.transition_score(team, row["previous_decision"], candidate)
        preference = self.team_preference_score(team, candidate)
        objective = self.context_score("objective", team, row["objective_context"], candidate)
        advantage = self.context_score("advantage", team, row["advantage_context"], candidate)
        structure = self.context_score("structure", team, row["structure_context"], candidate)
        lord = self.context_score("lord", team, row["lord_context"], candidate)

        final_score = (
            self.WEIGHTS["transition"] * transition
            + self.WEIGHTS["team_preference"] * preference
            + self.WEIGHTS["objective_context"] * objective
            + self.WEIGHTS["advantage_context"] * advantage
            + self.WEIGHTS["structure_context"] * structure
            + self.WEIGHTS["lord_context"] * lord
        )

        return {
            "transition": transition,
            "team_preference": preference,
            "objective_context": objective,
            "advantage_context": advantage,
            "structure_context": structure,
            "lord_context": lord,
            "final_score": final_score,
        }