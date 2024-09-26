from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import sqlite3
import json
from datetime import datetime
import uvicorn

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
DATABASE_URL = "sqlite:////data/receipts.db"

@app.get("/")
async def default():
   return {"message": "Hello World"}

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = receipt

    # Save the receipt to the database
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS receipts (
                id TEXT PRIMARY KEY,
                retailer TEXT,
                purchaseDate TEXT,
                purchaseTime TEXT,
                items TEXT,
            """
        )

        items_json = json.dumps([item.model_dump() for item in receipt.items])
        
        cursor.execute(
            """
            INSERT INTO receipts (id, retailer, purchaseDate, purchaseTime, total, items)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (receipt_id, receipt.retailer, receipt.purchaseDate, receipt.purchaseTime, receipt.total, items_json)
        )
        conn.commit()
                       
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
async def get_points(id: str):
    receipt = None

    # Check if the receipt exists in the database
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receipts WHERE id = ?", (id,))
        receipt = cursor.fetchone()

    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    receipt = Receipt(**receipt)

    points = 0

    # Point Rules
    points += sum(c.isalnum() for c in receipt.retailer)

    if receipt.total.endswith('.00'):
        points += 50

    if float(receipt.total) % 0.25 == 0:
        points += 25

    points += (len(receipt.items) // 2) * 5

    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += int(float(item.price) * 0.2 + 0.99)

    if int(receipt.purchaseDate.split('-')[2]) % 2 == 1:
        points += 6

    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points += 10
    
    return {"points": points}

if __name__ == "__main__":
   uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)