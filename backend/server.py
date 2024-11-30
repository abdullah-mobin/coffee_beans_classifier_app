import os
import gridfs # type: ignore
import io
from fastapi import FastAPI, File, Form, UploadFile,HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.responses import HTMLResponse,StreamingResponse # type: ignore
from PIL import Image
from dotenv import load_dotenv # type: ignore
from pymongo import MongoClient # type: ignore
from bson import ObjectId  # type: ignore
from datetime import datetime
from helper import details, predict_image

load_dotenv()
admin = os.getenv("ADMIN")
password = os.getenv("PASS")
database=os.getenv("DB")
client = MongoClient(f"mongodb://{admin}:{password}@localhost:27017") 
db = client[f'{database}'] 
fs = gridfs.GridFS(db)  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
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
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        im_details = details(image)
        pred = predict_image(image, model)

        file_id = fs.put(
            image_data,
            filename=file.filename,
            content_type=file.content_type,
            metadata={
                "model": model,
                "predicted_class": pred["predicted_class"],
                "accuracy": pred["accuracy"],
                "width": im_details["width"],
                "height": im_details["height"],
                "mode": im_details["mode"],
                "timestamp": datetime.now()
            }
        )

        return {
            "status": "success",
            "message": "Prediction made and saved to database",
            "file_id": str(file_id), 
            **pred,
            **im_details,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/image/view/{file_id}")
async def get_image(file_id: str):
    try:
        file_object = fs.get(ObjectId(file_id))
        return StreamingResponse(io.BytesIO(file_object.read()), media_type=file_object.content_type)
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_recent_images(limit: int = 100):
    try:
        files = fs.find().sort("uploadDate", -1).limit(limit) 
        images = [
            {"file_id": str(file._id), "filename": file.filename, "uploadDate": file.uploadDate, "metadata":file.metadata}
            for file in files
        ]
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))