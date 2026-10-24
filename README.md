# Form Coach

A Python prototype for analyzing squat videos with OpenCV, MediaPipe pose estimation, and a FastAPI web interface. The current web and command-line entry points estimate squat depth, repetition consistency, and repetition count from a single video passed to the side-view analysis path.

## How it works

1. Validate the video format, file size, frame rate, and duration.
2. Extract body landmarks from frames where MediaPipe detects a pose.
3. Build a knee-angle signal and detect repetitions.
4. Return a score, metrics, detected issues, and recommendations.

The scores use prototype angle thresholds and weights; they are not a validated assessment of lifting safety.

## Project layout

| Path | Purpose |
| --- | --- |
| [`backend/main.py`](backend/main.py) | FastAPI app, upload handling, and analysis endpoint. |
| [`backend/templates/index.html`](backend/templates/index.html) | Browser upload interface. |
| [`backend/analyze_video.py`](backend/analyze_video.py) | Command-line video analysis. |
| [`backend/services/pose_estimator.py`](backend/services/pose_estimator.py) | MediaPipe landmark extraction. |
| [`backend/services/video_processor.py`](backend/services/video_processor.py) | Video validation and limits. |
| [`backend/analysis/exercises/squathard.py`](backend/analysis/exercises/squathard.py) | Squat analyzer used by the current entry points. |
| [`backend/utils/geometry.py`](backend/utils/geometry.py) | Geometry helpers for landmark measurements. |
| [`tests`](tests) | Geometry and pose-estimator smoke tests. |

## Set up locally

From a terminal with Python and `venv` available:

```bash
git clone https://github.com/S0M3-THING/liftingform.git
cd liftingform
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The dependency list pins a full environment, including platform-specific packages such as `uvloop`. Installation compatibility has not been verified across operating systems. The pose estimator uses `mediapipe.solutions.pose`; the installed MediaPipe version must expose that API. If installation or imports fail, resolve the environment compatibility before starting the app.

## Run the web app

Run from the repository root because the template and upload paths are relative to the working directory:

```bash
python -m uvicorn backend.main:app --reload
```

Open [the local app](http://127.0.0.1:8000). Choose a squat video and submit it for analysis. Keep the person fully visible and the camera stationary.

| Endpoint | Behavior |
| --- | --- |
| `GET /` | Browser interface. |
| `GET /health` | Returns `{"status": "healthy"}`; this does not test pose estimation. |
| `POST /analyze` | Accepts a multipart file field named `video` and returns video metadata plus analysis. |

Example upload from a second terminal:

```bash
curl -F "video=@/path/to/squat.mp4" http://127.0.0.1:8000/analyze
```

The response contains `job_id`, `video_info`, and `analysis`. Analysis includes the exercise, score, metrics, issues, and recommendations.

## Video requirements and processing

- The validator accepts `.mp4`, `.mov`, and `.avi` files that OpenCV can decode.
- The maximum size is 100 MiB (`100 * 1024 * 1024` bytes); the maximum duration is 60 seconds.
- The video must have a readable positive frame rate and a detectable person.
- The web endpoint saves every upload as `squat.mp4` before validation, so its filename extension check does not verify the original upload extension. Decoding still depends on OpenCV.
- Web uploads are temporarily stored under `uploads/<job_id>/` and removed in the endpoint's cleanup block after processing. Analysis is returned in the response rather than saved as a report.

## Run from the command line

With the environment activated and from the repository root:

```bash
python -m backend.analyze_video /path/to/squat.mp4
```

This prints video metadata, the score, metrics, issues, and recommendations. No sample videos are included in the repository.

## Checks

```bash
python -m pytest -q
```

The existing tests cover a right-angle calculation and pose-estimator creation. The pose test requires working OpenCV/MediaPipe dependencies and may initialize model resources. They do not validate end-to-end video analysis or scoring accuracy.

## Current scope

The active entry points analyze squats using one video. Although the analyzer has front/back pose parameters and other exercise modules exist, the current web endpoint does not expose multi-view input or an exercise selector. Video processing runs within the request rather than in a background job queue; treat this as a local prototype.

## License

See [LICENSE](LICENSE).
