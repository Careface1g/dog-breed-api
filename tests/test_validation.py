import pytest
from fastapi import HTTPException
from app.validation import validate_image

def test_validate_image():
    with open("tests/images/dog1.jpg", "rb") as image_file:
        image_bytes = image_file.read()

    image = validate_image(image_bytes, "image/jpeg")

    assert image.format == "JPEG"

def test_wrong_file_type():
    with pytest.raises(HTTPException) as e:
        validate_image(b"fake PDF", "application/pdf")

    assert e.value.status_code == 415

def test_fake_image():
    with pytest.raises(HTTPException) as e:
        validate_image(b"fake JPG", "image/jpeg")

    assert e.value.status_code == 400