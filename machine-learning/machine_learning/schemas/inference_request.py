from pydantic import BaseModel

from typing import List

class InferenceRequest(BaseModel):
    text: str