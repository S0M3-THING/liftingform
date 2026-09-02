import numpy as np

from backend.analysis.landmarks import (
    LEFT_HIP,
    RIGHT_HIP,
    LEFT_KNEE,
    RIGHT_KNEE,
    LEFT_ANKLE,
    RIGHT_ANKLE
)

from backend.analysis.exercises.squat_metrics import (
    get_average_knee_angle,
    get_left_knee_angle,
    get_right_knee_angle
)

from backend.analysis.rep_detector import (
    detect_repetitions
)

from backend.analysis.scoring import (
    clamp
)

from backend.models.analysis import (
    AnalysisResult,
    Issue
)


class SquatAnalyzer:

    def build_knee_signal(
        self,
        pose_frames
    ):

        signal = []

        for frame in pose_frames:

            landmarks = frame[
                "landmarks"
            ]

            angle = get_average_knee_angle(
                landmarks
            )

            if angle is not None:
                signal.append(angle)

        return signal

    def analyze_depth(
        self,
        knee_signal
    ):

        if not knee_signal:

            return {
                "score": 0,
                "minimum_angle": None
            }

        minimum_angle = min(
            knee_signal
        )

        # Approximate prototype scoring.
        #
        # ~90 degrees = excellent depth
        # ~110 degrees = moderate
        # >130 degrees = shallow

        if minimum_angle <= 95:
            score = 100

        elif minimum_angle <= 105:
            score = 90

        elif minimum_angle <= 115:
            score = 75

        elif minimum_angle <= 125:
            score = 60

        else:
            score = 40

        return {
            "score": score,
            "minimum_angle": minimum_angle
        }

    def analyze_symmetry(
        self,
        pose_frames
    ):

        differences = []

        for frame in pose_frames:

            landmarks = frame[
                "landmarks"
            ]

            left = get_left_knee_angle(
                landmarks
            )

            right = get_right_knee_angle(
                landmarks
            )

            if left is None or right is None:
                continue

            differences.append(
                abs(left - right)
            )

        if not differences:

            return {
                "score": 0,
                "average_difference": None
            }

        average_difference = float(
            np.mean(differences)
        )

        score = clamp(
            100 - (
                average_difference * 3
            )
        )

        return {
            "score": score,
            "average_difference": (
                average_difference
            )
        }

    def analyze_rep_consistency(
        self,
        repetitions,
        knee_signal
    ):

        if len(repetitions) < 2:

            return {
                "score": 100,
                "depth_variation": 0
            }

        depths = []

        for rep in repetitions:

            bottom = rep["bottom"]

            if bottom < len(knee_signal):

                depths.append(
                    knee_signal[bottom]
                )

        if len(depths) < 2:

            return {
                "score": 100,
                "depth_variation": 0
            }

        variation = float(
            np.std(depths)
        )

        score = clamp(
            100 - variation * 5
        )

        return {
            "score": score,
            "depth_variation": variation
        }

    def analyze(
        self,
        front_pose=None,
        side_pose=None,
        back_pose=None
    ):

        issues = []
        recommendations = []

        metrics = {}

        # --------------------------------
        # SIDE VIEW
        # --------------------------------

        repetitions = []

        if side_pose:

            knee_signal = (
                self.build_knee_signal(
                    side_pose
                )
            )

            depth = self.analyze_depth(
                knee_signal
            )

            metrics["depth"] = (
                depth["score"]
            )

            minimum_angle = (
                depth["minimum_angle"]
            )

            if minimum_angle is not None:

                if minimum_angle > 115:

                    issues.append(
                        Issue(
                            type="insufficient_depth",
                            severity="moderate",
                            description=(
                                "Your squat appears "
                                "to be relatively shallow."
                            )
                        )
                    )

                    recommendations.append(
                        "Try gradually increasing "
                        "your squat depth while "
                        "maintaining control."
                    )

            repetitions = (
                detect_repetitions(
                    knee_signal
                )
            )

            consistency = (
                self.analyze_rep_consistency(
                    repetitions,
                    knee_signal
                )
            )

            metrics["rep_consistency"] = (
                consistency["score"]
            )

            if (
                consistency["depth_variation"]
                > 5
            ):

                issues.append(
                    Issue(
                        type="inconsistent_depth",
                        severity="mild",
                        description=(
                            "Your squat depth "
                            "varies between repetitions."
                        )
                    )
                )

                recommendations.append(
                    "Try to reach a similar "
                    "depth on every repetition."
                )

        # --------------------------------
        # FRONT VIEW
        # --------------------------------

        if front_pose:

            symmetry = (
                self.analyze_symmetry(
                    front_pose
                )
            )

            metrics["symmetry"] = (
                symmetry["score"]
            )

            if (
                symmetry[
                    "average_difference"
                ] is not None
                and
                symmetry[
                    "average_difference"
                ] > 8
            ):

                issues.append(
                    Issue(
                        type="left_right_asymmetry",
                        severity="moderate",
                        description=(
                            "Your left and right "
                            "legs are moving somewhat "
                            "differently."
                        )
                    )
                )

                recommendations.append(
                    "Focus on keeping your "
                    "weight balanced between "
                    "both legs."
                )

        # --------------------------------
        # BACK VIEW
        # --------------------------------

        if back_pose:

            back_symmetry = (
                self.analyze_symmetry(
                    back_pose
                )
            )

            # If front symmetry already exists,
            # average the two views.

            if "symmetry" in metrics:

                metrics["symmetry"] = (
                    metrics["symmetry"]
                    + back_symmetry["score"]
                ) / 2

            else:

                metrics["symmetry"] = (
                    back_symmetry["score"]
                )

        # --------------------------------
        # NO DATA
        # --------------------------------

        if not metrics:

            return AnalysisResult(
                exercise="squat",
                score=0,
                metrics={},
                issues=[
                    Issue(
                        type="insufficient_data",
                        severity="high",
                        description=(
                            "We could not detect "
                            "enough body movement "
                            "to analyze this squat."
                        )
                    )
                ],
                recommendations=[
                    "Make sure your entire body "
                    "is visible and the camera "
                    "remains stationary."
                ]
            )

        # --------------------------------
        # SCORE
        # --------------------------------

        weights = {
            "depth": 0.40,
            "symmetry": 0.30,
            "rep_consistency": 0.30
        }

        total = 0
        total_weight = 0

        for metric, weight in weights.items():

            if metric in metrics:

                total += (
                    metrics[metric]
                    * weight
                )

                total_weight += weight

        if total_weight > 0:

            score = (
                total / total_weight
            )

        else:

            score = 0

        return AnalysisResult(
            exercise="squat",
            score=score,
            metrics={
                **metrics,
                "repetitions": float(
                    len(repetitions)
                )
            },
            issues=issues,
            recommendations=recommendations
        )