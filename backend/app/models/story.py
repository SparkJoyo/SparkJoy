from pydantic import BaseModel
from typing import List

class StoryRequest(BaseModel):
    character_keys: List[str]
    setting_keys: List[str]

class StoryResponse(BaseModel):
    title: str
    story: str
    character_keys: List[str]
    setting_keys: List[str]
