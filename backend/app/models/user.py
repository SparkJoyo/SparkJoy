from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfileRequest(BaseModel):
    """
    Request model for updating or creating a user profile.
    """
    name: Optional[str] = None
    bio: Optional[str] = None                      # Paragraph text
    favorite_color: Optional[str] = None
    likes: Optional[List[str]] = Field(default_factory=list)
    
    image_keys: Optional[List[str]] = Field(default_factory=list)           # S3 object keys for images
    audio_keys: Optional[List[str]] = Field(default_factory=list)           # S3 object keys for audio clips
    video_keys: Optional[List[str]] = Field(default_factory=list)           # S3 object keys for video clips

class UserProfileResponse(UserProfileRequest):
    """
    Response model for a user profile, including the user ID.
    """
    user_id: str
