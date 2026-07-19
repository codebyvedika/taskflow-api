import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app import models 

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A team task and project management API with status workflows, comments, and a full activity feed per task.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"success": False, "message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation error", "errors": exc.errors()},
    )


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": settings.PROJECT_NAME}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}