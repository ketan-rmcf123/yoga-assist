# Yoga Pose Validator

This project provides a Yoga Pose Validation tool that helps users perform yoga poses correctly by using computer vision and machine learning techniques. The application tracks the user's movements through their webcam and compares them with predefined asana (pose) angles to provide feedback and guidance.

### Features
- Real-time yoga pose validation using MediaPipe for pose detection.
- Provides feedback and guidance to users to improve posture.
- Displays instructional video and step-by-step guidance.
- Progress bar to track completion of each asana in the sequence.
- Transition from one asana to the next automatically when the pose is validated.
- A simple UI built with Streamlit for interactive use.

## Technologies Used
- **Streamlit**: For building the web app and creating the UI.
- **MediaPipe**: For pose detection and keypoint tracking.
- **Python**: Main programming language for the application logic.
- **OpenCV**: For image manipulation and video processing.
- **Extra Streamlit Components**: For adding extra interactive features to the UI.
- **stqdm**: For displaying progress with a smooth visual interface.

## Usage

1. To start the Yoga Pose Validator app, run:

   ```bash
   streamlit run app.py
2. The application will open in your default web browser. You can start performing the yoga poses in front of your webcam and receive feedback in real time.

How it Works

    Pose Detection: The app uses MediaPipe to detect key points on the user's body and compare their movements against predefined angles for each asana.
    Asana Validation: The app validates whether the pose matches the expected posture and displays a message when the pose is correctly done.
    Stage Progression: The user progresses through the yoga sequence. After each correct asana, the next one is unlocked, and a progress bar is updated.
    UI Interaction: The app uses Streamlit for a clean and responsive UI. It displays videos, progress bars, and status messages to help guide the user.

Contributing

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details.