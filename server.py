from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary memory to hold the feed
feed_database = []

class IncomingPost(BaseModel):
    image_url: str
    caption: str

# 1. THE WEBHOOK (Where your main app sends the data)
@app.post("/webhook")
def receive_webhook(post: IncomingPost):
    new_post = {
        "id": len(feed_database) + 1,
        "image": post.image_url,
        "caption": post.caption,
        "timestamp": "JUST NOW"
    }
    # Insert new post at the top of the feed
    feed_database.insert(0, new_post)
    print(f"📸 POST RECEIVED: {post.caption[:20]}...")
    return {"status": "success"}

# 2. THE FEED API (Where the HTML page reads the data)
@app.get("/feed")
def get_feed():
    return feed_database

if __name__ == "__main__":
    print("📱 Mock Instagram Server running on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)