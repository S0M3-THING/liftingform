import sys

from backend.services.video_processor import (
    validate_video
)

from backend.services.pose_estimator import (
    PoseEstimator
)

from backend.analysis.exercises.squathard import (
    SquatAnalyzer
)


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python -m "
            "backend.analyze_video video.mp4"
        )

        sys.exit(1)

    video_path = sys.argv[1]

    print(
        f"Analyzing: {video_path}"
    )

    metadata = validate_video(
        video_path
    )

    print(
        f"Duration: "
        f"{metadata['duration']:.2f}s"
    )

    print(
        f"FPS: {metadata['fps']:.2f}"
    )

    estimator = PoseEstimator()

    try:

        result = estimator.process_video(
            video_path
        )

    finally:

        estimator.close()

    print(
        f"Total frames: "
        f"{result['total_frames']}"
    )

    print(
        f"Frames with pose: "
        f"{len(result['pose_frames'])}"
    )

    if not result["pose_frames"]:

        print(
            "ERROR: No pose detected."
        )

        return

    analyzer = SquatAnalyzer()

    analysis = analyzer.analyze(
        side_pose=result["pose_frames"]
    )

    print()
    print("=" * 50)
    print("SQUAT ANALYSIS")
    print("=" * 50)

    print(
        f"Score: {analysis.score:.1f}/100"
    )

    print()

    print("Metrics:")

    for key, value in (
        analysis.metrics.items()
    ):

        print(
            f"  {key}: {value}"
        )

    print()

    print("Issues:")

    if not analysis.issues:

        print("  None detected")

    else:

        for issue in analysis.issues:

            print(
                f"  [{issue.severity}] "
                f"{issue.description}"
            )

    print()

    print("Recommendations:")

    if not analysis.recommendations:

        print("  None")

    else:

        for recommendation in (
            analysis.recommendations
        ):

            print(
                f"  • {recommendation}"
            )


if __name__ == "__main__":
    main()