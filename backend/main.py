import os
import shutil
import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from starlette.requests import Request

from backend.services.video_processor import (
    validate_video
)

from backend.services.pose_estimator import (
    PoseEstimator
)

from backend.analysis.exercises.squathard import (
    SquatAnalyzer
)


app = FastAPI(
    title="Form Coach",
    version="0.1.0"
)


templates = Jinja2Templates(
    directory="backend/templates"
)


UPLOAD_DIRECTORY = "uploads"

os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
def health():

    return {
        "status": "healthy"
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


def process_video(
    video_path
):

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
    video: UploadFile = File(...)
):

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

    video_path = os.path.join(
        job_directory,
        "squat.mp4"
    )

    try:

        save_upload_file(
            video,
            video_path
        )

        print(
            f"[{job_id}] Validating video"
        )

        validate_video(
            video_path
        )

        print(
            f"[{job_id}] Running pose estimation"
        )

        result = process_video(
            video_path
        )

        print(
            f"[{job_id}] "
            f"Detected pose in "
            f"{len(result['pose_frames'])} "
            f"frames"
        )

        analyzer = SquatAnalyzer()

        analysis = analyzer.analyze(
            side_pose=result[
                "pose_frames"
            ]
        )

        return {
            "job_id": job_id,

            "video_info": {
                "fps": result["fps"],
                "total_frames": (
                    result["total_frames"]
                ),
                "pose_frames": len(
                    result["pose_frames"]
                ),
                "duration": (
                    result["total_frames"]
                    / result["fps"]
                )
            },

            "analysis":
                analysis.to_dict()
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
                "Video analysis failed: "
                + str(error)
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