from app.models.auth import LoginRequest, LoginResponse
from app.utils.users import get_user_by_id

def login_user(data: LoginRequest) -> LoginResponse:
    user = get_user_by_id(data.user_id)
    if not user or user["birthdate"] != data.birthdate.isoformat():
        raise ValueError("Invalid user ID or birthdate.")

    # For MVP: return a dummy token
    token = f"user-{data.user_id}-token"
    return LoginResponse(token=token, user_id=data.user_id)
