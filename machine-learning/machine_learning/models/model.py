from pydantic import BaseModel, Field
from typing import List

class EntityWithConfidence(BaseModel):
    """Base class for any entity that includes a confidence score."""
    entity: str
    value: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class InferenceRequest(BaseModel):
    """Request model to extract entities from text."""
    text: str

class InferenceResponse(BaseModel):
    """Response model to return extracted entities."""
    entities: List[EntityWithConfidence]
