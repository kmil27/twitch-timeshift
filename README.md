# Time-Shifted Twitch Stream Player

## Overview
The **Time-Shifted Twitch Stream Player** automatically records Twitch live streams and replays them at the next local occurrence of their start time in the user’s timezone. This allows viewers to watch streams as if they were live, without rewind or pause functionality.

## Features
✅ **Automatically records Twitch streams when they go live**  
✅ **Schedules replays based on local time zones**  
✅ **Plays streams at the exact scheduled time with no seeking or pausing**  
✅ **Simple web UI to manage streamers and view scheduled replays**  
✅ **Fully self-hosted with Docker for easy deployment**  

---

## 📌 Setup Guide

### **1️⃣ Install Prerequisites**
Ensure you have:
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- A [Twitch Developer Account](https://dev.twitch.tv/console/apps) (for API credentials)

### **2️⃣ Clone the Repository**
```bash
 git clone https://github.com/YOUR-USERNAME/twitch-timeshift.git
 cd twitch-timeshift
```

### **3️⃣ Set Up Twitch API Credentials**
1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console/apps) and create a new application.
2. Copy your **Client ID** and **Client Secret**.
3. Open `docker-compose.yml` and update the environment variables:
```yaml
environment:
  TWITCH_CLIENT_ID: "your_client_id"
  TWITCH_CLIENT_SECRET: "your_client_secret"
  USER_TIMEZONE: "America/New_York"  # Change to your local timezone
```

### **4️⃣ Start the Docker Container**
```bash
 docker-compose up --build -d
```
- This will build and start the service in the background.

### **5️⃣ Access the Web UI**
Open your browser and go to:
```
http://localhost:8000/frontend/
```
Here you can:
- **Add/Remove streamers**
- **See upcoming scheduled replays**
- **Watch live replays** (No seeking or pausing!)

---

## 📜 How It Works
1. **Add a Twitch streamer** in the web UI.
2. The system **automatically records** when they go live.
3. The recording is **scheduled for playback at the next local occurrence** of its start time.
4. The playback starts **automatically at the correct time**, emulating a live stream.

⏳ **Example:**  
A Twitch stream starts at **8:00 PM EST**. If you are in **London (GMT)**, it will be played back at **8:00 PM GMT** the next time 8 PM happens in your timezone.

---

## 🔧 Updating the App
To pull the latest updates:
```bash
 git pull
 docker-compose up --build -d
```

---

## ❌ Stopping the Service
```bash
 docker-compose down
```
- Your recorded videos and settings are saved in the `data/` folder.

---

## 🚀 Enjoy Watching Twitch on Your Own Schedule! 🎉


-this is currently brpken, feel free to help with de-bugging
