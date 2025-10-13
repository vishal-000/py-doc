import cv2
import os
import numpy as np
import json
from pathlib import Path

# ========== PATH CONFIG ==========
DATASET_DIR = Path("dataset")
TRAINER_DIR = Path("trainer")
MODEL_PATH = TRAINER_DIR / "lbph_model.yml"
LABEL_MAP_PATH = TRAINER_DIR / "label_map.json"
HAAR_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Make directories if not exist
DATASET_DIR.mkdir(exist_ok=True)
TRAINER_DIR.mkdir(exist_ok=True)

# ========== STEP 1: CAPTURE IMAGES ==========
def capture_images(person_name, num_images=20):
    """Capture face images for a given person using webcam."""
    person_dir = DATASET_DIR / person_name
    person_dir.mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(HAAR_CASCADE)
    count = 0
    print(f"[INFO] Capturing {num_images} images for {person_name}. Press 'q' to quit early.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y+h, x:x+w]
            cv2.imwrite(str(person_dir / f"{count}.jpg"), face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, f"Image {count}/{num_images}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.imshow("Capturing Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count >= num_images:
            break

    print(f"[INFO] Collected {count} images for {person_name}.")
    cam.release()
    cv2.destroyAllWindows()


# ========== STEP 2: TRAIN MODEL ==========
def train_model():
    """Train the LBPH recognizer using all images in dataset."""
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(HAAR_CASCADE)

    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for person_dir in DATASET_DIR.iterdir():
        if not person_dir.is_dir():
            continue
        name = person_dir.name
        label_map[current_label] = name

        for img_path in person_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected = detector.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in detected:
                faces.append(gray[y:y+h, x:x+w])
                labels.append(current_label)

        current_label += 1

    if len(faces) == 0:
        print("[ERROR] No faces found in dataset.")
        return

    recognizer.train(faces, np.array(labels))
    recognizer.write(str(MODEL_PATH))
    with open(LABEL_MAP_PATH, "w") as f:
        json.dump(label_map, f)

    print(f"[INFO] Model trained successfully with {len(label_map)} persons.")


# ========== STEP 3: REAL-TIME RECOGNITION ==========
def recognize_faces(threshold=75):
    """Recognize faces in real time using webcam."""
    if not MODEL_PATH.exists():
        print("[INFO] No trained model found. Training a new one...")
        train_model()

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL_PATH))

    with open(LABEL_MAP_PATH, "r") as f:
        label_map = json.load(f)

    detector = cv2.CascadeClassifier(HAAR_CASCADE)
    cam = cv2.VideoCapture(0)
    print("[INFO] Recognition started. Press 'q' to quit, 'r' to retrain.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi)

            if confidence < threshold:
                name = label_map.get(str(label)) or label_map.get(int(label), "Unknown")
                color = (0, 255, 0)
            else:
                name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{name} ({confidence:.0f})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            print("[INFO] Retraining model...")
            train_model()
            recognizer.read(str(MODEL_PATH))

    cam.release()
    cv2.destroyAllWindows()


# ========== MAIN MENU ==========
if __name__ == "__main__":
    while True:
        print("\n========== FACE RECOGNITION SYSTEM ==========")
        print("1. Capture new face data")
        print("2. Train model")
        print("3. Recognize faces (webcam)")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            name = input("Enter person's name: ").strip().lower()
            capture_images(name)
        elif choice == '2':
            train_model()
        elif choice == '3':
            recognize_faces()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
