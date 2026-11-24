"""
Asana Knowledge Base and Reference Postures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AsanaPose:
    id: str
    name: str
    sanskrit_name: str
    description: str
    benefits: str
    target_angles: Dict[str, float]
    tolerances: Dict[str, float] = field(default_factory=dict)
    default_tolerance: float = 20.0

    def get_tolerance(self, joint: str) -> float:
        return self.tolerances.get(joint, self.default_tolerance)


ASANA_CATALOG: Dict[str, AsanaPose] = {
    "tadasana": AsanaPose(
        id="tadasana",
        name="Mountain Pose",
        sanskrit_name="Tadasana",
        description="Foundational standing pose cultivating stability, symmetry, and mindful posture.",
        benefits="Improves posture, strengthens thighs, knees, and ankles.",
        target_angles={
            "left_elbow": 180.0,
            "right_elbow": 180.0,
            "left_shoulder": 15.0,
            "right_shoulder": 15.0,
            "left_hip": 180.0,
            "right_hip": 180.0,
            "left_knee": 180.0,
            "right_knee": 180.0,
        },
        default_tolerance=20.0
    ),
    "pranamasana": AsanaPose(
        id="pranamasana",
        name="Prayer Pose",
        sanskrit_name="Pranamasana",
        description="First step of Surya Namaskar. Hands joined at heart center.",
        benefits="Calms the mind and establishes rhythm of breath.",
        target_angles={
            "left_elbow": 85.0,
            "right_elbow": 85.0,
            "left_shoulder": 30.0,
            "right_shoulder": 30.0,
            "left_hip": 180.0,
            "right_hip": 180.0,
            "left_knee": 180.0,
            "right_knee": 180.0,
        },
        default_tolerance=22.0
    ),
    "hastauttanasana": AsanaPose(
        id="hastauttanasana",
        name="Raised Arms Pose",
        sanskrit_name="Hastauttanasana",
        description="Inhale and lift both arms overhead, gently arching the spine backward.",
        benefits="Stretches abdominal organs and expands the chest.",
        target_angles={
            "left_elbow": 175.0,
            "right_elbow": 175.0,
            "left_shoulder": 170.0,
            "right_shoulder": 170.0,
            "left_hip": 170.0,
            "right_hip": 170.0,
            "left_knee": 180.0,
            "right_knee": 180.0,
        },
        default_tolerance=25.0
    ),
    "padahastasana": AsanaPose(
        id="padahastasana",
        name="Hand to Foot Pose",
        sanskrit_name="Padahastasana",
        description="Exhale and fold forward from the hips until hands touch feet or floor.",
        benefits="Stretches hamstrings, strengthens calves, and stimulates digestion.",
        target_angles={
            "left_elbow": 160.0,
            "right_elbow": 160.0,
            "left_hip": 45.0,
            "right_hip": 45.0,
            "left_knee": 175.0,
            "right_knee": 175.0,
        },
        default_tolerance=25.0
    ),
    "bhujangasana": AsanaPose(
        id="bhujangasana",
        name="Cobra Pose",
        sanskrit_name="Bhujangasana",
        description="Prone back-bending asana that elevates the chest and strengthens the spinal column.",
        benefits="Strengthens the spine, firms buttocks, and stimulates abdominal organs.",
        target_angles={
            "left_elbow": 140.0,
            "right_elbow": 140.0,
            "left_shoulder": 70.0,
            "right_shoulder": 70.0,
            "left_hip": 145.0,
            "right_hip": 145.0,
            "left_knee": 180.0,
            "right_knee": 180.0,
        },
        default_tolerance=25.0
    ),
    "adho_mukha_svanasana": AsanaPose(
        id="adho_mukha_svanasana",
        name="Downward-Facing Dog",
        sanskrit_name="Adho Mukha Svanasana",
        description="Inverted V-shape pose elongating the posterior chain.",
        benefits="Energizes the body, relieves back pain, stretches calves and hamstrings.",
        target_angles={
            "left_elbow": 180.0,
            "right_elbow": 180.0,
            "left_shoulder": 170.0,
            "right_shoulder": 170.0,
            "left_hip": 70.0,
            "right_hip": 70.0,
            "left_knee": 175.0,
            "right_knee": 175.0,
        },
        default_tolerance=25.0
    ),
}
