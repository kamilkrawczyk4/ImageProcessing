import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt


def save_to_file(image, output_path):
  if not cv2.imwrite(output_path, image):
    raise OSError(f"Could not write image to {output_path}")
  print(f"Image saved to {output_path}")

#Assessing the quality of an image (so far based on)
def assess_quality(hist, sl_threshold):
   prob = hist/hist.sum()
   shadows = np.sum(prob[0:sl_threshold]) * 100
   lights = np.sum(prob[256-sl_threshold:256]) * 100
   if shadows > 5 or lights > 5:
      return False
   return True
   


url = "https://upload.wikimedia.org/wikipedia/mediawiki/a/a9/Example.jpg"

request = urllib.request.Request(url, headers={"User-Agent": "ImageProc/1.0"})
with urllib.request.urlopen(request) as response:
  image_array = np.frombuffer(response.read(), dtype=np.uint8)

image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

output_path = "unprocessed_image.jpg"
save_to_file(image, output_path)

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

plt.figure()
hist = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
plt.xlabel("Jasność piksela (0–255)")
plt.ylabel("Liczba pikseli")
plt.plot(hist)
plt.savefig("histogram_whole.jpg")

colors = ("b", "g", "r")

for i, col in enumerate(colors):
    hist_rgb = cv2.calcHist([image], [i], None, [256], [0, 256])
    plt.plot(hist_rgb, color=col, label=col.upper())

plt.xlim([0,256])
plt.legend()
plt.savefig("histogram_rgb.jpg")

print("Dobra jakość" if assess_quality(hist, 6) else "Zła jakość")