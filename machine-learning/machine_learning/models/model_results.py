from typing import List
from dataclasses import dataclass

@dataclass
class ParsedEntity:
    entity: str
    value: str

@dataclass
class ModelResults:
    results: List[ParsedEntity]