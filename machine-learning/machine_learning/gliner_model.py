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
    "Interval", "Organization", "Money", "Date", "Phone", "Address", "Person", "Faculty", 
    "PaymentMethod", "Email", "Gift Type", "Frequency", "Distribution"]

test_set_path = Path("results.jsonl")

results = []

with open(test_set_path, "r") as f:
    for line in f:
        raw_data = json.loads(line)
        try:
            result = Result(**raw_data)
            filtered_entities = [entity for entity in result.entities if entity.types in labels]
            result.entities = filtered_entities
            results.append(result)
        except Exception as e:
            print(f"Error parsing line: {e}")
            print(f"Problematic data: {raw_data}")

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

ner_results = []
for result in results:
    text = result.text
    entities = model.predict_entities(text, labels)
    classified = [Entity(entity=entity["text"], types=entity["label"]) for entity in entities]
    ner_results.append(Result(text=text, entities=classified))

# Save JSON Schema
schema = generate_json_schema()
with open("schema.json", "w") as f:
    json.dump(schema, f, indent=4)

print("JSON Schema saved to schema.json")
