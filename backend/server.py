import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from helper import detect_image

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Define a home route
@app.get("/home")
async def home():
    return {"hi": "I am ok"}

@app.get("/")
async def root():
    return{"msg":"This is root route"}


@app.post("/predict")
async def upload_image(file: UploadFile = File(...)):
    # Read the image file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # Call your image detection function
    result = detect_image(image)

    return {"filename": file.filename, **result}