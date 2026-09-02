from backend.analysis.exercises.squathard import (
    SquatAnalyzer
)

from backend.analysis.exercises.deadlift import (
    DeadliftAnalyzer
)

from backend.analysis.exercises.bench_press import (
    BenchPressAnalyzer
)


class ExerciseAnalyzer:

    def __init__(self):

        self.analyzers = {
            "squat": SquatAnalyzer(),
            "deadlift": DeadliftAnalyzer(),
            "bench_press": BenchPressAnalyzer()
        }

    def analyze(
        self,
        exercise,
        front_pose=None,
        side_pose=None,
        back_pose=None
    ):

        exercise = (
            exercise
            .lower()
            .strip()
        )

        if exercise not in self.analyzers:

            raise ValueError(
                f"Unsupported exercise: {exercise}"
            )

        return self.analyzers[
            exercise
        ].analyze(
            front_pose=front_pose,
            side_pose=side_pose,
            back_pose=back_pose
        )