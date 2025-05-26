from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: str
    birthdate: str  # YYYY-MM-DD format

class LoginResponse(BaseModel):
    token: str
    user_id: str
