from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, save, stats, notifications, prompts, user
import time
import json
from supabase import create_client, Client
import os
import dotenv

dotenv.load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["chrome-extension://enfcjmbdbldomiobfndablekgdkmcipd", "https://chatgpt.com", "https://claude.ai", "https://chat.mistral.ai", "https://copilot.microsoft.com"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Include all routers
app.include_router(auth.router)
app.include_router(save.router)
app.include_router(stats.router)
app.include_router(notifications.router)
app.include_router(user.router)
app.include_router(prompts.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Jaydai API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring - no auth required."""
    start_time = time.time()
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "components": {}
    }
    
    # Check API
    health["components"]["api"] = {"status": "healthy"}
    
    # Check Supabase connection
    try:
        # Create a fresh client for the health check
        supabase_client = create_client(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )
        
        # Try listing buckets - this is a lightweight operation
        # that doesn't depend on application-specific tables
        supabase_client.storage.list_buckets()
        
        health["components"]["database"] = {
            "status": "healthy",
            "responseTime": f"{(time.time() - start_time) * 1000:.2f}ms"
        }
    except Exception as e:
        health["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health["status"] = "degraded"
    
    # Set appropriate status code based on overall health
    if health["status"] != "healthy":
        return Response(content=json.dumps(health), media_type="application/json", status_code=503)
    
    return health

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)