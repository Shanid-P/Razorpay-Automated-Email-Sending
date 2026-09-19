from fastapi import FastAPI, Request, Depends, Query, HTTPException

from sqlalchemy import DateTime
from datetime import datetime, timezone

from sqlalchemy.orm import joinedload, Session
from sqlalchemy import func
from database import engine, Base
from database import get_db, SessionLocal

from models import Order

from datetime import datetime, timedelta

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

Base.metadata.create_all(bind=engine)

import random
import string

import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

app = FastAPI()

@app.get("/")
def home():
    return "Welcome to fastAPI"


@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request, db : Session = Depends(get_db)):


    data = await request.json()

    print("DATA:", data)
    
    if(data["event"] == "payment.captured"):
        
        c_data = data["payload"]["payment"]["entity"]
        payment_id = c_data['id']
        order_id = c_data['order_id']
        amount = c_data['amount']
        currency = c_data['currency']
        email = c_data['email']
        contact = c_data['contact']
        status = c_data['status']
        
        orders = db.query(Order)\
            .filter(Order.payment_id == payment_id)\
            .first()
            
        if orders:
            return {"status": "Already processed"}
        
        characters = string.ascii_letters + string.digits
        
        while(True):
            coupon_id =  ''.join(random.choices(characters, k=6))
        
            coupon_existing = db.query(Order)\
                .filter(Order.coupon_id == coupon_id)\
                .first()
                
            if coupon_existing:
                continue
            
            break
        
        coupon_id_comp = 'SADHYA-' + coupon_id
        
        new_order = Order(
            order_id = order_id,
            payment_id = payment_id,
            email = email,
            contact = contact,
            status = status,
            amount = amount,
            coupon_id = coupon_id_comp
        )
        
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        return {"status": "Payment Success"}