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

#RESEND_API_KEY = os.getenv("RESEND_API_KEY")

app = FastAPI()

# import resend

# def send_coupon_email(email, coupon):
#     params = {
#         "from": "onboarding@resend.dev",
#         "to": ["pazhayangadi2006@gmail.com"],
#         "subject": "Your Onam Sadhya Coupon",
#         "html": f"""
#             <h2>Onam Sadhya 🎉</h2>
#             <p>Your payment was successful.</p>
#             <p>Your coupon code is:</p>
#             <h3>{coupon}</h3>
#             <p>Thank you for your order!</p>
#         """
#     }

#     return resend.Emails.send(params)

# @app.get("/test-email")
# def test_email():
#     return send_coupon_email(
#         "pazhayangadi2006@gmail.com",
#         "SADHYA-TEST123"
#     )

from dotenv import load_dotenv

load_dotenv()

import os
import requests

MJ_API_KEY = os.getenv("MJ_API_KEY")
MJ_SECRET_KEY = os.getenv("MJ_SECRET_KEY")
MJ_SENDER_EMAIL = os.getenv("MJ_SENDER_EMAIL")


def send_test_email( email, coupon):
    response = requests.post(
        "https://api.mailjet.com/v3.1/send",
        auth=(MJ_API_KEY, MJ_SECRET_KEY),
        json={
            "Messages": [
                {
                    "From": {
                        "Email": MJ_SENDER_EMAIL,
                        "Name": "Onam Sadhya"
                    },
                    "To": [
                        {
                            "Email": email,
                        }
                    ],
                    "Subject": "Your Onam Sadhya Coupon",
                    "HTMLPart": f"""
                         <h2>Onam Sadhya 🎉</h2>
                         <p>Your payment was successful.</p>
                         <p>Your coupon code is:</p>
                         <h3>{coupon}</h3>
                         <p>Thank you for your order!</p>
                     """
                }
            ]
        }
    )
    
    return {
        "status_code": response.status_code,
        "response": response.json()
    }
    
# @app.get("/test-email")
# def test_email():
#     return send_test_email()

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
        
        try:
            send_test_email(email, coupon_id_comp)
            new_order.email_status = "sent"

        except Exception as e:
            print("EMAIL ERROR:", e)
            new_order.email_status = "failed"

        db.commit()
        
        return {"status": "Payment Success"}