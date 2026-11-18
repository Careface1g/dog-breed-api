import torch
from PIL import Image
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0

from app.schemas import BreedPrediction, PredictionResponse

# CONSTANTS
FIRST_DOG_ID = 151  # ImageNet classes 151 - 268 are dog breeds
LAST_DOG_ID = 268
DOG_THRESHOLD = 0.5  # total dog probability needed to count as a dog
CONFIDENCE_THRESHOLD = 0.4  # top breed probability needed to be "confident"
TOP_RESULTS = 3

# Model settings
weights = EfficientNet_B0_Weights.DEFAULT
model = efficientnet_b0(weights=weights)
model.eval()
preprocess = weights.transforms()
categories = weights.meta["categories"]


# Methods
def get_probabilities(image: Image.Image):
    image = image.convert("RGB")
    batch = preprocess(image)
    batch = batch.unsqueeze(0)  # model expects a batch, so we make a batch of 1

    with torch.no_grad():
        output = model(batch)

    probabilities = output.softmax(dim=1)
    return probabilities[0]  # results for our one image


def predict(image: Image.Image) -> PredictionResponse:
    probabilities = get_probabilities(image)

    dog_probabilities = probabilities[FIRST_DOG_ID:LAST_DOG_ID + 1]
    dog_probability = dog_probabilities.sum().item()
    dog_probability = round(dog_probability, 3)

    if dog_probability < DOG_THRESHOLD:
        return PredictionResponse(is_dog=False, dog_probability=dog_probability)

    top_probabilities, top_positions = dog_probabilities.topk(TOP_RESULTS)

    predictions = []
    for i in range(TOP_RESULTS):
        class_id = FIRST_DOG_ID + top_positions[i].item()
        breed = categories[class_id]
        probability = round(top_probabilities[i].item(), 3)
        predictions.append(BreedPrediction(breed=breed, probability=probability))

    confident = predictions[0].probability >= CONFIDENCE_THRESHOLD

    return PredictionResponse(
        is_dog=True,
        dog_probability=dog_probability,
        confident=confident,
        predictions=predictions,
    )