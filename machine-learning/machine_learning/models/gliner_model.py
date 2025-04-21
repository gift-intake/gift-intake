from gliner import GLiNER
from machine_learning.models.model_results import ModelResults, ParsedEntity

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

ENTITY_LABELS = [
  "Interval", "Organization", "Money", "Date", "Phone", "Address", "Person", "Faculty", 
  "PaymentMethod", "Email", "GiftType", "Frequency", "Distribution"
]

def extract_entities(text: str) -> ModelResults:
    """
    Extract entities from the given text using the GLiNER model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        dict: A dictionary containing the extracted entities and their values.
    """
    
    entities = model.predict_entities(text, ENTITY_LABELS, threshold=0.70)
    
    results = []

    for entity in entities:
        results.append(ParsedEntity(entity=entity["label"], value=entity["text"]))

    return ModelResults(results=results)