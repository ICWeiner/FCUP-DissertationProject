from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

router = APIRouter()

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request,
                                                     "title": "GNS3 - Evaluation platform",
                                                     "description": "GNS3 - Evaluation platform"})