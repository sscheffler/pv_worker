from fastapi import APIRouter
from starlette.responses import RedirectResponse

from app.logging_configuration import create_logger

logger = create_logger(name=__name__)


app_api_router = APIRouter()


@app_api_router.get("/")
async def redirect_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")
