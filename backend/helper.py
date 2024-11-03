import numpy as np
import os

from fastapi import FastAPI # type: ignore
from dotenv import load_dotenv # type: ignore
from PIL import Image
from tensorflow.keras.models import load_model # type: ignore

app = FastAPI()

load_dotenv()
model_path = os.getenv("COFFEE_MODEL")
model = load_model(model_path)


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

def predict_image(image: Image.Image):
    class_name = ['Espresso roast','French roast','Green / Not roasted','Light roast']
    prep = prepare_image(image)
    result = model.predict(prep)
    predicted_class_id = np.argmax(result,axis=1)[0]
    predicted_class = ""
    if predicted_class_id==0:
        predicted_class = class_name[0] 
    elif predicted_class_id==1:
        predicted_class = class_name[1] 
    elif predicted_class_id==2:
        predicted_class = class_name[2] 
    elif predicted_class_id==3:
        predicted_class = class_name[3] 

    acc = float(np.max(result))
    print("class = ",predicted_class)
    print("accuracy = ",acc)
    return {
        "predicted_class":predicted_class,
        "accuracy":acc
    }