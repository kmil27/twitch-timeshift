from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timezone
import threading, os, json

import models
from models import add_streamer, remove_streamer, list_streamers, list_recordings, get_recording
from scheduler import scheduler_loop

app = FastAPI(title="Time-Shifted Twitch Stream Player")

# Serve static frontend files at /frontend
static_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/frontend", StaticFiles(directory=static_dir, html=True), name="frontend")

@app.on_event("startup")
def startup_event():
    threading.Thread(target=scheduler_loop, daemon=True).start()
    print("Background scheduler started.")

@app.get("/streamers")
def get_streamers():
    return {"streamers": list_streamers()}

@app.post("/streamers")
def add_streamer_endpoint(data: dict):
    name = data.get("name")
    tz = data.get("timezone")
    if not name:
        raise HTTPException(status_code=400, detail="Missing streamer name")
    add_streamer(name, tz)
    return {"status": "added", "name": name}

@app.delete("/streamers/{streamer_id}")
def delete_streamer_endpoint(streamer_id: int):
    remove_streamer(streamer_id)
    return {"status": "removed", "id": streamer_id}

@app.get("/recordings")
def get_recordings():
    return {"recordings": list_recordings()}

@app.get("/schedule")
def get_schedule():
    now_iso = datetime.now(timezone.utc).isoformat()
    return {"schedule": [r for r in list_recordings() if r["scheduled_time"] > now_iso and not r["played"]]}

@app.get("/play/{recording_id}")
def play_recording(recording_id: int):
    rec = get_recording(recording_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")

    scheduled_time = datetime.fromisoformat(rec["scheduled_time"])
    if datetime.now(timezone.utc) < scheduled_time:
        raise HTTPException(status_code=403, detail="Playback not available yet")

    video_path = rec["video_path"]
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")

    def iter_file():
        with open(video_path, "rb") as f:
            while chunk := f.read(8192):
                yield chunk
    return StreamingResponse(iter_file(), media_type="video/mp4")
