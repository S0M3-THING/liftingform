from backend.services.pose_estimator import PoseEstimator

estimator = PoseEstimator()

result = estimator.process_video(
    "/Users/akashs/Downloads/squatvideo.mp4"
)

print("FPS:", result["fps"])
print("Total frames:", result["total_frames"])
print("Frames with pose:", len(result["pose_frames"]))

estimator.close()