import os
import boto3
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
from utils import is_garbage, get_garbage_price

# Force CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY",
    aws_secret_access_key="YOUR_AWS_SECRET_KEY"
)
table = dynamodb.Table("GarbageRecords")

# Load model
model = tf.keras.models.load_model("model/garbage_model.h5")
labels = ["newspaper", "aluminium", "glass_bottle", "plastic_bottle"]

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    img = Image.open(file.file).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    confidence = float(np.max(predictions))
    label = labels[np.argmax(predictions)]

    if not is_garbage(label, confidence):
        return {"status": "error", "message": "Not garbage"}

    price = get_garbage_price(label)

    # Save record to DynamoDB
    table.put_item(Item={
        "id": str(uuid.uuid4()),
        "material": label,
        "confidence": confidence,
        "price": price
    })

    return {
        "status": "success",
        "material": label,
        "confidence": f"{confidence*100:.2f}%",
        "price": price,
        "map_image_url": "/static/garbage_map.png"
    }
