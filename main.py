import cv2
import mediapipe as mp
import os
import math 
import numpy as np
import time  

# --- 1. KONFIGURACJA I AI ---
MODE = "DATASET"  # "CAMERA" lub "DATASET"
base_dataset_path = r"C:\Projekt_AI\YawDD_dataset"

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# FUNKCJA EAR 
def calculate_ear(eye_landmarks):
    v1 = math.sqrt((eye_landmarks[1][0] - eye_landmarks[5][0])**2 + 
                   (eye_landmarks[1][1] - eye_landmarks[5][1])**2)
    v2 = math.sqrt((eye_landmarks[2][0] - eye_landmarks[4][0])**2 + 
                   (eye_landmarks[2][1] - eye_landmarks[4][1])**2)
    h = math.sqrt((eye_landmarks[0][0] - eye_landmarks[3][0])**2 + 
                  (eye_landmarks[0][1] - eye_landmarks[3][1])**2)
    return (v1 + v2) / (2.0 * h)

# --- PARAMETRY ---
RECORDING_TIME = 10  
is_recording = False
video_writer = None

EAR_THRESHOLD = 0.22 
CLOSED_FRAMES_LIMIT = 15 
COUNTER = 0

# ==========================================
# 3. GŁÓWNA LOGIKA Z NAGRYWANIEM I POMIJANIEM
# ==========================================

def process_stream(cap, source_name):
    global COUNTER, is_recording, video_writer
    start_time = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                coords = [(lm.x * w, lm.y * h) for lm in face_landmarks.landmark]
                
                left_ear = calculate_ear([coords[i] for i in LEFT_EYE])
                right_ear = calculate_ear([coords[i] for i in RIGHT_EYE])
                avg_ear = (left_ear + right_ear) / 2.0

                # Rysowanie punktów MediaPipe
                for i in LEFT_EYE + RIGHT_EYE:
                    cv2.circle(frame, (int(coords[i][0]), int(coords[i][1])), 1, (0, 255, 0), -1)

                if avg_ear < EAR_THRESHOLD:
                    COUNTER += 1
                    if COUNTER >= CLOSED_FRAMES_LIMIT:
                        cv2.putText(frame, "!!! ALARM !!!", (50, 150), 1, 3, (0, 0, 255), 3)
                else:
                    COUNTER = 0

                # Informacje na ekranie
                cv2.putText(frame, f"Source: {source_name}", (10, 30), 1, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 60), 1, 1, (255, 255, 0), 2)

        # --- LOGIKA NAGRYWANIA ---
        if is_recording:
            elapsed_time = time.time() - start_time
            if elapsed_time <= RECORDING_TIME:
                cv2.circle(frame, (w - 30, 30), 10, (0, 0, 255), -1)
                cv2.putText(frame, f"REC: {int(RECORDING_TIME - elapsed_time)}s", (w - 150, 40), 1, 1.2, (0, 0, 255), 2)
                video_writer.write(frame)
            else:
                print("Nagrywanie zakończone.")
                is_recording = False
                video_writer.release()

        cv2.imshow('System Wykrywania Sennosci', frame)
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'): 
            return "QUIT"
        
        if key == ord('n') and MODE == "DATASET":
            print(f"Pomijanie filmu: {source_name}")
            return "SKIP"
        
        # 'r' - start nagrywania
        if key == ord('r') and not is_recording:
            print("Nagrywanie 10 sekund...")
            is_recording = True
            start_time = time.time()
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            h, w, _ = frame.shape
            video_writer = cv2.VideoWriter('demo_projektu.mp4', fourcc, 20.0, (w, h))

    cap.release()
    return "CONTINUE"

# ==========================================
# 4. START PROGRAMU
# ==========================================
if MODE == "CAMERA":
    print("Uzyj q do wyjscia")
    cap = cv2.VideoCapture(0)
    process_stream(cap, "Kamera LIVE")
elif MODE == "DATASET":
    print("Skanowanie folderów YawDD...")
    print("Uzyj n do pomijania biezacego filmu, q do wyjscia")
    for root, dirs, files in os.walk(base_dataset_path):
        for file in files:
            if file.endswith(".avi"):
                cap = cv2.VideoCapture(os.path.join(root, file))
                status = process_stream(cap, file)
                if status == "QUIT":
                    break
        else: continue
        break

cv2.destroyAllWindows()