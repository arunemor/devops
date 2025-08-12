from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import boto3
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# Load model
MODEL_PATH = "model/garbage_classifier.h5"
model = tf.keras.models.load_model(MODEL_PATH)
class_names = ["newspaper", "aluminium", "glass_bottle", "plastic_bottle"]

# DynamoDB setup
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1',  # Change region
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
materials_table = dynamodb.Table("GarbageMaterials")

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_price_from_dynamodb(material):
    response = materials_table.get_item(Key={"material": material})
    return response["Item"]["price_per_kg"] if "Item" in response else None

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).resize((224, 224))
    image_array = np.expand_dims(np.array(image) / 255.0, axis=0)
    
    predictions = model.predict(image_array)[0]
    confidence = np.max(predictions) * 100
    predicted_class = class_names[np.argmax(predictions)]
    
    if confidence < 80:
        raise HTTPException(status_code=400, detail="Not identified as garbage")
    
    price = get_price_from_dynamodb(predicted_class)
    
    if price is None:
        raise HTTPException(status_code=404, detail="Price not found in DB")
    
    nearest_shops = [
        {"name": "Green Recycle Center", "contact": "+91-9876543210", 
         "location": "https://maps.google.com/?q=28.6139,77.2090"}
    ]
    
    return JSONResponse({
        "material": predicted_class,
        "confidence": round(confidence, 2),
        "price_per_kg": price,
        "nearest_shops": nearest_shops
    })
