"""
YogaAssist: AI-Powered Yoga Pose Alignment & Rehabilitation Studio.
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from core.geometry import calculate_angle_3d
from core.asanas import ASANA_CATALOG, AsanaPose
from core.pose_analyzer import PoseAnalyzer

st.set_page_config(
    page_title="YogaAssist AI Studio",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧘 YogaAssist: AI Pose Validator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Computer Vision & Biomechanics-driven Yoga Posture Guidance & Assessment.</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Navigation")
    active_tab = st.radio(
        "Explore",
        ["🏠 Dashboard", "📷 Real-Time Pose Checker", "📚 Asana Encyclopedia", "☀️ Surya Namaskar Guide"]
    )
    st.markdown("---")
    st.subheader("Pose Difficulty & Tolerance")
    tolerance_offset = st.slider("Tolerance Margin (± degrees)", min_value=10, max_value=35, value=20, step=2)

analyzer = PoseAnalyzer()

# ----------------- 1. DASHBOARD -----------------
if "Dashboard" in active_tab:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Curated Asanas", len(ASANA_CATALOG))
    with col2:
        st.metric("Joint Accuracy Target", "80%+")
    with col3:
        st.metric("Daily Streak", "7 Days 🔥")
    with col4:
        st.metric("AI Model", "MediaPipe 3D")

    st.markdown("### Featured Posture Sessions")
    cols = st.columns(3)
    asanas_list = list(ASANA_CATALOG.values())
    for idx, asana in enumerate(asanas_list[:3]):
        with cols[idx]:
            st.markdown(f"#### {asana.name} ({asana.sanskrit_name})")
            st.write(asana.description)
            st.info(f"**Key Benefit:** {asana.benefits}")
            st.markdown(f"- **Key Evaluated Joints**: `{len(asana.target_angles)}` joints")

# ----------------- 2. REAL-TIME POSE CHECKER -----------------
elif "Real-Time Pose Checker" in active_tab:
    st.header("📷 Interactive Pose Alignment Checker")
    st.write("Select an Asana posture, stand in front of your camera, and evaluate posture alignment in real-time.")

    selected_id = st.selectbox(
        "Choose Asana to Validate",
        list(ASANA_CATALOG.keys()),
        format_func=lambda x: f"{ASANA_CATALOG[x].name} ({ASANA_CATALOG[x].sanskrit_name})"
    )
    current_asana = ASANA_CATALOG[selected_id]
    current_asana.default_tolerance = float(tolerance_offset)

    col_target, col_camera = st.columns([1, 2])

    with col_target:
        st.subheader("Target Posture")
        st.markdown(f"**Asana:** {current_asana.name}")
        st.markdown(f"**Sanskrit:** *{current_asana.sanskrit_name}*")
        st.write(current_asana.description)
        st.markdown("#### Joint Angle Targets:")
        for joint, ang in current_asana.target_angles.items():
            st.write(f"- `{joint.replace('_', ' ').title()}`: **{int(ang)}°** (±{int(tolerance_offset)}°)")

    with col_camera:
        st.subheader("Live Camera Evaluation")
        photo = st.camera_input("Take a Snapshot in Pose")
        uploaded = st.file_uploader("Or Upload a Pose Photo", type=["jpg", "jpeg", "png", "webp"])

        eval_frame = None
        if photo:
            pil_img = Image.open(photo).convert("RGB")
            eval_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        elif uploaded:
            pil_img = Image.open(uploaded).convert("RGB")
            eval_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        else:
            if st.button("🧪 Evaluate Synthetic Standing Pose"):
                # Create synthetic figure
                test_img = np.zeros((480, 640, 3), dtype=np.uint8)
                test_img[:] = (245, 245, 245)
                eval_frame = test_img

        if eval_frame is not None:
            res = analyzer.analyze_frame(eval_frame, current_asana)
            
            st.markdown("### 📊 Alignment Feedback")
            col_res1, col_res2 = st.columns([2, 1])
            with col_res1:
                st.image(cv2.cvtColor(res.annotated_image, cv2.COLOR_BGR2RGB), caption="Analyzed Keypoints", use_container_width=True)
            with col_res2:
                if res.is_matched:
                    st.success(f"🎉 Pose Validated! Compliance: {int(res.accuracy_percentage)}%")
                else:
                    st.warning(f"⚠️ Posture Needs Adjustment. Compliance: {int(res.accuracy_percentage)}%")

                st.progress(res.accuracy_percentage / 100.0)
                st.write(f"**Visible Keypoints:** {res.visible_joint_count}")
                st.write(f"**Aligned Joints:** {res.correct_joint_count} / {len(res.joint_feedbacks)}")

                for j_name, fb in res.joint_feedbacks.items():
                    status_emoji = "✅" if fb.is_correct else "❌"
                    st.write(f"{status_emoji} **{j_name.title()}**: Current: {int(fb.current_angle)}° | Target: {int(fb.target_angle)}°")

# ----------------- 3. ASANA ENCYCLOPEDIA -----------------
elif "Asana Encyclopedia" in active_tab:
    st.header("📚 Complete Asana Biomechanical Directory")
    for a_id, asana in ASANA_CATALOG.items():
        with st.expander(f"🧘 {asana.name} ({asana.sanskrit_name})", expanded=False):
            st.markdown(f"**Description:** {asana.description}")
            st.markdown(f"**Therapeutic Benefits:** {asana.benefits}")
            st.markdown("##### Reference Joint Angles:")
            cols = st.columns(4)
            for i, (joint, ang) in enumerate(asana.target_angles.items()):
                with cols[i % 4]:
                    st.metric(joint.replace('_', ' ').title(), f"{int(ang)}°")

# ----------------- 4. SURYA NAMASKAR -----------------
elif "Surya Namaskar Guide" in active_tab:
    st.header("☀️ Surya Namaskar (Sun Salutation) 12-Step Cycle")
    st.write("Surya Namaskar is a sequential flow of 12 powerful yoga asanas coordinating breath and alignment.")
    
    steps = [
        ("1. Pranamasana", "Prayer Pose - Centering and breath awareness"),
        ("2. Hastauttanasana", "Raised Arms Pose - Inhale and arch spine backward"),
        ("3. Padahastasana", "Hand to Foot Pose - Exhale and fold from hips"),
        ("4. Ashwa Sanchalanasana", "Equestrian Pose - Step right leg back"),
        ("5. Dandasana", "Stick / Plank Pose - Core activation"),
        ("6. Ashtanga Namaskara", "Salute with 8 points - Knees, chest, chin"),
        ("7. Bhujangasana", "Cobra Pose - Elevated chest and lumbar extension"),
        ("8. Adho Mukha Svanasana", "Downward Dog - Inverted V lengthening"),
        ("9. Ashwa Sanchalanasana", "Equestrian Pose - Step left leg back"),
        ("10. Padahastasana", "Hand to Foot Pose - Standing forward bend"),
        ("11. Hastauttanasana", "Raised Arms Pose - Gentle backward bend"),
        ("12. Tadasana / Pranamasana", "Mountain / Prayer Pose - Concluding breath"),
    ]
    
    for title, desc in steps:
        st.markdown(f"- **{title}**: {desc}")
