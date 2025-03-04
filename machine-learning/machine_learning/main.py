from fastapi import FastAPI
from machine_learning.schemas.InferenceRequest import SummaryRequest
from machine_learning.schemas.InferenceResponse import SummaryResponse
from machine_learning.api.endpoints.health import router as health_route

app = FastAPI(
    title="Gift Intake Inference API",
    description="API for performing NER and summarization on donation emails",
    version="0.0.1",
)


@app.post("/api/v1/inference/summary", response_model=SummaryResponse)
async def get_summary(request: SummaryRequest):
    """
    Summarize the input text
    """
    return SummaryResponse(summary="This is a summary of the input text")


app.include_router(health_route, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
