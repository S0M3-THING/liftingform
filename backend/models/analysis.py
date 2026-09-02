from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class Issue:

    type: str
    severity: str
    description: str


@dataclass
class AnalysisResult:

    exercise: str

    score: float

    metrics: Dict[str, Any] = field(
        default_factory=dict
    )

    issues: List[Issue] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    def to_dict(self):

        formatted_metrics = {}

        for key, value in self.metrics.items():

            if isinstance(
                value,
                (int, float)
            ):

                formatted_metrics[key] = round(
                    value,
                    1
                )

            else:

                formatted_metrics[key] = value

        return {
            "exercise": self.exercise,

            "score": round(
                self.score,
                1
            ),

            "metrics": formatted_metrics,

            "issues": [
                {
                    "type": issue.type,
                    "severity": issue.severity,
                    "description": (
                        issue.description
                    )
                }
                for issue in self.issues
            ],

            "recommendations": (
                self.recommendations
            )
        }