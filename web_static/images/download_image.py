#!/usr/bin/python3
import requests

image_url = "https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/268/logo.png"
response = requests.get(image_url)

if response.status_code == 200:
    with open("logo.png", "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully as 'logo.png'")
else:
    print("Failed to download the image")

