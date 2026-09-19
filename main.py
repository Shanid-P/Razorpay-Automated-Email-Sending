from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    data = await request.json()

    print(data)

    return {"status": "received"}