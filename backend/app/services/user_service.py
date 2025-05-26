from app.models.user import UserProfileRequest, UserProfileResponse
from app.utils.users import get_user_profile, save_user_profile

def update_user_profile(user_id: str, profile_data: UserProfileRequest) -> UserProfileResponse:
    # Save or update profile
    save_user_profile(user_id, profile_data.dict())
    return UserProfileResponse(user_id=user_id, **profile_data.dict())

def fetch_user_profile(user_id: str) -> UserProfileResponse:
    profile = get_user_profile(user_id)
    if not profile:
        raise ValueError("Profile not found.")
    return UserProfileResponse(user_id=user_id, **profile)
