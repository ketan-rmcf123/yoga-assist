"""
Compatibility wrapper for legacy match_function imports.
Redirects to core.pose_analyzer and core.geometry.
"""

from typing import Dict, Any, Tuple
import cv2
import numpy as np

from core.geometry import calculate_angle_3d
from core.pose_analyzer import PoseAnalyzer
from core.asanas import ASANA_CATALOG, AsanaPose

_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = PoseAnalyzer()
    return _analyzer

def load_model():
    """Legacy helper: returns mediapipe pose instances if available."""
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        mp_drawing = mp.solutions.drawing_utils
        return mp_pose, pose, mp_drawing
    except Exception:
        return None, None, None

def draw_keypoints(image: np.ndarray, required_angles: Dict[str, float], diff: float = 20.0):
    """
    Evaluates pose keypoints with absolute difference tolerance and color coding.
    """
    temp_asana = AsanaPose(
        id="custom",
        name="Custom Pose",
        sanskrit_name="Custom",
        description="",
        benefits="",
        target_angles=required_angles,
        default_tolerance=diff
    )
    analyzer = get_analyzer()
    res = analyzer.analyze_frame(image, temp_asana)
    
    joint_angles = {k: v.current_angle for k, v in res.joint_feedbacks.items()}
    visibilities = {k: 3 if v.is_correct else 2 for k, v in res.joint_feedbacks.items()}
    
    return joint_angles, res.is_matched, visibilities, res.annotated_image

def filter_visibility(visibility_params):
    return len([x for x in visibility_params if len(x) > 3 and x[3] > 0.5])

def speak_text(text_input: str):
    """Text-to-speech feedback."""
    try:
        from gtts import gTTS
        import tempfile
        import streamlit as st
        tts = gTTS(text_input, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            tts.save(temp_audio_file.name)
            st.audio(temp_audio_file.name, format="audio/mp3")
    except Exception:
        pass
