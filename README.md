# Face Engine Microservice

A lightweight, FastAPI-based microservice for face detection using MediaPipe.

## Features
- **FastAPI**: High performance, easy to use.
- **MediaPipe**: Efficient on-device face detection.
- **Dockerized**: Ready for deployment.

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run server**:
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`.

## Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up --build -d
```

### Using Docker CLI
1. **Build image**:
   ```bash
   docker build -t face-engine .
   ```

2. **Run container**:
   ```bash
   docker run -d -p 8000:8000 --name face-engine face-engine
   ```

## API Endpoints

- `GET /`: Status check.
- `GET /health`: Health check.
- `POST /api/v1/detect`: Detect faces.
  - Body: `{"image": "base64_string"}`
