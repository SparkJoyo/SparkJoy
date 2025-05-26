# Mock user database
USER_DB = {
    "user123": {"birthdate": "2018-06-15", "name": "Emma"},
    "user456": {"birthdate": "2019-09-22", "name": "Liam"},
    "user789": {"birthdate": "2017-01-03", "name": "Sophia"}
}

# Mock profile database
USER_PROFILES = {
    "user123": {
        "name": "Emma",
        "bio": "Emma loves magical forests and monster trucks.",
        "favorite_color": "pink",
        "likes": ["cats", "trucks"],
        "image_keys": ["user123/profile1.jpg"],
        "audio_keys": ["user123/voice1.mp3"],
        "video_keys": []
    }
}

def get_user_by_id(user_id: str):
    return USER_DB.get(user_id)

def save_user_profile(user_id: str, profile_data: dict):
    USER_PROFILES[user_id] = profile_data
    print(f"✅ USER_PROFILES updated: {user_id} → {profile_data}")


def get_user_profile(user_id: str):
    return USER_PROFILES.get(user_id)