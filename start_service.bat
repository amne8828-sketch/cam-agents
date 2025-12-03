@echo off
echo Starting Face Engine Microservice...
echo.
echo Installing dependencies if needed...
pip install -q -r requirements.txt
echo.
echo Starting FastAPI server on http://localhost:8000
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
