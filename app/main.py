from fastapi import FastAPI, UploadFile

from app.validation import validate_image

app = FastAPI(title="Dog Breed Detector")


@app.post("/upload")
async def upload_image(file: UploadFile):
    contents = await file.read()
    image = validate_image(contents, file.content_type)

    return {
        "filename": file.filename,
        "format": image.format,
        "width": image.width,
        "height": image.height,
    }