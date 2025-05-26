from pydantic import BaseModel
from typing import List, Optional

class UserProfileRequest(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None                      # Paragraph text
    favorite_color: Optional[str] = None
    likes: Optional[List[str]] = []
    
    image_keys: Optional[List[str]] = []           # S3 object keys for images
    audio_keys: Optional[List[str]] = []           # S3 object keys for audio clips
    video_keys: Optional[List[str]] = []           # S3 object keys for video clips

class UserProfileResponse(UserProfileRequest):
    user_id: str
