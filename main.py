from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return "Welcome to fastAPI"


@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    print("🔥 WEBHOOK RECEIVED")

    data = await request.json()

    print("DATA:", data)

    return {"status": "received"}