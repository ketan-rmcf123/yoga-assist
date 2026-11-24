"""
Unit Tests for YogaAssist Core Engine.
"""

import os
import sys
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.geometry import calculate_angle_3d, calculate_angle_2d
from core.asanas import ASANA_CATALOG, AsanaPose
from core.pose_analyzer import PoseAnalyzer


class TestPoseGeometry(unittest.TestCase):
    def test_orthogonal_angle_90(self):
        # Point B at origin (0,0,0)
        # Point A at (0, 1, 0) - north
        # Point C at (1, 0, 0) - east
        angle = calculate_angle_3d((0, 1, 0), (0, 0, 0), (1, 0, 0))
        self.assertAlmostEqual(angle, 90.0, places=2)

    def test_straight_line_angle_180(self):
        # Point B at (0, 0, 0)
        # Point A at (-1, 0, 0)
        # Point C at (1, 0, 0)
        angle = calculate_angle_3d((-1, 0, 0), (0, 0, 0), (1, 0, 0))
        self.assertAlmostEqual(angle, 180.0, places=2)

    def test_acute_angle_45(self):
        angle = calculate_angle_3d((1, 1, 0), (0, 0, 0), (1, 0, 0))
        self.assertAlmostEqual(angle, 45.0, places=2)

    def test_collinear_zero(self):
        # Point A and C in same direction
        angle = calculate_angle_3d((2, 0, 0), (0, 0, 0), (1, 0, 0))
        self.assertAlmostEqual(angle, 0.0, places=2)

    def test_2d_angle(self):
        angle = calculate_angle_2d((0, 1), (0, 0), (1, 0))
        self.assertAlmostEqual(angle, 90.0, places=2)


class TestAsanaCatalog(unittest.TestCase):
    def test_catalog_integrity(self):
        self.assertIn("tadasana", ASANA_CATALOG)
        self.assertIn("pranamasana", ASANA_CATALOG)
        self.assertIn("bhujangasana", ASANA_CATALOG)

        for asana_id, asana in ASANA_CATALOG.items():
            self.assertIsInstance(asana.name, str)
            self.assertIsInstance(asana.target_angles, dict)
            self.assertGreater(len(asana.target_angles), 0)
            self.assertGreater(asana.get_tolerance("left_elbow"), 0.0)


class TestPoseAnalyzerHeadless(unittest.TestCase):
    def test_analyzer_blank_frame(self):
        analyzer = PoseAnalyzer()
        blank_frame = np.zeros((240, 320, 3), dtype=np.uint8)
        asana = ASANA_CATALOG["tadasana"]

        res = analyzer.analyze_frame(blank_frame, asana)
        self.assertFalse(res.is_matched)
        self.assertEqual(res.accuracy_percentage, 0.0)
        self.assertEqual(res.annotated_image.shape, blank_frame.shape)


if __name__ == "__main__":
    unittest.main()
