from machine_learning.models.model_results import ParsedEntity
from pydantic import BaseModel 

from typing import List

class InferenceResponseData(BaseModel):
    file_name: str
    file_contents: str
    entities: List[ParsedEntity]

class InferenceResponse(BaseModel):
  results: List[InferenceResponseData]