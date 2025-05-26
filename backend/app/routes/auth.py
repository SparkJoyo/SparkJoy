from fastapi import APIRouter, HTTPException
from app.models.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    try:
        return login_user(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
