# NutriMind food and nutrition classifier
# Written with <3 by Conner Smith
# Backend server-- Alpha 8 - 4/21/23
# This version is designed to strictly output the JSON data needed, without outputting anything else. 

import requests
import json
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os 
import datetime
import sys
import subprocess

timestamp = os.path.getmtime("keras_model.h5")
last_modified = datetime.datetime.fromtimestamp(timestamp)
# print(f"Classifier model updated on: {last_modified}")
# Clear out the nutrition information file
with open("nutrition.txt", "w") as f:
    f.write("")
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("keras_model.h5", compile=False)
# Load the labels
class_names = open("labels.txt", "r").readlines()
# print("!!BEGIN CLASSIFICATION!!")
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image
arg4image = sys.argv[1]
image_path = arg4image
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
prediction = model.predict(data, verbose=0)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]
# Pass the result to the nutrition API
query = class_name[2:].strip()
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'YOUR-KEY-HERE'})
if response.status_code == requests.codes.ok:
    # Write the classified food item to a text file
    # print(f"Class: {class_name[2:]}")
    with open("result.txt", "w") as f:
        f.write(class_name[2:])
    conf = round(confidence_score * 100, 2)
    # print(f"Confidence Score: {conf}%")
    response_data = response.json()[0]
    # Print nutrition information
    calories = response_data["calories"]
    # print("Calories:", calories)
    size = response_data["serving_size_g"]
    # print("Serving size:", size, "g")
    satfat = response_data["fat_saturated_g"]
    # print("Saturated Fat:", satfat, "g")
    totalfat = response_data["fat_total_g"]
    # print("Total Fat:", totalfat, "g")
    protein = response_data["protein_g"]
    # print("Protein:", protein, "g")
    sodium = response_data["sodium_mg"]
    # print("Sodium:", sodium, "mg")
    potassium = response_data["potassium_mg"]
    # print("Potassium:", potassium, "mg")
    cholesterol = response_data["cholesterol_mg"]
    # print("Cholesterol:", cholesterol, "mg")
    carbs = response_data["carbohydrates_total_g"]
    # print("Total Carbohydrates:", carbs, "g")
    fiber = response_data["fiber_g"]
    # print("Fiber:", fiber, "g")
    sugar = response_data["sugar_g"]
    # print("Sugar:", sugar, "g")
    # Save the nutrition information to a file 
    with open(f"nutrition.txt", "a") as f:
        f.write(f"Calories: {str(calories)}\n")
        f.write(f"Service size: {str(size)}g\n")
        f.write(f"Saturated Fat: {str(satfat)}g\n")
        f.write(f"Total Fat: {str(totalfat)}g\n")
        f.write(f"Protein: {str(protein)}g\n")
        f.write(f"Sodium: {str(sodium)}mg\n")
        f.write(f"Potassium: {str(potassium)}mg\n")
        f.write(f"Cholesterol: {str(cholesterol)}mg\n")
        f.write(f"Total Carbohydrates: {str(carbs)}g\n")
        f.write(f"Fiber: {str(fiber)}g\n")
        f.write(f"Sugar: {str(sugar)}g\n")
    # Read in file1.txt
    with open("result.txt", "r") as f:
        name = f.readline().strip()
        nutrition_info = {}
        for line in f:
            key, value = line.strip().split(': ')
            nutrition_info[key] = value
    # Read in file2.txt
    with open("nutrition.txt", "r") as f:
        nutrition_info2 = {}
        for line in f:
            key, value = line.strip().split(': ')
            nutrition_info2[key] = value
    # Combine the data from both files into one dictionary
    jsresult = {"name": name, "nutrition_info": nutrition_info2}
    # Output the result as a JSON object    
    # json_dict = json.loads(jsresult)

    # Convert the dictionary back to a JSON string with no backslashes or new lines
    clean_json_str = json.dumps(jsresult, indent=None)

    # Print the clean JSON string
    print(clean_json_str)
    with open(f"json.txt", "w") as f:
        f.write(clean_json_str)
else:
    # If the API encounters an error, log it to the file and display it in app
    print(f"Class: {class_name[2:]}")
    print(f"Confidence Score: {confidence_score}")
    print("Error:", response.status_code, response.text)
    with open(f"nutrition.txt", "a") as f:
        f.write(f"Nutrition retreival error. Please try again later.\n")
