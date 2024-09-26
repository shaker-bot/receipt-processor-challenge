from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import sqlite3
import json
from datetime import datetime

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

    # Rules
    # One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)

    # 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith('.00'):
        points += 50

    # 25 points if the total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += int(float(item.price) * 0.2 + 0.99)

    # 6 points if the day in the purchase date is odd
    if int(receipt.purchaseDate.split('-')[2]) % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points += 10
    
    return {"points": points}
