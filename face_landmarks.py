import cv2
import numpy as np
import os
import dlib

def get_landmark_model():
    """
    Load dlib facial landmark model with robust path resolution.
    Works regardless of where the script is run from.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try multiple possible locations for the shape predictor
    possible_paths = [
        os.path.join(script_dir, "gaze_tracking", "trained_models", "shape_predictor_68_face_landmarks.dat"),
        os.path.join(script_dir, "models", "shape_predictor_68_face_landmarks.dat"),
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        raise FileNotFoundError(
            f"shape_predictor_68_face_landmarks.dat not found in:\n" +
            "\n".join(possible_paths)
        )
    
    print(f"[Landmark Model] Loading from: {model_path}")
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_path)
    
    print("[Landmark Model] Model loaded successfully!")
    return detector, predictor


def get_square_box(box):
    left_x = box[0]
    top_y = box[1]
    right_x = box[2]
    bottom_y = box[3]

    box_width = right_x - left_x
    box_height = bottom_y - top_y
    diff = box_height - box_width
    delta = int(abs(diff) / 2)

    if diff == 0:
        return box
    elif diff > 0:
        left_x -= delta
        right_x += delta
        if diff % 2 == 1:
            right_x += 1
    else:
        top_y -= delta
        bottom_y += delta
        if diff % 2 == 1:
            bottom_y += 1

    return [left_x, top_y, right_x, bottom_y]


def move_box(box, offset):
    return [
        box[0] + offset[0],
        box[1] + offset[1],
        box[2] + offset[0],
        box[3] + offset[1],
    ]


def detect_marks(img, model, face):
    detector, predictor = model

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rect = dlib.rectangle(
        int(face[0]),
        int(face[1]),
        int(face[2]),
        int(face[3])
    )

    shape = predictor(gray, rect)

    marks = []
    for i in range(68):
        x = shape.part(i).x
        y = shape.part(i).y
        marks.append((x, y))

    return np.array(marks)
