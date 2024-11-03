import io
from fastapi import FastAPI, File, UploadFile # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from PIL import Image

from helper import details, predict_image

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return{"msg":"This is root route"}


@app.get("/home")
async def home():
    return {"msg": "Hi! I am home"}



@app.post("/predict")
async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    im_details = details(image)

    pred = predict_image(image)

    return {
        "filename":file.filename,
        **pred,
        **im_details
    }