#!/usr/bin/env python
"""
Test script to verify all model files can be found and loaded.
Run this from any directory to test path resolution.
"""

import os
import sys

def test_model_paths():
    print("=" * 60)
    print("MODEL FILE PATH VERIFICATION TEST")
    print("=" * 60)
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"\nProject Root: {project_root}")
    print(f"Current Working Directory: {os.getcwd()}")
    print()
    
    # Test face_detector.py
    print("-" * 60)
    print("Testing face_detector.py...")
    print("-" * 60)
    try:
        from face_detector import get_face_detector
        print("✓ face_detector imported successfully")
        
        # Test TensorFlow model
        print("\nAttempting to load TensorFlow model...")
        tf_model = get_face_detector(quantized=True)
        print("✓ TensorFlow model loaded successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test face_landmarks.py
    print("\n" + "-" * 60)
    print("Testing face_landmarks.py...")
    print("-" * 60)
    try:
        from face_landmarks import get_landmark_model
        print("✓ face_landmarks imported successfully")
        
        print("\nAttempting to load landmark model...")
        landmark_model = get_landmark_model()
        print("✓ Landmark model loaded successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Check all model files
    print("\n" + "-" * 60)
    print("Checking all model files exist...")
    print("-" * 60)
    
    models_dir = os.path.join(project_root, "models")
    required_files = {
        "TensorFlow Model": "opencv_face_detector_uint8.pb",
        "TensorFlow Config": "opencv_face_detector.pbtxt",
        "Caffe Config": "deploy.prototxt",
        "YOLO Weights": "yolov3.weights",
        "Landmark Data": "shape_predictor_68_face_landmarks.dat",
    }
    
    all_exist = True
    for name, filename in required_files.items():
        filepath = os.path.join(models_dir, filename)
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        size = f"({os.path.getsize(filepath) / 1024 / 1024:.2f} MB)" if exists else "(MISSING)"
        print(f"{status} {name}: {filename} {size}")
        if not exists:
            all_exist = False
    
    # Check for caffemodel files (any variation)
    print("\nCaffemodel files found:")
    caffemodel_files = [f for f in os.listdir(models_dir) if f.endswith('.caffemodel')]
    if caffemodel_files:
        for f in caffemodel_files:
            filepath = os.path.join(models_dir, f)
            size = os.path.getsize(filepath) / 1024 / 1024
            print(f"  ✓ {f} ({size:.2f} MB)")
    else:
        print("  ✗ No .caffemodel files found")
        all_exist = False
    
    print("\n" + "=" * 60)
    if all_exist:
        print("✓ ALL TESTS PASSED - All model files are accessible!")
    else:
        print("⚠ SOME TESTS FAILED - Check missing files above")
    print("=" * 60)
    
    return all_exist

if __name__ == '__main__':
    success = test_model_paths()
    sys.exit(0 if success else 1)
