from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import settings
from db import create_db_and_tables
from routes import health, tasks, auth

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RESTful API for Todo application with JWT authentication",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
# Allow all origins or specific origins from config
if settings.CORS_ORIGINS == "*":
    cors_origins = ["*"]
else:
    cors_origins = settings.cors_origins_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    create_db_and_tables()
    logger.info("Application startup complete")


@app.on_event("shutdown")
def on_shutdown():
    """Cleanup on shutdown."""
    logger.info("Application shutdown")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
