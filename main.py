from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2 as cv
import numpy as np
import uvicorn
from detector import FaceDetector
import base64
from pydantic import BaseModel

app = FastAPI(title="Face Engine Microservice")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector
detector = FaceDetector()

class ImageRequest(BaseModel):
    image: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "Face Engine Microservice"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/detect")
async def detect_faces_api(data: ImageRequest):
  
    try:
        image_data = data.image
        if not image_data:
            raise HTTPException(status_code=400, detail="No image data provided")
            
        # Remove header if present
        if "," in image_data:
            image_data = image_data.split(",")[1]
            
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv.imdecode(nparr, cv.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
            
        result = detector.detect(image)
        
        # Transform result to match client expectation if needed
        # Client expects: {"faces": [...]}
        # Detector returns: {"status": "success", "faces_detected": n, "faces": [...]}
        # So it matches well enough (client gets .get("faces", []))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
