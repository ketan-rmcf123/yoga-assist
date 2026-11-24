"""
MediaPipe Pose Analyzer and Joint Compliance Evaluator.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import cv2
import numpy as np

from .geometry import calculate_angle_3d
from .asanas import AsanaPose, ASANA_CATALOG


@dataclass
class JointFeedback:
    name: str
    current_angle: float
    target_angle: float
    difference: float
    is_correct: bool
    points: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]


@dataclass
class PoseAnalysisResult:
    is_matched: bool
    accuracy_percentage: float
    joint_feedbacks: Dict[str, JointFeedback]
    annotated_image: np.ndarray
    visible_joint_count: int
    correct_joint_count: int


class PoseAnalyzer:
    """Real-time pose extractor and compliance analyzer."""

    def __init__(
        self,
        min_detection_confidence: float = 0.6,
        min_tracking_confidence: float = 0.6,
        model_complexity: int = 1
    ) -> None:
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.model_complexity = model_complexity
        self._mp_pose = None
        self._pose = None
        self._mp_drawing = None

    def _ensure_model(self) -> bool:
        if self._pose is not None:
            return True
        try:
            import mediapipe as mp
            self._mp_pose = mp.solutions.pose
            self._mp_drawing = mp.solutions.drawing_utils
            self._pose = self._mp_pose.Pose(
                static_image_mode=False,
                model_complexity=self.model_complexity,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )
            return True
        except Exception:
            return False

    def analyze_frame(
        self,
        frame_bgr: np.ndarray,
        asana: AsanaPose
    ) -> PoseAnalysisResult:
        """
        Analyze webcam frame against target Asana posture.
        """
        annotated = frame_bgr.copy()
        h, w = frame_bgr.shape[:2]

        if not self._ensure_model():
            return PoseAnalysisResult(
                is_matched=False,
                accuracy_percentage=0.0,
                joint_feedbacks={},
                annotated_image=annotated,
                visible_joint_count=0,
                correct_joint_count=0,
            )

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._pose.process(frame_rgb)

        if not results.pose_landmarks:
            return PoseAnalysisResult(
                is_matched=False,
                accuracy_percentage=0.0,
                joint_feedbacks={},
                annotated_image=annotated,
                visible_joint_count=0,
                correct_joint_count=0,
            )

        landmarks = results.pose_landmarks.landmark
        keypoints = [
            (int(lm.x * w), int(lm.y * h), lm.z, lm.visibility)
            for lm in landmarks
        ]

        mp_p = self._mp_pose.PoseLandmark

        joint_triplets = {
            "left_elbow": (mp_p.LEFT_SHOULDER.value, mp_p.LEFT_ELBOW.value, mp_p.LEFT_WRIST.value),
            "right_elbow": (mp_p.RIGHT_SHOULDER.value, mp_p.RIGHT_ELBOW.value, mp_p.RIGHT_WRIST.value),
            "left_shoulder": (mp_p.LEFT_HIP.value, mp_p.LEFT_SHOULDER.value, mp_p.LEFT_ELBOW.value),
            "right_shoulder": (mp_p.RIGHT_HIP.value, mp_p.RIGHT_SHOULDER.value, mp_p.RIGHT_ELBOW.value),
            "left_hip": (mp_p.LEFT_SHOULDER.value, mp_p.LEFT_HIP.value, mp_p.LEFT_KNEE.value),
            "right_hip": (mp_p.RIGHT_SHOULDER.value, mp_p.RIGHT_HIP.value, mp_p.RIGHT_KNEE.value),
            "left_knee": (mp_p.LEFT_HIP.value, mp_p.LEFT_KNEE.value, mp_p.LEFT_ANKLE.value),
            "right_knee": (mp_p.RIGHT_HIP.value, mp_p.RIGHT_KNEE.value, mp_p.RIGHT_ANKLE.value),
        }

        feedbacks: Dict[str, JointFeedback] = {}
        correct_count = 0
        visible_count = 0

        for joint_name, (idxA, idxB, idxC) in joint_triplets.items():
            if joint_name not in asana.target_angles:
                continue

            ptA = keypoints[idxA]
            ptB = keypoints[idxB]
            ptC = keypoints[idxC]

            # Visibility threshold
            if ptA[3] < 0.4 or ptB[3] < 0.4 or ptC[3] < 0.4:
                continue

            visible_count += 1
            curr_angle = calculate_angle_3d(ptA, ptB, ptC)
            target_angle = asana.target_angles[joint_name]
            tol = asana.get_tolerance(joint_name)

            diff = abs(curr_angle - target_angle)
            is_correct = diff <= tol

            if is_correct:
                correct_count += 1
                color = (0, 255, 60)  # Green BGR
            else:
                color = (0, 60, 255)  # Red BGR

            # Draw skeletal bones
            cv2.line(annotated, ptA[:2], ptB[:2], color, 4)
            cv2.line(annotated, ptB[:2], ptC[:2], color, 4)

            # Draw joint vertices
            cv2.circle(annotated, ptB[:2], 7, (255, 255, 255), -1)
            cv2.circle(annotated, ptB[:2], 5, color, -1)

            # Draw angle text badge
            cv2.putText(
                annotated,
                f"{int(curr_angle)}",
                (ptB[0] + 8, ptB[1] - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
                cv2.LINE_AA
            )

            feedbacks[joint_name] = JointFeedback(
                name=joint_name,
                current_angle=curr_angle,
                target_angle=target_angle,
                difference=diff,
                is_correct=is_correct,
                points=(ptA[:2], ptB[:2], ptC[:2])
            )

        total_evaluated = len(feedbacks)
        accuracy = (correct_count / total_evaluated * 100.0) if total_evaluated > 0 else 0.0
        is_matched = (accuracy >= 80.0) and (visible_count >= 4)

        return PoseAnalysisResult(
            is_matched=is_matched,
            accuracy_percentage=accuracy,
            joint_feedbacks=feedbacks,
            annotated_image=annotated,
            visible_joint_count=visible_count,
            correct_joint_count=correct_count,
        )

    def close(self) -> None:
        if self._pose is not None:
            try:
                self._pose.close()
            except Exception:
                pass
