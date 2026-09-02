from backend.models.analysis import (
    AnalysisResult,
    Issue
)


class BenchPressAnalyzer:

    def analyze(
        self,
        front_pose=None,
        side_pose=None,
        back_pose=None
    ):

        if not side_pose:

            return AnalysisResult(
                exercise="bench_press",
                score=0,
                metrics={},
                issues=[
                    Issue(
                        type="missing_side_view",
                        severity="high",
                        description=(
                            "A side view is required "
                            "for bench press analysis."
                        )
                    )
                ],
                recommendations=[
                    "Upload a clear side-view video."
                ]
            )

        return AnalysisResult(
            exercise="bench_press",
            score=75,
            metrics={
                "technique": 75
            },
            issues=[],
            recommendations=[]
        )