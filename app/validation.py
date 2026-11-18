from io import BytesIO

from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "JPG"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image(contents: bytes, content_type: str | None) -> Image.Image:
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{content_type}'. Allowed: JPEG, PNG, WEBP.",
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    try:
        image = Image.open(BytesIO(contents))
        image.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="The file is not a valid image.")

    if image.format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=415, detail=f"Image format '{image.format}' is not supported.")

    return Image.open(BytesIO(contents))