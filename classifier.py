import requests
import json
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image_path = "IMG_6216.jpeg"
image = Image.open(image_path).convert("RGB")

# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.LANCZOS)

# turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]
query = class_name[2:].strip()
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'rJH5ilDDCLmiao2g41toaw==mykxvTT6Y9BusDo7'})
if response.status_code == requests.codes.ok:
    print(f"Class: {class_name[2:]}")
    print(f"Confidence Score: {confidence_score}")
    response_data = response.json()[0]
    print("Calories:", response_data["calories"])
    print("Serving size:", response_data["serving_size_g"], "g")
    print("Saturated Fat:", response_data["fat_saturated_g"], "g")
    print("Total Fat:", response_data["fat_total_g"], "g")
    print("Protein:", response_data["protein_g"], "g")
    print("Sodium:", response_data["sodium_mg"], "mg")
    print("Potassium:", response_data["potassium_mg"], "mg")
    print("Cholesterol:", response_data["cholesterol_mg"], "mg")
    print("Total Carbohydrates:", response_data["carbohydrates_total_g"], "g")
    print("Fiber:", response_data["fiber_g"], "g")
    print("Sugar:", response_data["sugar_g"], "g")
else:
    print(f"Class: {class_name[2:]}")
    print(f"Confidence Score: {confidence_score}")
    print("Error:", response.status_code, response.text)

