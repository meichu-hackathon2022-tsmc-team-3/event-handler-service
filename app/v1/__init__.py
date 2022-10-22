from ..main import app

config = {}

from .routers import health

app.include_router(health.router,
    prefix="/api/v1/health",
    tags=['health']
)