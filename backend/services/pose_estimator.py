import cv2
import mediapipe as mp


class PoseEstimator:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_video(self, video_path):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(
                f"Could not open video: {video_path}"
            )

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = 30.0

        total_frames = int(
            cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

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

        frames = []

        frame_number = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            result = self.pose.process(rgb)

            if result.pose_landmarks:

                landmarks = []

                for landmark in (
                    result.pose_landmarks.landmark
                ):

                    landmarks.append({
                        "x": float(
                            landmark.x
                        ),
                        "y": float(
                            landmark.y
                        ),
                        "z": float(
                            landmark.z
                        ),
                        "visibility": float(
                            landmark.visibility
                        )
                    })

                frames.append({
                    "frame": frame_number,
                    "time": (
                        frame_number / fps
                    ),
                    "landmarks": landmarks
                })

            frame_number += 1

        cap.release()

        return {
            "fps": fps,
            "total_frames": total_frames,
            "width": width,
            "height": height,
            "pose_frames": frames
        }

    def close(self):
        self.pose.close()