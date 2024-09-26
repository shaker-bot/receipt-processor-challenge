from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

receipts = {}

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = receipt
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in receipts:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # Here you would implement the logic to calculate points
    # For now, we'll return a dummy value
    return {"points": 100}
