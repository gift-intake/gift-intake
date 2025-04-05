import json
from pathlib import Path
from pydantic import BaseModel, field_validator
from typing import List
from gliner import GLiNER

class Entity(BaseModel): 
    entity: str
    types: str
    
    @field_validator('entity')
    @classmethod
    def clean_entity(cls, v):
        if isinstance(v, str) and "," in v:
            return v.split(",")[0].strip()
        return v

class Result(BaseModel):
    text: str
    entities: List[Entity]

def generate_json_schema():
    return Result.model_json_schema()

labels = [
            "ConstituentID", "ConstituentType", "GiftAmount", "DonorFirstName",
            "DonorMiddleName", "DonorLastName", "OrganizationName", "GiftIntakeType",
            "DonorAddress", "DonorCity", "DonorProvince", "DonorCountry", "DonorPhone",
            "DonorEmail", "GiftCurrency", "GiftDate", "PaymentMethod"]

results = []
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
for label in labels:
    results.append({"label": label, "value": []})
    

