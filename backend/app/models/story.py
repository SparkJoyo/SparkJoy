from pydantic import BaseModel, Field
from typing import List, Optional

class StoryRequest(BaseModel):
    """
    Request model for generating a story.

    Attributes:
        image_keys (Optional[List[str]]): List of image keys associated with the story.
        instructions (Optional[str]): Additional text instructions for the story.
        length (Optional[str]): The length of the story. Can be "Short", "Medium", or "Long".
    """
    image_keys: Optional[List[str]] = Field(default_factory=list)
    instructions: Optional[str] = None
    length: Optional[str] = "Medium"  # Short, Medium, Long

class StoryResponse(BaseModel):
    """
    Response model for a generated story.

    Attributes:
        title (str): The title of the generated story.
        story (str): The full text of the generated story.
        image_keys (List[str]): List of image keys used in the story generation.
    """
    title: str
    story: str
    image_keys: List[str] = Field(default_factory=list)
