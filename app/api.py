from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers.api_controller import (
    router as api_router,
)
from app.controllers.dashboard_controller import (
    router as dashboard_router,
)


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"


app = FastAPI(
    title="Personal Executive AI",
    version="0.2.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


app.include_router(api_router)
app.include_router(dashboard_router)