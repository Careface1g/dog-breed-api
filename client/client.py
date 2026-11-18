import mimetypes
import os
from tkinter import Tk, filedialog
import requests

# CONSTANTS
SERVER_URL = "http://127.0.0.1:8000/predict"
TIMEOUT = 30  # seconds to wait for the server


# Methods


def choose_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose a dog photo",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")],
    )
    root.destroy()
    return file_path


def send_image(file_path):
    file_name = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0]

    with open(file_path, "rb") as image_file:
        files = {"file": (file_name, image_file, content_type)}
        response = requests.post(SERVER_URL, files=files, timeout=TIMEOUT)

    return response


def show_result(response):
    if response.status_code != 200:
        try:
            message = response.json()["detail"]
        except (ValueError, KeyError):
            message = response.text
        print(f"Error {response.status_code}: {message}")
        return

    data = response.json()

    if not data["is_dog"]:
        print(f"No dogo detected (dog probability: {data['dog_probability']:.1%})")
        return

    print("Dogo detected!\n")
    number = 1
    for prediction in data["predictions"]:
        breed = prediction["breed"].title()
        print(f"{number}. {breed:<30} {prediction['probability']:.1%}")
        number += 1

    if not data["confident"]:
        print("\nModel is not completely sure what the breed is.") # If its above 40% he is confident at the guess


def main():
    file_path = choose_image()
    if not file_path:
        print("No image selected.")
        return

    try:
        response = send_image(file_path)
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server.")
        return
    except requests.exceptions.Timeout:
        print(f"The server did not answer within {TIMEOUT} seconds.")
        return

    show_result(response)


if __name__ == "__main__":
    main()