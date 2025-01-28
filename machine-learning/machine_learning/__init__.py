from fastapi import FastAPI
from pydantic import BaseModel
from gliner import GLiNER
from typing import List
from ollama import chat

model = GLiNER.from_pretrained("urchade/gliner_large-v2.1")

app = FastAPI()

class Thread(BaseModel):
    text: str

class ThreadList(BaseModel):
    threads: List[Thread]

@app.post("/inference/ner")
def inference(input_data: ThreadList):
    results = []

    for thread in input_data.threads:
        entities = model.predict_entities(thread.text, ["Interval","Frequency","Date","Money","GiftType", "Department", "Person"], threshold=0.8)
        
        results.append({
            "text": thread.text,
            "entities": entities
        })

    return {
        "results": results
    }