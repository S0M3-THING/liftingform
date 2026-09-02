from backend.services.pose_estimator import PoseEstimator


def test_pose_estimator_creation():

    estimator = PoseEstimator()

    assert estimator is not None

    estimator.close()