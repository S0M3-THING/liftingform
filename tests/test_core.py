"""Regression checks that do not require video or machine-learning packages."""
import json
import unittest

from backend.analysis.scoring import clamp, weighted_score
from backend.models.analysis import AnalysisResult, Issue


class ScoringTests(unittest.TestCase):
    def test_score_bounds(self):
        self.assertEqual(clamp(-10), 0)
        self.assertEqual(clamp(110), 100)
        self.assertEqual(clamp(67.5), 67.5)
        self.assertEqual(clamp(12, minimum=10, maximum=20), 12)

    def test_missing_metric_does_not_lower_observed_score(self):
        score = weighted_score({'depth': 80}, {'depth': 0.4, 'symmetry': 0.6})
        self.assertAlmostEqual(score, 80)

    def test_weighted_combination(self):
        score = weighted_score({'depth': 100, 'symmetry': 40}, {'depth': 0.4, 'symmetry': 0.6})
        self.assertAlmostEqual(score, 64)

    def test_no_contributing_weights(self):
        self.assertEqual(weighted_score({}, {'depth': 1}), 0)
        self.assertEqual(weighted_score({'depth': 90}, {}), 0)
        self.assertEqual(weighted_score({'depth': 90}, {'depth': 0}), 0)

    def test_unconfigured_metrics_are_ignored(self):
        score = weighted_score({'depth': 80, 'repetitions': 1000}, {'depth': 1})
        self.assertEqual(score, 80)

    def test_combined_score_stays_bounded(self):
        self.assertEqual(weighted_score({'depth': 150}, {'depth': 1}), 100)
        self.assertEqual(weighted_score({'depth': -5}, {'depth': 1}), 0)


class AnalysisResultTests(unittest.TestCase):
    def test_response_shape_rounding_and_json(self):
        result = AnalysisResult(
            exercise='squat', score=81.234,
            metrics={'depth': 92.345, 'repetitions': 3, 'unavailable': None},
            issues=[Issue('depth', 'moderate', 'Example issue')],
            recommendations=['Example recommendation'],
        )
        expected = {
            'exercise': 'squat', 'score': 81.2,
            'metrics': {'depth': 92.3, 'repetitions': 3, 'unavailable': None},
            'issues': [{'type': 'depth', 'severity': 'moderate', 'description': 'Example issue'}],
            'recommendations': ['Example recommendation'],
        }
        self.assertEqual(json.loads(json.dumps(result.to_dict())), expected)

    def test_serializing_does_not_round_original_metrics(self):
        result = AnalysisResult('squat', 80, metrics={'depth': 92.345})
        result.to_dict()
        self.assertEqual(result.metrics['depth'], 92.345)

    def test_default_collections_are_not_shared(self):
        first = AnalysisResult('squat', 0)
        second = AnalysisResult('squat', 0)
        first.metrics['depth'] = 90
        first.issues.append(Issue('depth', 'mild', 'Example'))
        first.recommendations.append('Example')
        self.assertEqual(second.to_dict(), {
            'exercise': 'squat', 'score': 0,
            'metrics': {}, 'issues': [], 'recommendations': [],
        })


if __name__ == '__main__':
    unittest.main()
