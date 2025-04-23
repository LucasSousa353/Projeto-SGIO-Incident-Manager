from fastapi import FastAPI
from app.api import routes
from app.core.config import get_settings
from app.routes import auth


settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    version="1.0.0"
)

app.include_router(routes.router, prefix=settings.api_v1_str)
app.include_router(auth.router, prefix=settings.api_v1_str)
