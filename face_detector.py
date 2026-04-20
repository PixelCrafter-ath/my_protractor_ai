import cv2
import numpy as np
import os

def get_face_detector(modelFile=None, configFile=None, quantized=False):
    """
    Load face detection model with robust path resolution.
    Works regardless of where the script is run from.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if quantized:
        # Use TensorFlow quantized model
        if modelFile is None:
            modelFile = os.path.join(script_dir, "models", "opencv_face_detector_uint8.pb")
        if configFile is None:
            configFile = os.path.join(script_dir, "models", "opencv_face_detector.pbtxt")
        
        # Verify files exist
        if not os.path.exists(modelFile):
            raise FileNotFoundError(f"TensorFlow model not found: {modelFile}")
        if not os.path.exists(configFile):
            raise FileNotFoundError(f"TensorFlow config not found: {configFile}")
        
        print(f"[Face Detector] Loading TensorFlow model from: {modelFile}")
        model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
    else:
        # Use Caffe model - search for the correct filename
        models_dir = os.path.join(script_dir, "models")
        
        if modelFile is None:
            # Search for caffemodel file (handle variations in filename)
            caffemodel_files = [f for f in os.listdir(models_dir) if f.endswith('.caffemodel')]
            if not caffemodel_files:
                raise FileNotFoundError(f"No .caffemodel file found in {models_dir}")
            # Use the first caffemodel file found
            modelFile = os.path.join(models_dir, caffemodel_files[0])
            print(f"[Face Detector] Found caffemodel: {caffemodel_files[0]}")
        
        if configFile is None:
            configFile = os.path.join(script_dir, "models", "deploy.prototxt")
        
        # Verify files exist
        if not os.path.exists(modelFile):
            raise FileNotFoundError(f"Caffe model not found: {modelFile}")
        if not os.path.exists(configFile):
            raise FileNotFoundError(f"Caffe config not found: {configFile}")
        
        print(f"[Face Detector] Loading Caffe model from: {modelFile}")
        model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    
    print("[Face Detector] Model loaded successfully!")
    return model


def find_faces(img, model):
    h, w = img.shape[:2]
    
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)),
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )
    
    model.setInput(blob)
    res = model.forward()
    
    faces = []
    
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])
    
    return faces
