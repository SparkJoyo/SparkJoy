from pydantic import BaseModel
from typing import List

class StoryRequest(BaseModel):
    """
    Request model for generating a story.

    Attributes:
        character_keys (List[str]): List of keywords or identifiers representing the main characters in the story.
            Example values: ["brave bear", "curious astronaut", "talking tree", "pirate captain", "robot dog"]
        setting_keys (List[str]): List of keywords or identifiers representing the main settings, locations, or environments where the story takes place.
            Example values: ["enchanted forest", "space station", "underwater city", "mountain village", "pirate ship"]
    """
    character_keys: List[str]
    setting_keys: List[str]

class StoryResponse(BaseModel):
    """
    Response model for a generated story.

    Attributes:
        title (str): The title of the generated story.
        story (str): The full text of the generated story.
        character_keys (List[str]): List of keywords or identifiers representing the main characters in the story.
            Example values: ["brave bear", "curious astronaut", "talking tree", "pirate captain", "robot dog"]
        setting_keys (List[str]): List of keywords or identifiers representing the main settings, locations, or environments where the story takes place.
            Example values: ["enchanted forest", "space station", "underwater city", "mountain village", "pirate ship"]
    """
    title: str
    story: str
    character_keys: List[str]
    setting_keys: List[str]
