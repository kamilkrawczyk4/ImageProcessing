import urllib.request
import cv2
import numpy as np


def save_to_file(image, output_path):
  if not cv2.imwrite(output_path, image):
    raise OSError(f"Could not write image to {output_path}")
  print(f"Image saved to {output_path}")


url = "https://upload.wikimedia.org/wikipedia/mediawiki/a/a9/Example.jpg"

request = urllib.request.Request(url, headers={"User-Agent": "ImageProc/1.0"})
with urllib.request.urlopen(request) as response:
  image_array = np.frombuffer(response.read(), dtype=np.uint8)

image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

output_path = "unprocessed_image.jpg"
save_to_file(image, output_path)