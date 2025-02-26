import os, subprocess, threading, requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from models import add_recording, finish_recording, list_streamers

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
TWITCH_API_BASE = "https://api.twitch.tv/helix"

def get_twitch_token():
    resp = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    return resp.json()["access_token"]

def calculate_next_occurrence(start_time_utc, streamer_timezone, user_timezone):
    streamer_tz = ZoneInfo(streamer_timezone or "UTC")
    user_tz = ZoneInfo(user_timezone or "UTC")
    start_local = start_time_utc.astimezone(streamer_tz)
    now_local = datetime.now(user_tz)
    next_occurrence = now_local.replace(hour=start_local.hour, minute=start_local.minute, second=0)
    if next_occurrence < now_local:
        next_occurrence += timedelta(days=1)
    return next_occurrence.astimezone(ZoneInfo("UTC")).isoformat()

def record_stream(streamer_name, streamer_timezone):
    start_time_utc = datetime.utcnow()
    rec_id = add_recording(streamer_name, start_time_utc.isoformat())

    video_file = f"data/videos/{streamer_name}_{start_time_utc.strftime('%Y%m%d_%H%M%S')}.mp4"
    subprocess.run(["streamlink", f"twitch.tv/{streamer_name}", "best", "-o", video_file], check=True)

    scheduled_iso = calculate_next_occurrence(start_time_utc, streamer_timezone, os.environ.get("USER_TIMEZONE", "UTC"))
    finish_recording(rec_id, datetime.utcnow().isoformat(), video_file, scheduled_iso)
