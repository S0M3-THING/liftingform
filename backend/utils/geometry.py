import math
import numpy as np


def landmark_to_array(landmark):
    return np.array(
        [
            landmark["x"],
            landmark["y"],
            landmark["z"]
        ],
        dtype=float
    )


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate angle ABC.

    Example:

        A
         \
          B ---- C

    The angle is measured at B.
    """

    a = landmark_to_array(point_a)
    b = landmark_to_array(point_b)
    c = landmark_to_array(point_c)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba == 0 or norm_bc == 0:
        return None

    cosine_angle = np.dot(ba, bc) / (
        norm_ba * norm_bc
    )

    cosine_angle = np.clip(
        cosine_angle,
        -1.0,
        1.0
    )

    angle = np.degrees(
        np.arccos(cosine_angle)
    )

    return float(angle)


def calculate_distance(point_a, point_b):

    a = landmark_to_array(point_a)
    b = landmark_to_array(point_b)

    return float(
        np.linalg.norm(a - b)
    )


def calculate_2d_distance(point_a, point_b):

    dx = point_a["x"] - point_b["x"]
    dy = point_a["y"] - point_b["y"]

    return float(
        math.sqrt(
            dx ** 2 + dy ** 2
        )
    )


def calculate_midpoint(point_a, point_b):

    a = landmark_to_array(point_a)
    b = landmark_to_array(point_b)

    midpoint = (a + b) / 2

    return {
        "x": float(midpoint[0]),
        "y": float(midpoint[1]),
        "z": float(midpoint[2])
    }


def average(values):

    values = [
        value
        for value in values
        if value is not None
    ]

    if not values:
        return None

    return float(
        np.mean(values)
    )


def median(values):

    values = [
        value
        for value in values
        if value is not None
    ]

    if not values:
        return None

    return float(
        np.median(values)
    )


def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0.0

    result = (
        (value - minimum)
        / (maximum - minimum)
    )

    return float(
        np.clip(result, 0.0, 1.0)
    )