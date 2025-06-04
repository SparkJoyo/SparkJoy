"""
Simple API route for requirements extraction
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.requirements_service import requirements_service

router = APIRouter(prefix="/requirements", tags=["requirements"])

class ExtractRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None

class ExtractResponse(BaseModel):
    ages: List[int]
    length: Optional[str]
    names: List[str]
    characters: List[str]
    educational_behavior: List[str]
    avoid_topics: List[str]
    additional_requirements: List[str]
    extraction_error: Optional[str] = None

@router.post("/extract", response_model=ExtractResponse)
async def extract_requirements(request: ExtractRequest):
    """
    Extract structured requirements from user prompt
    
    Extracts: age, length, names, characters, educational behavior, avoid topics
    Everything else goes to additional_requirements
    """
    try:
        result = requirements_service.extract_requirements(
            request.prompt, 
            request.user_id
        )
        return ExtractResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 