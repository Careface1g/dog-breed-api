# Dog Breed Detector API

A FastAPI project that takes a photo and returns the 3 most likely dog breeds. If there's no dog in the photo, or the model isn't sure, it tells you that instead.

I got the idea from an earlier version I made for my Godot game.

It uses a pretrained model (EfficientNet-B0) and checks uploads before running it, so wrong or broken files get a clear error.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
fastapi dev app/main.py
```

Then open http://127.0.0.1:8000/docs to try it, or run `python client/client.py` to pick an image and see the result.

Example result:

```
Doggo detected!
1. Chihuahua                      96.8%
2. Pembroke                       0.3%
3. Toy Terrier                    0.2%
```

## Tests

```powershell
pip install -r requirements-dev.txt
pytest -v
```
