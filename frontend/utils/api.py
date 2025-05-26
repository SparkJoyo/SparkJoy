import requests
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE = os.getenv("API_BASE")

def login(user_id: str, birthdate: str) -> Optional[str]:
    try:
        res = requests.post(f"{API_BASE}/login", json={
            "user_id": user_id,
            "birthdate": birthdate
        })
        if res.status_code == 200:
            return res.json().get("token")
    except Exception as e:
        print(f"Login error: {e}")
    return None

def upload_file(token: str, file) -> str:
    try:
        files = {"file": (file.name, file, file.type)}
        res = requests.post(f"{API_BASE}/upload", headers={"Authorization": token}, files=files)
        if res.status_code == 200:
            return res.json().get("s3_key")
    except Exception as e:
        print(f"Upload error: {e}")
    return None

def get_profile(token: str):
    try:
        res = requests.get(f"{API_BASE}/profile", headers={"Authorization": token})
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Get profile error: {e}")
    return None

def update_profile(token: str, data: dict):
    try:
        res = requests.post(f"{API_BASE}/profile", headers={"Authorization": token}, json=data)
        return res.status_code == 200
    except Exception as e:
        print(f"Update profile error: {e}")
    return False

def generate_story(token: str, data: dict):
    try:
        res = requests.post(f"{API_BASE}/generate", headers={"Authorization": token}, json=data)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Generate story error: {e}")
    return None
