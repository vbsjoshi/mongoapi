from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["euron"]
euron_data = db["euron_coll"]

app = FastAPI()

print(f"MONGO_URI: {MONGO_URI}")

class EuronData(BaseModel):
    name: str
    phone: int
    city: str
    course: str


@app.get("/")
def hello():
    return {"message": "Hello, welcome to mongodbapi!"}


@app.post("/euron/insert")
async def euron_data_insert(data: EuronData):
    result = await euron_data.insert_one(data.dict())
    return {"message": "Data inserted successfully"}


@app.get("/euron/get")
async def get_euron_data():
    items = []
    cursor = euron_data.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        items.append(document)
    return items

@app.get("/euron/showdata")
async def show_data():
    items = []
    cursor = euron_data.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        items.append(document)
    return items



async def update_euron_data(name:str, updated_name:str):
    result = euron_data.update_one(
        {"name": name},
        {"$set": {"name": updated_name}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Euron data not found")
    return {"message": "Euron data updated successfully"}



