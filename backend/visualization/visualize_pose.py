import cv2
import mediapipe as mp

from backend.services.pose_estimator import (
    PoseEstimator
)


def visualize_video(
    input_path,
    output_path
):

    estimator = PoseEstimator()

    cap = cv2.VideoCapture(
        input_path
    )

    if not cap.isOpened():

        estimator.close()

        raise ValueError(
            "Could not open input video."
        )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 30

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    mp_drawing = (
        mp.solutions.drawing_utils
    )

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = estimator.pose.process(
            rgb
        )

        if result.pose_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                estimator.mp_pose.POSE_CONNECTIONS
            )

        writer.write(frame)

        frame_count += 1

        if frame_count % 30 == 0:

            print(
                f"Processed {frame_count} frames"
            )

    cap.release()
    writer.release()

    estimator.close()

    print(
        f"Saved visualization to: "
        f"{output_path}"
    )


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 3:

        print(
            "Usage:"
        )

        print(
            "python -m "
            "backend.visualization.visualize_pose "
            "input.mp4 output.mp4"
        )

        sys.exit(1)

    visualize_video(
        sys.argv[1],
        sys.argv[2]
    )