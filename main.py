from fastapi import FastAPI, Request
import httpx

app = FastAPI()

DEBIT_URL = "https://debit-service.onrender.com"
CARD_URL = "https://card-store-8uzi.onrender.com"

@app.api_route("/api/debit/{path:path}", methods=["GET","POST","PATCH"])
async def proxy_debit(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{DEBIT_URL}/{path}",
            content=await request.body()
        )
    return response.json()

@app.api_route("/api/cards/{path:path}", methods=["GET","POST","PUT"])
async def proxy_cards(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{CARD_URL}/{path}",
            content=await request.body()
        )
    return response.json()