from backend.utils.geometry import calculate_angle


def test_right_angle():

    a = {
        "x": 0,
        "y": 1,
        "z": 0
    }

    b = {
        "x": 0,
        "y": 0,
        "z": 0
    }

    c = {
        "x": 1,
        "y": 0,
        "z": 0
    }

    angle = calculate_angle(
        a,
        b,
        c
    )

    assert 89 <= angle <= 91