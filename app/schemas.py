from pydantic import BaseModel


class BreedPrediction(BaseModel):
    breed: str
    probability: float


class PredictionResponse(BaseModel):
    is_dog: bool
    dog_probability: float
    confident: bool | None = None
    predictions: list[BreedPrediction] = []