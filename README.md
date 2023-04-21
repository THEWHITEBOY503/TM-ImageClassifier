
# TM-ImageClassifier
An adaptation of Google's Teachable Machine library to classify a food item and look up nutrition information. 

This code is an adaptation of the code provided with Google's Teachable Machine library. I'm making this for a school project. Image models are NOT provided in this code repository, you can make your own model for free with [Google's Teachable Machine.](https://teachablemachine.withgoogle.com)
If you don't want to try and gather images of food, you can download my model [from this link](https://drive.google.com/file/d/1LuuLeYXHS3DG7E_eHF2ScPFoI9PedlXp/view?usp=sharing) (Note that this model file is NOT pre-trained, it's just the training data. To convert it to the h5 file the code needs, see the guide below.)

The version on this branch (websv) has two files, an updated classifier script that only outputs JSON, and an HTML server you can make a POST request to and get a response. Simply keep `websv.py` running and both py files in the same directory, then make a POST request. Here's an example output, with a picture of steak passed:
```
% curl -X POST http://localhost:8080 -d '{"arg1": "IMG_2942.jpeg"}'
{"name": "Steak", "nutrition_info": {"Calories": "273.4", "Service size": "100.0g", "Saturated Fat": "7.3g", "Total Fat": "18.8g", "Protein": "26.0g", "Sodium": "52mg", "Potassium": "194mg", "Cholesterol": "95mg", "Total Carbohydrates": "0.0g", "Fiber": "0.0g", "Sugar": "0.0g"}}%
```
One thing I would like to see incorperated with this is a script to where a user can take a picture (of food) with their phone, and it will SFTP it (or upload the file to the remote folder one way or another), and then the name of the uploaded file is passed to the POST request, and the results are fed back. 


## Getting an image model
To get an image model, go to [Google's Teachable Machine.](https://teachablemachine.withgoogle.com) 
If you want to build your own training database, go right ahead! Simply create a new image classifier, and train your model how you want it, then skip to downloading your model.
If you would rather use my example model, first download the `Food training.tm` library from [either this link or the one above (they're the same).](https://drive.google.com/file/d/1LuuLeYXHS3DG7E_eHF2ScPFoI9PedlXp/view?usp=sharing) Then, select "Open an existing project from file".
<img width="1440" alt="Screenshot 2023-04-21 at 12 29 07" src="https://user-images.githubusercontent.com/28698926/233710628-9f619beb-4eb2-484a-aff2-ab9662468313.png">
<img width="1440" alt="Screenshot 2023-04-21 at 13 38 04" src="https://user-images.githubusercontent.com/28698926/233710992-91c34d22-77ca-45db-af1e-e7984d055e5e.png">
Once you import the project file, you'll see the training data. If you'd like to fine tune your training settings, feel free to. But, if you don't know how to, don't touch the settings, simply hit "Train Model". When the training completes, your webcam will most likely get a request to turn on. If you'd like, you can test out your model in your web browser using an image file or your webcam.
When your model is tuned to your liking, you can hit "Export Model".
<img width="823" alt="Screenshot 2023-04-21 at 13 40 06" src="https://user-images.githubusercontent.com/28698926/233712395-6b2fb6ad-dfb2-4deb-97f8-a0281dd32e57.png">

You will be presented with a screen like this, just go to the "Tensorflow" tab, make sure "Keras" is selcted, and hit "Download my model". Then, take the files from the downloaded folder and paste them into the folder with your python scrips. That's it! 

# Installation
To prepare this program for use:

- Clone this branch of the repository with `git clone -b websv --single-branch https://github.com/THEWHITEBOY503/TM-ImageClassifier.git`
- Install the dependancies with `pip install tensorflow keras pillow requests` (You may need to install tensorflow another way)
- Paste your ML model files into the cloned directory
- Start the web server with `python3 websv.py`

That's it!
