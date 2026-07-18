from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Video Automation Agent API",
    description="Automated video creation and YouTube upload system for @ItsChachu-x8k",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# In-memory storage for jobs (use database in production)
jobs_db = {}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "channel": "@ItsChachu-x8k"}

@app.get("/")
async def root():
    return {
        "message": "Video Automation Agent API",
        "version": "1.0.0",
        "channel": "@ItsChachu-x8k",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/api/v1/videos")
async def list_videos():
    """List all generated videos"""
    return {"videos": [], "total": 0, "channel": "ItsChachu"}

@app.post("/api/v1/videos/generate")
async def generate_video(background_tasks: BackgroundTasks, content: dict):
    """Trigger video generation"""
    job_id = f"job_{datetime.utcnow().timestamp()}"
    jobs_db[job_id] = {"status": "generating", "content": content}
    
    background_tasks.add_task(process_video_generation, job_id, content)
    
    logger.info(f"Video generation queued for job {job_id}: {content}")
    return {"status": "queued", "job_id": job_id, "message": "Video generation queued for @ItsChachu-x8k"}

async def process_video_generation(job_id: str, content: dict):
    """Process video generation"""
    try:
        logger.info(f"Processing video for job {job_id}")
        
        # Generate video using content
        video_title = content.get("title", "Auto Generated Video")
        video_description = content.get("description", "")
        video_tags = content.get("tags", ["chachu", "automation"])
        
        # Simulate video generation
        video_path = f"/app/videos/{job_id}.mp4"
        
        jobs_db[job_id] = {
            "status": "generated",
            "title": video_title,
            "path": video_path,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Video generated for job {job_id}: {video_path}")
        
    except Exception as e:
        logger.error(f"Error generating video for job {job_id}: {str(e)}")
        jobs_db[job_id]["status"] = "failed"
        jobs_db[job_id]["error"] = str(e)

@app.post("/api/v1/videos/{video_id}/upload")
async def upload_video(video_id: str, background_tasks: BackgroundTasks):
    """Upload video to YouTube channel @ItsChachu-x8k"""
    if video_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Video job not found")
    
    job = jobs_db[video_id]
    if job["status"] != "generated":
        raise HTTPException(status_code=400, detail="Video not ready for upload")
    
    background_tasks.add_task(process_youtube_upload, video_id, job)
    
    logger.info(f"YouTube upload queued for video {video_id} to channel @ItsChachu-x8k")
    return {
        "status": "uploading",
        "video_id": video_id,
        "message": "Video upload started to @ItsChachu-x8k",
        "channel": "@ItsChachu-x8k"
    }

async def process_youtube_upload(job_id: str, job: dict):
    """Upload to YouTube"""
    try:
        logger.info(f"Uploading video {job_id} to @ItsChachu-x8k")
        
        body = {
            "snippet": {
                "title": job.get("title", "Auto Generated Video"),
                "description": job.get("description", "Auto-generated content by Video Automation Agent"),
                "tags": job.get("tags", ["chachu", "automation"]),
                "categoryId": "24",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            },
            "status": {
                "privacyStatus": "public",
                "publishAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Simulated upload (implement actual YouTube API upload)
        youtube_id = f"yt_{datetime.utcnow().timestamp()}"
        
        jobs_db[job_id] = {
            **job,
            "status": "uploaded",
            "youtube_id": youtube_id,
            "uploaded_at": datetime.utcnow().isoformat(),
            "channel": "@ItsChachu-x8k",
            "youtube_url": f"https://youtube.com/watch?v={youtube_id}"
        }
        
        logger.info(f"Video uploaded to @ItsChachu-x8k: {youtube_id}")
        
    except Exception as e:
        logger.error(f"Error uploading to YouTube: {str(e)}")
        jobs_db[job_id]["status"] = "upload_failed"
        jobs_db[job_id]["error"] = str(e)

@app.get("/api/v1/schedule")
async def get_schedule():
    """Get upload schedule"""
    return {
        "daily_time": "09:00",
        "timezone": "UTC",
        "enabled": True,
        "channel": "@ItsChachu-x8k",
        "status": "active"
    }

@app.put("/api/v1/schedule")
async def update_schedule(schedule: dict):
    """Update upload schedule"""
    logger.info(f"Schedule updated: {schedule}")
    return {
        "status": "updated",
        "schedule": schedule,
        "channel": "@ItsChachu-x8k"
    }

@app.get("/api/v1/analytics")
async def get_analytics():
    """Get channel analytics for @ItsChachu-x8k"""
    return {
        "channel": "@ItsChachu-x8k",
        "total_videos": 0,
        "total_views": 0,
        "total_subscribers": 0,
        "avg_watch_time": 0,
        "status": "monitoring"
    }

@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status"""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs_db[job_id]

@app.get("/api/v1/channel")
async def get_channel_info():
    """Get channel information"""
    return {
        "channel": "@ItsChachu-x8k",
        "channel_id": YOUTUBE_CHANNEL_ID,
        "status": "active",
        "automation": "enabled",
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
