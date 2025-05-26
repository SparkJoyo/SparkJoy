from fastapi import APIRouter, Header, HTTPException
from app.models.story import StoryRequest, StoryResponse
from app.services.story_service import generate_story
from fastapi.security import APIKeyHeader
from app.utils.jwt import extract_user_id

router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


@router.post("/generate", response_model=StoryResponse)
def generate_story_endpoint(
    data: StoryRequest,
    authorization: str = Header(..., alias="Authorization")
):
    user_id = extract_user_id(authorization)
    return generate_story(user_id, data)
