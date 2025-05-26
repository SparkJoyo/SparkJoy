from fastapi import Header, HTTPException

def extract_user_id(authorization: str = Header(..., alias="Authorization")) -> str:
    print("🔐 extract_user_id() called")
    print(f"Received Authorization header: {authorization}")
    try:
        token_parts = authorization.split("-")
        user_id = token_parts[1]
        print(f"Parsed user_id: {user_id}")
        return user_id
    except Exception as e:
        print("❌ Failed to parse token:", e)
        raise HTTPException(status_code=401, detail="Invalid token format")