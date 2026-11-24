"""
3D and 2D Pose Geometry and Angle Calculations.
"""

from typing import Sequence, Tuple, Union
import numpy as np


def calculate_angle_3d(
    pointA: Sequence[float],
    pointB: Sequence[float],
    pointC: Sequence[float],
    directed: bool = False
) -> float:
    """
    Calculate the angle at pointB formed by vectors BA and BC in 3D space.
    
    Args:
        pointA: Coordinates (x, y, z) of point A.
        pointB: Joint vertex coordinates (x, y, z).
        pointC: Coordinates (x, y, z) of point C.
        directed: Whether to return a signed angle (-180 to +180) or unsigned (0 to 180).
        
    Returns:
        float: Angle in degrees.
    """
    a = np.array(pointA[:3], dtype=np.float64)
    b = np.array(pointB[:3], dtype=np.float64)
    c = np.array(pointC[:3], dtype=np.float64)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba < 1e-6 or norm_bc < 1e-6:
        return 0.0

    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

    if directed:
        cross_product = np.cross(ba, bc)
        reference_vector = np.array([0.0, 0.0, 1.0])
        if np.dot(cross_product, reference_vector) < 0:
            angle = -angle

    return float(angle)


def calculate_angle_2d(
    pointA: Sequence[float],
    pointB: Sequence[float],
    pointC: Sequence[float]
) -> float:
    """Calculate planar 2D angle in degrees (0 to 180)."""
    a = np.array(pointA[:2], dtype=np.float64)
    b = np.array(pointB[:2], dtype=np.float64)
    c = np.array(pointC[:2], dtype=np.float64)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba < 1e-6 or norm_bc < 1e-6:
        return 0.0

    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))
