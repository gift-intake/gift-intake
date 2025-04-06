from fastapi import FastAPI

from machine_learning.api.endpoints import extraction, health

app = FastAPI(
    title="Gift Intake",
    description="Extracts entities from .msg email files using GLiNER.",
)

app.include_router(extraction.router, prefix="/api/v1", tags=["extraction"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
