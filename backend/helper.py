import numpy as np
import os
import json

from fastapi import FastAPI # type: ignore
from dotenv import load_dotenv # type: ignore
from PIL import Image
from tensorflow.keras.models import load_model # type: ignore

app = FastAPI()

load_dotenv()

def getUsersModel(model_name):

    if model_name == "coffeenet":
        model_path = os.getenv("COFFEE_MODEL")
        model = load_model(model_path)
        

    elif model_name == "resnet":
        model_path = os.getenv("RESNET_MODEL")
        model = load_model(model_path)

    elif model_name == "xception":
        model_path = os.getenv("XCEPTION_MODEL")
        model = load_model(model_path)

    elif model_name == "vgg":
        model_path = os.getenv("VGG_MODEL")
        model = load_model(model_path)

    else:
        model_path = os.getenv("COFFEE_MODEL")
        model = load_model(model_path)

    return model


def details(image: Image.Image):
    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
    }

def prepare_image(image: Image.Image, target_size=(224, 224)):
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0 
    return np.expand_dims(image_array, axis=0)  

def getClassName(predicted_class_id):
    class_name = ['Espresso roast','French roast','Green / Not roasted','Light roast']
    if predicted_class_id==0:
        predicted_class = class_name[0] 
    elif predicted_class_id==1:
        predicted_class = class_name[1] 
    elif predicted_class_id==2:
        predicted_class = class_name[2] 
    elif predicted_class_id==3:
        predicted_class = class_name[3] 
        
    return predicted_class


def predict_image(image: Image.Image ,model_name):
    model = getUsersModel(model_name)
    prep = prepare_image(image)
    result = model.predict(prep)
    predicted_class_id = np.argmax(result,axis=1)[0]

    predicted_class = getClassName(predicted_class_id)
    model_description = getModelDescription(model_name)
    cf_description=getCoffeeDescription(predicted_class_id)

    acc = float(np.max(result))
    print("class = ",predicted_class)
    print("accuracy = ",acc)
    print("model = ",model_name)
    return {
        "predicted_class":predicted_class,
        "accuracy":acc,
        "coffee_details":cf_description,
        "modedl_details":model_description,
    }   



def getModelDescription(model_name="none"):
    description_path = os.getenv("DESCRIPTION")
    
    with open(os.path.join(description_path, "model.json"), "r") as file:
        data = json.load(file)

    if model_name == "coffeenet":
        description = data.get('coffeenet', 'Description for CoffeeNet not found')
    elif model_name == "resnet":
        description = data.get('resnet', 'Description for ResNet not found')
    elif model_name == "xception":
        description = data.get('xception', 'Description for Xception not found')
    elif model_name == "vgg":
        description = data.get('vgg', 'Description for VGG not found')
    else:
        description = 'Model name not recognized'

    return description

def getCoffeeDescription(class_id):
    description_path = os.getenv("DESCRIPTION")
    
    with open(os.path.join(description_path, "class.json"), "r") as file:
        data = json.load(file)

    if class_id==0:
        description = data.get('espresso', 'Description not found')
    elif class_id==1:
        description = data.get('french', 'Description not found')
    elif class_id==2:
        description = data.get('green', 'Description not found')
    elif class_id==3:
        description = data.get('light', 'Description not found')
    return description