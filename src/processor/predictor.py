from typing import Any

from processor.greedy_scorer import GreedyScorer


class Predictor:
    def __init__(self, scorer: GreedyScorer) -> None:
        self.scorer = scorer

    def predict_top_k(self, row: dict[str, Any], k: int = 5) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for candidate in self.scorer.candidate_decisions:
            breakdown = self.scorer.score(row, candidate)

            results.append({
                "action": candidate[0],
                "location": candidate[1],
                "score": breakdown["final_score"],
                "breakdown": breakdown,
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:k]