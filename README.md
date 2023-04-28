
# Java-and-py Branch
This branch is under construction. If you can write this program faster than me, please do! (This project is due in like, a week)
This branch includes the AI image classification server (classifier folder), and the Java app (src/main/java/com/example) that takes a screenshot, SFTP's it over to the classifier server, classifies it, then deletes the file. 

## To-Do (Java front-end)
- [ ] ~~actually learn java~~
- [ ] Make it to where the Java app uses a camera or webcam to take a picture instead of using a screenshot.
- [ ] Port to mobile(?)
- [ ] ~~find a better hobby~~
	- I, personally, think riding motorcycles is a better use of my time than writing horrible code in a language I hate. 


# TM-ImageClassifier
An adaptation of Google's Teachable Machine library to classify a food item and look up nutrition information. 

This code is an adaptation of the code provided with Google's Teachable Machine library. I'm making this for a school project. Image models are NOT provided in this code repository, you can make your own model for free with [Google's Teachable Machine.](https://teachablemachine.withgoogle.com)
If you don't want to try and gather images of food, you can download my model [from this link](https://drive.google.com/file/d/1LuuLeYXHS3DG7E_eHF2ScPFoI9PedlXp/view?usp=sharing) (Note that this model file is NOT pre-trained, it's just the training data. To convert it to the h5 file the code needs, see the guide below.)

The version on this branch (websv) has two files, an updated classifier script that only outputs JSON, and an HTML server you can make a POST request to and get a response. Simply keep `websv.py` running and both py files in the same directory, then make a POST request. Here's an example output, with a picture of steak passed:
```
% curl -X POST http://localhost:8080 -d '{"arg1": "IMG_2942.jpeg"}'
{"name": "Steak", "nutrition_info": {"Calories": "273.4", "Service size": "100.0g", "Saturated Fat": "7.3g", "Total Fat": "18.8g", "Protein": "26.0g", "Sodium": "52mg", "Potassium": "194mg", "Cholesterol": "95mg", "Total Carbohydrates": "0.0g", "Fiber": "0.0g", "Sugar": "0.0g"}}%
```
One thing I would like to see incorporated with this is a script to where a user can take a picture (of food) with their phone, and it will SFTP it (or upload the file to the remote folder one way or another), and then the name of the uploaded file is passed to the POST request, and the results are fed back. 

## What is the end goal?
My end goal with this program is to make a nutrition logging app where you can take a picture of a food item and have it automatically log the food and nutrition information. I was gonna incorperate GPT into it, so you could log your symptoms and have GPT try and find a correlation between them. But, this image classifier part is hard enough, and this project ends in like a week or two, and I graduate in like a month, so I'm not going to bother. 

## Preparing the model
### Getting an image model
To get an image model, go to [Google's Teachable Machine.](https://teachablemachine.withgoogle.com) 
If you want to build your own training database, go right ahead! Simply create a new image classifier, and train your model how you want it, then skip to downloading your model.
If you would rather use my example model, first download the `Food training.tm` library from [either this link or the one above (they're the same).](https://drive.google.com/file/d/1LuuLeYXHS3DG7E_eHF2ScPFoI9PedlXp/view?usp=sharing) Then, select "Open an existing project from file".

<img width="1440" alt="Screenshot 2023-04-21 at 12 29 07" src="https://user-images.githubusercontent.com/28698926/233710628-9f619beb-4eb2-484a-aff2-ab9662468313.png">

### Training your image model
<img width="1440" alt="The project screen of Google Teachable Machine" src="https://user-images.githubusercontent.com/28698926/233710992-91c34d22-77ca-45db-af1e-e7984d055e5e.png">
Once you import the project file, you'll see the training data. If you'd like to fine tune your training settings, feel free to. But, if you don't know how to, don't touch the settings, simply hit "Train Model". When the training completes, your webcam will most likely get a request to turn on. If you'd like, you can test out your model in your web browser using an image file or your webcam.

### Exporting your model
When your model is tuned to your liking, you can hit "Export Model".

<img width="2125" alt="Screenshot 2023-04-21 at 19 47 21" src="https://user-images.githubusercontent.com/28698926/233752919-d1469f65-2871-4bfc-92b6-a3e3a4b0dd8a.png">

<img width="823" alt="Screenshot 2023-04-21 at 13 40 06" src="https://user-images.githubusercontent.com/28698926/233753121-2054ff82-717e-4c38-857d-375f24c50ddf.png">

You will be presented with a screen like this, just go to the "Tensorflow" tab, make sure "Keras" is selected, and hit "Download my model". Then, take the files from the downloaded folder and paste them into the folder with your python scripts. That's it! 

## Installation
To prepare this program for use:

- Clone this branch of the repository with `git clone -b websv --single-branch https://github.com/THEWHITEBOY503/TM-ImageClassifier.git`
- Install the dependancies with `pip install tensorflow keras pillow requests` (You may need to install tensorflow another way)
- Paste your ML model files into the cloned directory
- Paste your image files into the directory
- Set up your API key
	- This project utilizes API-Ninja's nutrition API. [You can read more about the API and sign up to get a key here.](https://api-ninjas.com/api/nutrition) Once you have your key, simply find and replace `--YOUR-API-KEY-HERE--` with your API key.
- Start the web server with `python3 websv.py`

That's it!

## Usage
Right now, there's no way to upload an image to the web server using a POST request. So, for the time being, you will need to have the image you want to process in the same directory as the scripts. 
Let's say I have this picture stored on my server in the same directory as my scripts under the file name `IMG_6216.jpeg`:

![IMG_6216](https://user-images.githubusercontent.com/28698926/233751930-d15b5a41-2ece-42a4-a656-f94d8cda510b.jpeg)
(mmm, yummy...)

In order to process this, I have to send the server this data with my POST request: 
`{"arg1": "IMG_2819.jpeg"}`

So, if I was going to make a cURL request to process this photo, I'd run `curl -X POST http://localhost:8080 -d '{"arg1": "IMG_2819.jpeg"}'`

![ezgif com-optimize-2](https://user-images.githubusercontent.com/28698926/233752410-95c8e571-ed3b-40e9-9f18-b9711a1e23f2.gif)
(Note-- in this example the server (right side) is being run on a Ubuntu VM running inside my MacBook Pro on Parallels, while the left side is just the terminal from macOS)

## To-do (Python classifier back-end)
- [x] (Done!) Merge web server and classification script into one .py file
- [x] ~~Make function to upload image directly to classifier~~ -- Technically, this task belongs to the Java front-end. Nonetheless, I did it. 
	- ~~Perferrably this would be done with the same POST request, but otherwise just make it SFTP it or something to the server then run the POST request~~
	- I ended up just making an SFTP upload for the Java front-end, because I can't for the life of me figure out how to upload an image with POST. My best bet would be to encode the image in base64, send it to the server, and have the server decode the base64. That's what ChatGPT suggested, anyways. 
