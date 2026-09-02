import numpy as np


def smooth_signal(
    signal,
    window=7
):

    signal = np.asarray(
        signal,
        dtype=float
    )

    if len(signal) < 3:
        return signal

    window = min(
        window,
        len(signal)
    )

    if window % 2 == 0:
        window -= 1

    if window < 3:
        return signal

    kernel = np.ones(window) / window

    return np.convolve(
        signal,
        kernel,
        mode="same"
    )


def detect_repetitions(
    signal,
    down_threshold=115,
    up_threshold=155,
    minimum_rep_frames=8
):
    """
    Detect repetitions from a movement-angle signal.

    For squats:

        standing
            ↓
        descending
            ↓
          bottom
            ↓
        ascending
            ↓
        standing
    """

    if signal is None:
        return []

    if len(signal) < minimum_rep_frames:
        return []

    signal = smooth_signal(
        signal,
        window=7
    )

    repetitions = []

    state = "standing"

    start_index = None
    bottom_index = None

    for i, angle in enumerate(signal):

        if np.isnan(angle):
            continue

        if state == "standing":

            if angle < down_threshold:

                state = "descending"

                start_index = i
                bottom_index = i

        elif state == "descending":

            if angle < signal[bottom_index]:

                bottom_index = i

            if angle < down_threshold:

                continue

            if angle > up_threshold:

                if (
                    i - start_index
                    >= minimum_rep_frames
                ):

                    repetitions.append({
                        "start": start_index,
                        "bottom": bottom_index,
                        "end": i
                    })

                    state = "standing"
                    start_index = None
                    bottom_index = None

    return repetitions