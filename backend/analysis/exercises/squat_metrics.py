from backend.analysis.landmarks import (
    LEFT_HIP,
    RIGHT_HIP,
    LEFT_KNEE,
    RIGHT_KNEE,
    LEFT_ANKLE,
    RIGHT_ANKLE,
    LEFT_SHOULDER,
    RIGHT_SHOULDER
)

from backend.utils.geometry import (
    calculate_angle,
    calculate_midpoint,
    average
)


def get_average_knee_angle(landmarks):

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

    return average([
        left_angle,
        right_angle
    ])


def get_left_knee_angle(landmarks):

    return calculate_angle(
        landmarks[LEFT_HIP],
        landmarks[LEFT_KNEE],
        landmarks[LEFT_ANKLE]
    )


def get_right_knee_angle(landmarks):

    return calculate_angle(
        landmarks[RIGHT_HIP],
        landmarks[RIGHT_KNEE],
        landmarks[RIGHT_ANKLE]
    )


def get_hip_height(landmarks):

    hip = calculate_midpoint(
        landmarks[LEFT_HIP],
        landmarks[RIGHT_HIP]
    )

    return hip["y"]


def get_shoulder_hip_alignment(
    landmarks
):

    shoulder = calculate_midpoint(
        landmarks[LEFT_SHOULDER],
        landmarks[RIGHT_SHOULDER]
    )

    hip = calculate_midpoint(
        landmarks[LEFT_HIP],
        landmarks[RIGHT_HIP]
    )

    return {
        "x": shoulder["x"] - hip["x"],
        "y": shoulder["y"] - hip["y"],
        "z": shoulder["z"] - hip["z"]
    }