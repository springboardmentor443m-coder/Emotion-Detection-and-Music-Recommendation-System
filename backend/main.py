"""
FastAPI Backend Server for Emotion-Based Music Recommender

Endpoints:
    POST /api/detect-text   — Detect emotion from text input
    POST /api/detect-image  — Detect emotion from image upload
    GET  /api/health        — Health check
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from backend.text_models import detect_emotion_from_text
from backend.music_recommender import recommend_songs, get_all_songs, get_emotion_profiles

# ─── App Setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Emotion Music Recommender API",
    description="Detects emotions from text/images and recommends matching music",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-load image model to avoid TensorFlow startup overhead
_image_model_loaded = False


def _ensure_image_model():
    """Lazy-load the image model on first use."""
    global _image_model_loaded
    if not _image_model_loaded:
        from backend.image_models import detect_emotion_from_image  # noqa
        _image_model_loaded = True


# ─── Request/Response Models ─────────────────────────────────────────────────

class TextRequest(BaseModel):
    text: str
    num_songs: Optional[int] = 5


class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    all_scores: dict
    recommendation: dict


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Emotion Music Recommender",
        "version": "1.0.0",
    }


@app.post("/api/detect-text")
async def detect_text_emotion(request: TextRequest):
    """
    Detect emotion from text input and recommend songs.

    Args:
        request: JSON body with 'text' and optional 'num_songs'
    """
    try:
        # Detect emotion
        emotion_result = detect_emotion_from_text(request.text)

        # Get song recommendations
        recommendation = recommend_songs(
            emotion_result["emotion"],
            num_songs=request.num_songs or 5,
        )

        return {
            "emotion": emotion_result["emotion"],
            "confidence": emotion_result["confidence"],
            "all_scores": emotion_result["all_scores"],
            "recommendation": recommendation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@app.post("/api/detect-image")
async def detect_image_emotion(
    file: UploadFile = File(...),
    num_songs: int = 5,
):
    """
    Detect emotion from facial image upload and recommend songs.

    Args:
        file: Image file (JPEG/PNG)
        num_songs: Number of songs to recommend
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image (JPEG/PNG).",
            )

        # Read image bytes
        image_bytes = await file.read()

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")

        # Detect emotion from image
        from backend.image_models import detect_emotion_from_image
        emotion_result = detect_emotion_from_image(image_bytes)

        # Get song recommendations
        recommendation = recommend_songs(
            emotion_result["emotion"],
            num_songs=num_songs,
        )

        return {
            "emotion": emotion_result["emotion"],
            "confidence": emotion_result["confidence"],
            "all_scores": emotion_result["all_scores"],
            "face_detected": emotion_result["face_detected"],
            "recommendation": recommendation,
        }

    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.get("/api/songs")
async def list_all_songs():
    """Return all songs in the dataset."""
    try:
        songs = get_all_songs()
        return {"total": len(songs), "songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/emotions")
async def list_emotion_profiles():
    """Return emotion-to-audio-feature profiles."""
    return get_emotion_profiles()


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
