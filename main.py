from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

DEBIT_URL = os.getenv("DEBIT_URL")
CARD_URL = os.getenv("CARD_URL")


@app.get("/")
def root():
    return {"message": "API Gateway Running"}


@app.api_route("/api/debit/{path:path}", methods=["GET", "POST", "PATCH"])
async def proxy_debit(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                request.method,
                f"{DEBIT_URL}/{path}",
                content=await request.body(),
                params=request.query_params,
                headers=dict(request.headers)
            )
            return response.json()
        except httpx.RequestError:
            return {"error": "Debit service unavailable"}


@app.api_route("/api/cards/{path:path}", methods=["GET", "POST", "PUT"])
async def proxy_cards(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                request.method,
                f"{CARD_URL}/{path}",
                content=await request.body(),
                params=request.query_params,
                headers=dict(request.headers)
            )
            return response.json()
        except httpx.RequestError:
            return {"error": "Card service unavailable"}