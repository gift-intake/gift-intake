from machine_learning.models.model_results import ParsedEntity
from pydantic import BaseModel 

from typing import List

class InferenceResponseData(BaseModel):
    """
    Represents inference results for a single file.
    
    Contains the file information and any entities extracted from the file
    during the inference process.
    
    Potential entity types include:
    - Interval: Time intervals between events
    - Organization: Names of organizations/institutions
    - Money: Monetary amounts and currencies
    - Date: Calendar dates and time references
    - Phone: Phone numbers
    - Address: Physical addresses
    - Person: Names of individuals
    - Faculty: Faculty members or departments
    - PaymentMethod: Methods of payment
    - Email: Email addresses
    - GiftType: Types of gifts (e.g., cash, stock, etc.)
    - Frequency: Frequency of payments or donations
    - Distribution: Information about fund distribution
    """
    file_name: str
    file_contents: str
    entities: List[ParsedEntity]

class InferenceResponse(BaseModel):
  results: List[InferenceResponseData]