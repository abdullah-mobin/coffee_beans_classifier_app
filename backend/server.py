import io
from fastapi import FastAPI, File, Form, UploadFile # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from PIL import Image

from helper import details, predict_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return{"msg":"API root"}


@app.get("/home")
async def home():
    return {"msg": "Welcome"}



@app.post("/predict")
async def predict(file: UploadFile = File(...), model: str = Form(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    im_details = details(image)

    pred = predict_image(image,model)

    return {
        **pred,
        **im_details
    }

