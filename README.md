# 🧘 YogaAssist: AI Pose Validator & Alignment Studio

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://img.shields.io/badge/Interface-Streamlit-red.svg)](https://streamlit.io)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20Estimation-00897B.svg)](https://developers.google.com/mediapipe)
[![Tests: Passing](https://img.shields.io/badge/Tests-7%20Passed-brightgreen.svg)]()

> Real-time computer vision and biomechanical analysis application designed to assist individuals in achieving proper yogic postures (Asanas) with **MediaPipe 3D skeletal tracking**, **joint-angle geometry**, and **instant visual alignment feedback**.

---

## 🌟 Key Features

- **🎯 Precision 3D Biomechanical Angle Analysis**:
  - Vector dot product & norm calculations for 10 anatomical joint triplets (elbows, shoulders, hips, knees, ankles).
  - Directed and planar angular calculations with configurable degree tolerances.
- **👁️ Real-Time Visual Feedback**:
  - Color-coded skeletal overlay: **Green** for joints within correct posture tolerance, **Red** for misalignments.
  - Joint angle numeric badges annotated directly on the live image feed.
- **📚 Curated Asana Knowledge Base**:
  - Built-in biomechanical standards for classical Asanas: *Tadasana (Mountain Pose)*, *Pranamasana (Prayer Pose)*, *Hastauttanasana (Raised Arms)*, *Padahastasana (Forward Fold)*, *Bhujangasana (Cobra)*, *Adho Mukha Svanasana (Downward Dog)*.
- **☀️ Surya Namaskar (Sun Salutation) Guide**:
  - 12-step guided sequence progression with step-by-step breathing, alignment, and health benefits.
- **💻 Interactive Streamlit Studio**:
  - Live webcam pose evaluation, instant alignment progress bar, joint compliance breakdown, and audio TTS cues.

---

## 📐 Biomechanical Formulation

For any anatomical joint vertex $B$ connected to adjacent limbs $A$ and $C$:

$$\vec{u} = \vec{A} - \vec{B}, \quad \vec{v} = \vec{C} - \vec{B}$$

The joint angle $\theta$ is derived using the Euclidean inner product:

$$\cos(\theta) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$

$$\theta = \arccos\left(\text{clip}\left(\frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}, -1.0, 1.0\right)\right) \times \frac{180^\circ}{\pi}$$

A joint is considered **correctly aligned** if:

$$|\theta - \theta_{\text{target}}| \le \text{tolerance}$$

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/ketan-rmcf123/yoga-assist.git
cd yoga-assist
pip install -r requirements.txt
```

### 2. Launch Interactive Application

```bash
streamlit run app.py
```
Open `http://localhost:8501` to start posture validation.

---

## 🧪 Testing

Run the automated test suite:

```bash
python -m unittest discover -s tests
# or using pytest
pytest tests/
```

All 7 unit tests validate 3D orthogonal angles ($90^\circ$), collinear angles ($180^\circ$), acute angles ($45^\circ$), 2D planar angles, asana catalog lookups, and headless pose analysis.

---

## 📁 Repository Structure

```
yoga-assist/
├── app.py                      # Modern Streamlit Web Application
├── pyproject.toml              # Modern package manifest
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
├── core/                       # Core biomechanics & pose engine
│   ├── __init__.py
│   ├── geometry.py             # 3D/2D vector angle math
│   ├── asanas.py               # Asana catalog & target angles
│   └── pose_analyzer.py        # MediaPipe skeletal analyzer
├── utils/                      # Legacy compatibility wrappers
│   ├── __init__.py
│   ├── match_function.py
│   └── db_utils.py
├── configs/                    # Session configurations
│   └── sn_config.py
├── pages/                      # Multi-page flows (Daily flow, Surya Namaskar)
└── tests/
    ├── __init__.py
    └── test_yoga_engine.py     # Unit test suite
```

---

## 📜 License

MIT License. Open for accessibility, rehabilitation, and wellness research.
