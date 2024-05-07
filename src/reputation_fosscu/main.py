from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from redis import Redis
from .utils import _get_airtable_data
import json
app = FastAPI()

BASE_DIR: Path = Path(__file__).resolve().parent

templates: Jinja2Templates = Jinja2Templates(
    directory=str(Path(BASE_DIR, "templates")))


@app.on_event("startup")
async def startup_event():
    app.state.redis = Redis(host='localhost', port=6379)


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    value = app.state.redis.get("entries")

    if value is None:
        data = await _get_airtable_data()
        app.state.redis.set("entries", data)
        app.state.redis.expire("entries", 10800)  # Refersh every 3 hours
    my_dict = json.loads(value)

    return templates.TemplateResponse(request=request, name="index.html", context={"data": my_dict})


@app.get("/search/", response_class=HTMLResponse)
async def search(request: Request, q: str):
    r = {"Name": "Test", "Discord Username": "Test", "XP": 'Test'}
    return templates.TemplateResponse(request=request, name="results.html", context={"result": r})
