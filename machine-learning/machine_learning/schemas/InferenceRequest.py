from pydantic import BaseModel
from typing import List, Dict


class TextThread(BaseModel):
    text: str


class InferenceRequest(BaseModel):
    threads: List[TextThread]


class SummaryRequest(BaseModel):
    text: str
