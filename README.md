Treść wiadomości Gemini
Oto tekst do skopiowania, sformatowany jako czysty plik Markdown. Bez problemu użyjesz go jako README.md w swoim repozytorium na GitHubie.

Real-Time Driver Drowsiness Detection System 🚗👁️
Overview
A Computer Vision Proof of Concept (PoC) designed to monitor driver alertness in real-time. The system processes video streams (RGB, 30 fps) to extract facial landmarks and computes the Eye Aspect Ratio (EAR) to detect microsleeps and prolonged fatigue.

This project bridges the gap between Deep Learning (Landmark Regression) and Behavioral Classification, offering a lightweight alternative to heavy CNN models, making it highly suitable for Edge AI deployment in automotive environments.

The Algorithm: Eye Aspect Ratio (EAR)
Instead of relying on basic Haar Cascades, this system utilizes Google's MediaPipe Face Mesh to accurately map 468 3D facial landmarks. The alertness is determined by calculating the distance between the eyelids.

The EAR is calculated using the following geometric model:

EAR = ( |p2 - p6| + |p3 - p5| ) / ( 2 * |p1 - p4| )

Where p1 to p6 are the 2D coordinates of the eye landmarks.

A threshold of 0.22 is used for drowsiness detection.

A moving window of 15 frames acts as an alarm trigger to filter out natural blinking.

Validation & Dataset
The algorithm was rigorously tested against the YawDD dataset (4.94 GB of professional driving footage). It demonstrates high resilience to head rotations, varying lighting conditions, and drivers wearing glasses.

How to Run
Clone the repository and set up the virtual environment:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
Run the main pipeline:

Bash
python main.py
Note: You can switch between CAMERA (live webcam feed) and DATASET mode inside the main.py configuration block.

Controls
q - Quit the application

n - Skip to the next video (Dataset mode)

r - Record a 10-second demo snippet (demo_projektu.mp4)
