from fastapi import FastAPI
from pydantic import BaseModel
from gliner import GLiNER
from typing import List

model = GLiNER.from_pretrained("urchade/gliner_large-v2.1")

app = FastAPI()

class Email(BaseModel):
    text: str

class EmailsList(BaseModel):
    emails: List[Email]

@app.post("/inference")
async def inference(input_data: EmailsList):
    results = []

    for email in input_data.emails:
        entities = model.predict_entities(email.text, ["Interval","Frequency","Date","Money","GiftType", "Department", "Person"], threshold=0.8)
        results.append({
            "text": email.text,
            "entities": entities
        })

    return {
        "results": results
    }