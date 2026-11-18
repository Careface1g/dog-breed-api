from fastapi import FastAPI, UploadFile
from fastapi.concurrency import run_in_threadpool
from app.validation import validate_image
from app.model import predict
from app.schemas import PredictionResponse

app = FastAPI(title="Dog Breed Detector")


@app.post("/predict")
async def predict_breed(file: UploadFile) -> PredictionResponse:
    contents = await file.read()
    image = validate_image(contents, file.content_type)
    return await run_in_threadpool(predict, image)