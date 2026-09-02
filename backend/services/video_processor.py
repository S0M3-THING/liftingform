import cv2
import os


ALLOWED_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi"
}

MAX_FILE_SIZE = (
    100 * 1024 * 1024
)

MAX_DURATION_SECONDS = 60


def validate_video(video_path):

    if not os.path.exists(video_path):

        raise ValueError(
            "Video does not exist."
        )

    extension = os.path.splitext(
        video_path
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise ValueError(
            "Unsupported video format. "
            "Use MP4, MOV, or AVI."
        )

    file_size = os.path.getsize(
        video_path
    )

    if file_size > MAX_FILE_SIZE:

        raise ValueError(
            "Video is too large. "
            "Maximum size is 100 MB."
        )

    cap = cv2.VideoCapture(
        video_path
    )

    if not cap.isOpened():

        raise ValueError(
            "Unable to open video."
        )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    frame_count = cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )

    if fps <= 0:

        cap.release()

        raise ValueError(
            "Could not determine video FPS."
        )

    duration = frame_count / fps

    cap.release()

    if duration > MAX_DURATION_SECONDS:

        raise ValueError(
            "Video is too long. "
            "Maximum duration is 60 seconds."
        )

    return {
        "fps": fps,
        "frame_count": int(
            frame_count
        ),
        "duration": duration
    }