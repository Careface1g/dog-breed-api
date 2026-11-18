from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.validation import MAX_FILE_SIZE
client = TestClient(app)


def send_test_image(image_name):
    with open(f"tests/images/{image_name}", "rb") as image_file:
        files = {"file": (image_name, image_file, "image/jpeg")}
        response = client.post("/predict", files=files)
    return response


def test_predict_pdf_rejected():
    files = {"file": ("document.pdf", b"fake PDF", "application/pdf")}
    response = client.post("/predict", files=files)

    assert response.status_code == 415


@pytest.mark.parametrize("image_name", ["dog1.jpg", "dog2.jpg", "dog3.jpg"])
def test_predict_dogs(image_name):
    response = send_test_image(image_name)

    assert response.status_code == 200
    data = response.json()
    assert data["is_dog"] is True
    assert len(data["predictions"]) == 3


@pytest.mark.parametrize("image_name", ["cow.jpg", "cup.jpg"])
def test_catch_non_dogos(image_name):
    response = send_test_image(image_name)

    assert response.status_code == 200
    data = response.json()
    assert data["is_dog"] is False
    assert data["confident"] is None
    assert data["predictions"] == []

def test_max_file_size():
    files = {"file": ("fake_image.jpg", b"0" * (MAX_FILE_SIZE + 1), "image/jpeg")}
    response = client.post("/predict", files=files)

    assert response.status_code == 413

def test_no_file_sent():
    response = client.post("/predict")

    assert response.status_code == 422
