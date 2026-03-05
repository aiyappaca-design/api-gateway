from jose import jwt
from fastapi import HTTPException, Security, requests
from fastapi.security import HTTPBearer

KEYCLOAK_URL = "http://192.168.0.104:8080/realms//banking-realm"
JWKS_URL = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"

security = HTTPBearer()

jwks = requests.get(JWKS_URL).json()


def verify_token(credentials=Security(security)):

    token = credentials.credentials

    try:
        header = jwt.get_unverified_header(token)

        key = None
        for k in jwks["keys"]:
            if k["kid"] == header["kid"]:
                key = k

        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience="gateway-client"
        )

        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Token validation failed")