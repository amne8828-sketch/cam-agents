import cv2 as cv
import mediapipe as mp
import numpy as np
import time

class FaceDetector:
    def __init__(self):
        print("Initializing FaceDetector with MediaPipe...")
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, # 0 for short range, 1 for full range (5 meters)
            min_detection_confidence=0.5
        )
        
    def detect(self, image):
        """
        Detect faces using MediaPipe.
        Returns a list of dicts with bbox and confidence.
        """
        if image is None:
            return {"status": "failed", "faces": []}
            
        # Convert to RGB for MediaPipe
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)
        
        faces_data = []
        
        if results.detections:
            h, w, _ = image.shape
            
            for detection in results.detections:
                # Get bounding box
                bboxC = detection.location_data.relative_bounding_box
                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                width = int(bboxC.width * w)
                height = int(bboxC.height * h)
                
                # Ensure bbox is within bounds
                x = max(0, x)
                y = max(0, y)
                width = min(w - x, width)
                height = min(h - y, height)
                
                # Get score
                score = detection.score[0]
                
                face_info = {
                    "bbox": {"x": x, "y": y, "width": width, "height": height},
                    "confidence": float(score)
                }
                
                faces_data.append(face_info)
                
        return {
            "status": "success",
            "faces_detected": len(faces_data),
            "faces": faces_data
        }
