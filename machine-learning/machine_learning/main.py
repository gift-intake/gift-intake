from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from machine_learning.api.endpoints import extraction, health, display

app = FastAPI(
    title="Gift Intake",
    description="Extracts entities from .msg email files using GLiNER.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extraction.router, prefix="/api/v1", tags=["extraction"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(display.router, prefix="/api/v1/display", tags=["display"])
