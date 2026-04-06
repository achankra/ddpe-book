# friction_score.py
"""Developer Friction Score Calculator for DDPE"""
from dataclasses import dataclass
from typing import List

@dataclass
class FrictionSource:
    name: str
    score: float        # 1-10 severity
    weight: float       # 0-1 importance
    multiplier: float   # <1 = improving, >1 = worsening

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    @property
    def predictive_score(self) -> float:
        return self.score * self.weight * self.multiplier

def calculate_friction(sources: List[FrictionSource]):
    current = sum(s.weighted_score for s in sources)
    predictive = sum(s.predictive_score for s in sources)
    delta = ((predictive - current) / current) * 100 if current else 0

    print(f"Current Friction Score: {current:.2f}")
    print(f"Predictive Friction Score: {predictive:.2f}")
    if delta > 10:
        print(f"⚠ Warning: Predicted friction increase of {delta:.1f}%")
    elif delta < -10:
        print(f"✅ Predicted friction decrease of {abs(delta):.1f}%")

# Example usage
sources = [
    FrictionSource("Cross-team dependencies", 8, 0.3, 1.2),
    FrictionSource("Test flakiness", 6, 0.2, 0.9),
    FrictionSource("Security assessments", 7, 0.25, 1.1),
    FrictionSource("Legacy integration", 9, 0.15, 1.3),
    FrictionSource("Build times", 5, 0.1, 0.8),
]
calculate_friction(sources)
