import os
import uuid
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from backend.services.video_processor import (
    validate_video
)

from backend.services.pose_estimator import (
    PoseEstimator
)

from backend.analysis.exercise_analyzer import (
    ExerciseAnalyzer
)


app = FastAPI(
    title="Form Coach API",
    description=(
        "AI-powered exercise form analysis"
    ),
    version="0.2.0"
)


UPLOAD_DIRECTORY = "uploads"

os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)


ALLOWED_EXERCISES = {
    "squat",
    "deadlift",
    "bench_press"
}


@app.get("/")
def root():

    return {
        "message": "Form Coach API is running",
        "version": "0.2.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/exercises")
def get_exercises():

    return {
        "exercises": [
            {
                "id": "squat",
                "name": "Squat"
            },
            {
                "id": "deadlift",
                "name": "Deadlift"
            },
            {
                "id": "bench_press",
                "name": "Bench Press"
            }
        ]
    }


def save_upload_file(
    upload_file,
    destination
):

    with open(
        destination,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            upload_file.file,
            buffer
        )


def process_video(video_path):

    validate_video(
        video_path
    )

    estimator = PoseEstimator()

    try:

        result = estimator.process_video(
            video_path
        )

    finally:

        estimator.close()

    if not result["pose_frames"]:

        raise ValueError(
            "No person could be detected "
            "in the video."
        )

    return result


@app.post("/analyze")
async def analyze(

    exercise: str = Form(...),

    front_video: UploadFile = File(...),

    side_video: UploadFile = File(...),

    back_video: UploadFile = File(...)
):

    exercise = (
        exercise
        .lower()
        .strip()
    )

    if exercise not in ALLOWED_EXERCISES:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported exercise: "
                f"{exercise}"
            )
        )

    job_id = str(
        uuid.uuid4()
    )

    job_directory = os.path.join(
        UPLOAD_DIRECTORY,
        job_id
    )

    os.makedirs(
        job_directory,
        exist_ok=True
    )

    front_path = os.path.join(
        job_directory,
        "front.mp4"
    )

    side_path = os.path.join(
        job_directory,
        "side.mp4"
    )

    back_path = os.path.join(
        job_directory,
        "back.mp4"
    )

    try:

        save_upload_file(
            front_video,
            front_path
        )

        save_upload_file(
            side_video,
            side_path
        )

        save_upload_file(
            back_video,
            back_path
        )

        print(
            f"[{job_id}] Processing front view"
        )

        front_result = process_video(
            front_path
        )

        print(
            f"[{job_id}] Processing side view"
        )

        side_result = process_video(
            side_path
        )

        print(
            f"[{job_id}] Processing back view"
        )

        back_result = process_video(
            back_path
        )

        analyzer = ExerciseAnalyzer()

        analysis = analyzer.analyze(
            exercise=exercise,

            front_pose=(
                front_result["pose_frames"]
            ),

            side_pose=(
                side_result["pose_frames"]
            ),

            back_pose=(
                back_result["pose_frames"]
            )
        )

        return {
            "job_id": job_id,

            "video_info": {
                "front_frames": (
                    front_result[
                        "total_frames"
                    ]
                ),

                "side_frames": (
                    side_result[
                        "total_frames"
                    ]
                ),

                "back_frames": (
                    back_result[
                        "total_frames"
                    ]
                )
            },

            "analysis": (
                analysis.to_dict()
            )
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        print(
            f"[{job_id}] ERROR: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Video analysis failed."
            )
        )

    finally:

        if os.path.exists(
            job_directory
        ):

            shutil.rmtree(
                job_directory,
                ignore_errors=True
            )