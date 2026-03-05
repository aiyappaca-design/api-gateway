from fastapi import FastAPI, Request, Depends, HTTPException
import httpx
import os
from auth import verify_token

app = FastAPI()

DEBIT_URL = os.getenv("DEBIT_URL")
CARD_URL = os.getenv("CARD_URL")


# @app.post("/login")
# def login():
#     token = create_access_token({"sub": "admin"})
#     return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"message": "API Gateway Running"}


# 🔐 Proxy Debit Service (JWT Protected)
@app.api_route("/api/debit/{path:path}", methods=["GET", "POST", "PATCH"])
async def proxy_debit(
    path: str,
    request: Request,
    user: dict = Depends(verify_token)   # ✅ Validate JWT at Gateway
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Authorization": request.headers.get("Authorization")
            }

            response = await client.request(
                method=request.method,
                url=f"{DEBIT_URL}/{path}",
                content=await request.body(),
                params=request.query_params,
                headers=headers,   # ✅ Propagate Token
            )

            return response.json()

        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Debit service unavailable")


# 🔐 Proxy Card Service (JWT Protected)
@app.api_route("/api/cards/{path:path}", methods=["GET", "POST", "PUT"])
async def proxy_cards(
    path: str,
    request: Request,
    user: dict = Depends(verify_token)   # ✅ Validate JWT at Gateway
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Authorization": request.headers.get("Authorization")
            }

            response = await client.request(
                method=request.method,
                url=f"{CARD_URL}/{path}",
                content=await request.body(),
                params=request.query_params,
                headers=headers,   # ✅ Propagate Token
            )

            return response.json()

        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Card service unavailable")