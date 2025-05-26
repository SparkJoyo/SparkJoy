from fastapi import APIRouter, Header, HTTPException
from app.models.user import UserProfileRequest, UserProfileResponse
from app.services.user_service import update_user_profile, fetch_user_profile
from app.utils.jwt import extract_user_id

router = APIRouter()

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(authorization: str = Header(...)):
    user_id = extract_user_id(authorization)
    try:
        return fetch_user_profile(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/profile", response_model=UserProfileResponse)
def update_profile(data: UserProfileRequest, authorization: str = Header(...)):
    user_id = extract_user_id(authorization)
    return update_user_profile(user_id, data)
