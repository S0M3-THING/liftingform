from backend.models.analysis import (
    AnalysisResult,
    Issue
)


class DeadliftAnalyzer:

    def analyze(
        self,
        front_pose=None,
        side_pose=None,
        back_pose=None
    ):

        issues = []
        recommendations = []

        metrics = {}

        if not side_pose:

            return AnalysisResult(
                exercise="deadlift",
                score=0,
                metrics={},
                issues=[
                    Issue(
                        type="missing_side_view",
                        severity="high",
                        description=(
                            "A side view is required "
                            "for reliable deadlift analysis."
                        )
                    )
                ],
                recommendations=[
                    "Upload a clear side-view video "
                    "showing your entire body."
                ]
            )

        metrics["technique"] = 75.0

        return AnalysisResult(
            exercise="deadlift",
            score=75,
            metrics=metrics,
            issues=issues,
            recommendations=recommendations
        )