import numpy as np
import mediapipe as mp
import streamlit as st 
import cv2 


@st.cache_resource
def load_model():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
    static_image_mode=False,       # Set to True if using static images (like photos)
    model_complexity=2,            # 0 for Lite, 1 for Medium, 2 for Full
    min_detection_confidence=0.7,  # Confidence threshold for detection
    min_tracking_confidence=0.7    # Confidence threshold for tracking
    )
    mp_drawing = mp.solutions.drawing_utils
    return mp_pose,pose,mp_drawing

mp_pose, pose,mp_drawing = load_model()

def calculate_angle_3d(pointA, pointB, pointC):
    """
    Calculate the directed angle between three points in 3D: A, B, and C.
    Args:
        pointA, pointB, pointC (tuple): Points representing the (x, y, z) coordinates.
    Returns:
        float: Directed angle in degrees between the three points (range -180 to +180).
    """
    a = np.array(pointA)
    b = np.array(pointB)
    c = np.array(pointC)

    # Calculate vectors BA and BC
    ba = a - b
    bc = c - b

    # Calculate the cosine of the angle using dot product and magnitudes
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    # Calculate the cross product to determine direction
    cross_product = np.cross(ba, bc)

    # Define a reference vector (e.g., z-axis) to check the direction
    reference_vector = np.array([0, 0, 1])  # This could be any vector orthogonal to the plane

    # Calculate dot product of cross_product with reference_vector
    direction = np.dot(cross_product, reference_vector)

    # Adjust angle based on direction
    if direction < 0:
        angle = -angle

    return angle


def draw_keypoints(image,required_angles):
    annotated_image = image
    joint_angle = dict()
    matched_sequence = False
    # Process the image to find keypoints
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    if results.pose_landmarks:
        # Get the pixel coordinates for each landmark
        h, w, _ = image.shape
        landmarks = results.pose_landmarks.landmark
        keypoints = [(int(landmark.x * w), int(landmark.y * h), int(landmark.z)) for landmark in landmarks]

        # Define the key joint angles to calculate
        joint_angles = {
            "left_elbow": (keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                           keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                           keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]),
            
            "right_elbow": (keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                            keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                            keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]),
            
            "left_shoulder": (keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                              keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                              keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]),
            
            "right_shoulder": (keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                               keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                               keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]),
            
            "left_hip": (keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                         keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                         keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value]),
            
            "right_hip": (keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                          keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                          keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value]),
            
            "left_knee": (keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                          keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
                          keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value]),
            
            "right_knee": (keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                           keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                           keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value]),
            
            "left_ankle": (keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
                           keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                           keypoints[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]),
            
            "right_ankle": (keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                            keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                            keypoints[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value])
        }
        # Check each joint angle against the reference angle
        correct_joints = []
        incorrect_joints = []
        for joint, (pointA, pointB, pointC) in joint_angles.items():
            # Calculate the current angle

            current_angle = calculate_angle_3d(pointA, pointB, pointC)
            joint_angle[joint] = current_angle
            if (current_angle - required_angles[joint])>30:
                cv2.line(annotated_image, pointA[:2], pointB[:2], (0, 0, 255), 5)  # Joint in blue
                cv2.line(annotated_image, pointB[:2], pointC[:2], (0, 0, 255), 5)
                incorrect_joints.append(joint)
            else:
                cv2.line(annotated_image, pointA[:2], pointB[:2], (0, 255, 0), 5)  # Joint in blue
                cv2.line(annotated_image, pointB[:2], pointC[:2], (0, 255, 0), 5) 
                correct_joints.append(joint)

                
            # Annotate the misplaced joint on the image
            #cv2.putText(annotated_image, f"{joint}: {current_angle:.1f}",
            #               (pointB[0], pointB[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if len(incorrect_joints)==0:
            matched_sequence= True
            print("Match")
    return joint_angle, matched_sequence