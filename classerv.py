# print("NutriMind food and nutrition classifier")
# print("Written with <3 by Conner Smith")
# print("Backend server & image classifier -- Beta revision 1- 4/26/23")

import requests
import json
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os 
import datetime
import sys
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # decode JSON data
        request_data = json.loads(post_data.decode('utf-8'))
        
        # get arguments
        arg1 = request_data.get('arg1')
        # arg2 = request_data.get('arg2') -- this is not needed yet, but I'll leave it commented out in case I need it. 
        np.set_printoptions(suppress=True)
        model = load_model("keras_model.h5", compile=False)
        class_names = open("labels.txt", "r").readlines()
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # decode output as JSON object
        arg4image = arg1
        image_path = arg4image
        image = Image.open(image_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        query = class_name[2:].strip()
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': '--YOUR-API-KEY-HERE---'})
        if response.status_code == requests.codes.ok:
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
            store = {
                "Calories": calories,
                "Serving size": size,
                "Saturated Fat": satfat,
                "Total Fat": totalfat,
                "Protein": protein,
                "Sodium": sodium,
                "Potassium": potassium,
                "Cholesterol": cholesterol,
                "Total Carbohydrates": carbs,
                "Fiber": fiber,
                "Sugar": sugar
            }
            jstore = json.dumps(store)
            jsresult = {"name": class_name[2:], "nutrition_info": store}
            jsresult["name"] = jsresult["name"].strip()
            cleaned_response = json.dumps(jsresult, ensure_ascii=False, indent=None).encode('utf-8')
            print(jsresult)
        else:
            # If the API encounters an error, log it to the file and display it in app
            print("Error:", response.status_code, response.text)
            cleaned_response = "An error occured. Please try again later."
        # send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(cleaned_response)

if __name__ == '__main__':
    # define server address and port
    server_address = ('', 8080)
    # create HTTP server
    httpd = HTTPServer(server_address, RequestHandler)
    # start HTTP server
    print('Starting server...')
    httpd.serve_forever()
