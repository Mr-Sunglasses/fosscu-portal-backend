from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from redis import Redis
from .utils import _get_airtable_data
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FOSSCU Portal", 
              description="Member directory for FOSSCU (Free and Open Source Community)",
              version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR: Path = Path(__file__).resolve().parent

templates: Jinja2Templates = Jinja2Templates(
    directory=str(Path(BASE_DIR, "templates")))

# Mount static files if needed
# app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, "static"))), name="static")


@app.on_event("startup")
async def startup_event():
    try:
        # Get Redis connection details from environment variables or use defaults
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        
        logger.info(f"Connecting to Redis at {redis_host}:{redis_port}")
        
        app.state.redis = Redis(
            host=redis_host, 
            port=redis_port,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            decode_responses=True  # Automatically decode response to str
        )
        # Test connection
        app.state.redis.ping()
        logger.info(f"✅ Connected to Redis successfully at {redis_host}:{redis_port}")
    except Exception as e:
        logger.warning(f"⚠️ Redis connection error: {e}")
        logger.info("Using in-memory cache instead")
        # Fallback to a simple in-memory cache
        app.state.cache = {}
        app.state.redis = None


@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'redis') and app.state.redis:
        app.state.redis.close()
        logger.info("📝 Redis connection closed")


@app.get('/api/health', response_class=JSONResponse)
async def health_check():
    """Health check endpoint"""
    redis_status = "connected" if (hasattr(app.state, 'redis') and app.state.redis) else "disconnected"
    return {"status": "ok", "redis": redis_status}


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    try:
        data = []
        
        if hasattr(app.state, 'redis') and app.state.redis:
            # Use Redis if available
            cached_data = app.state.redis.get("entries")
            
            if cached_data is None:
                logger.info("Cache miss. Fetching data from Airtable")
                data_str = await _get_airtable_data()
                app.state.redis.set("entries", data_str)
                app.state.redis.expire("entries", 10800)  # Refresh every 3 hours
                data = json.loads(data_str)
            else:
                logger.info("Cache hit. Using cached data")
                if isinstance(cached_data, str):
                    data = json.loads(cached_data)
                else:
                    # Already a string due to decode_responses=True
                    data = json.loads(cached_data)
        else:
            # Fallback to in-memory cache
            if hasattr(app.state, 'cache') and "entries" in app.state.cache:
                logger.info("Using in-memory cache")
                data = app.state.cache["entries"]
            else:
                logger.info("In-memory cache miss. Fetching data from Airtable")
                data_str = await _get_airtable_data()
                data = json.loads(data_str)
                app.state.cache["entries"] = data

        # Sort data by XP (high to low)
        try:
            data.sort(key=lambda x: float(x.get("XP", 0)), reverse=True)
        except Exception as e:
            logger.error(f"Error sorting data: {e}")
            # Continue without sorting if there's an error
        
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={"data": data}
        )
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        # Return error page
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": str(e)},
            status_code=500
        )


@app.get("/search/", response_class=HTMLResponse)
async def search(request: Request, q: str = ""):
    try:
        # Get all data first
        all_data = []
        
        if hasattr(app.state, 'redis') and app.state.redis:
            cached_data = app.state.redis.get("entries")
            if cached_data:
                all_data = json.loads(cached_data)
            else:
                data_str = await _get_airtable_data()
                all_data = json.loads(data_str)
                app.state.redis.set("entries", data_str)
                app.state.redis.expire("entries", 10800)
        else:
            # Fallback to in-memory cache or fetch new data
            if hasattr(app.state, 'cache') and "entries" in app.state.cache:
                all_data = app.state.cache["entries"]
            else:
                data_str = await _get_airtable_data()
                all_data = json.loads(data_str)
                if hasattr(app.state, 'cache'):
                    app.state.cache["entries"] = all_data
        
        # If empty query, return all results sorted
        if not q:
            all_data.sort(key=lambda x: float(x.get("XP", 0)), reverse=True)
            return templates.TemplateResponse(
                request=request, 
                name="results.html", 
                context={"results": all_data}
            )
        
        # Filter results based on the query
        q = q.lower()
        results = [
            item for item in all_data if 
            q in item.get("Name", "").lower() or 
            q in item.get("Discord Username", "").lower()
        ]
        
        # Sort results by XP
        results.sort(key=lambda x: float(x.get("XP", 0)), reverse=True)
        
        return templates.TemplateResponse(
            request=request, 
            name="results.html", 
            context={"results": results}
        )
    except Exception as e:
        logger.error(f"Error in search route: {e}")
        return templates.TemplateResponse(
            request=request,
            name="results.html",
            context={"results": [{"Name": "Error", "Discord Username": str(e), "XP": 0}]}
        )