import numpy as np

from backend.analysis.landmarks import (
    LEFT_HIP,
    RIGHT_HIP,
    LEFT_KNEE,
    RIGHT_KNEE,
    LEFT_ANKLE,
    RIGHT_ANKLE
)

from backend.utils.geometry import (
    calculate_angle
)

from backend.models.analysis import (
    AnalysisResult,
    Issue
)


class SquatAnalyzer:

    def get_knee_angle(
        self,
        landmarks
    ):

        left_angle = calculate_angle(
            landmarks[LEFT_HIP],
            landmarks[LEFT_KNEE],
            landmarks[LEFT_ANKLE]
        )

        right_angle = calculate_angle(
            landmarks[RIGHT_HIP],
            landmarks[RIGHT_KNEE],
            landmarks[RIGHT_ANKLE]
        )

        angles = [
            angle
            for angle in [
                left_angle,
                right_angle
            ]
            if angle is not None
        ]

        if not angles:
            return None

        return float(
            np.mean(angles)
        )


    def analyze(
        self,
        front_pose=None,
        side_pose=None,
        back_pose=None
    ):

        pose_frames = (
            side_pose
            or front_pose
            or back_pose
            or []
        )

        if not pose_frames:

            return AnalysisResult(
                exercise="squat",
                score=0,
                metrics={},
                issues=[
                    Issue(
                        type="insufficient_data",
                        severity="high",
                        description=(
                            "No usable body "
                            "movement was detected."
                        )
                    )
                ],
                recommendations=[
                    "Make sure your full body "
                    "is visible throughout "
                    "the video."
                ]
            )


        knee_angles = []

        for frame in pose_frames:

            angle = self.get_knee_angle(
                frame["landmarks"]
            )

            if angle is not None:

                knee_angles.append(
                    angle
                )


        if not knee_angles:

            return AnalysisResult(
                exercise="squat",
                score=0,
                metrics={},
                issues=[
                    Issue(
                        type="insufficient_data",
                        severity="high",
                        description=(
                            "We could not calculate "
                            "your knee angle."
                        )
                    )
                ],
                recommendations=[
                    "Make sure your legs "
                    "are clearly visible."
                ]
            )


        minimum_angle = min(
            knee_angles
        )

        maximum_angle = max(
            knee_angles
        )


        # --------------------------------
        # DEPTH
        # --------------------------------

        if minimum_angle <= 95:

            depth_score = 100

        elif minimum_angle <= 105:

            depth_score = 90

        elif minimum_angle <= 115:

            depth_score = 75

        elif minimum_angle <= 125:

            depth_score = 60

        else:

            depth_score = 40


        issues = []

        recommendations = []


        if minimum_angle > 115:

            issues.append(
                Issue(
                    type="insufficient_depth",
                    severity="moderate",
                    description=(
                        "Your knees do not appear "
                        "to bend deeply enough "
                        "during the squat."
                    )
                )
            )

            recommendations.append(
                "Try gradually increasing "
                "your squat depth while "
                "keeping your feet stable "
                "and maintaining control."
            )


        # --------------------------------
        # MOVEMENT
        # --------------------------------

        movement_range = (
            maximum_angle
            - minimum_angle
        )


        if movement_range < 25:

            issues.append(
                Issue(
                    type="limited_movement",
                    severity="moderate",
                    description=(
                        "There is relatively "
                        "little knee movement "
                        "in this video."
                    )
                )
            )

            recommendations.append(
                "Make sure the video contains "
                "several complete squat "
                "repetitions."
            )


        # --------------------------------
        # SCORE
        # --------------------------------

        score = depth_score


        return AnalysisResult(
            exercise="squat",
            score=score,
            metrics={
                "minimum_knee_angle":
                    minimum_angle,

                "maximum_knee_angle":
                    maximum_angle,

                "knee_movement_range":
                    movement_range,

                "pose_frames":
                    len(pose_frames)
            },
            issues=issues,
            recommendations=recommendations
        )