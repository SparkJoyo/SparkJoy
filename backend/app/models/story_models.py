"""
Pydantic models for the story generation system.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class StoryLength(str, Enum):
    """Story length options."""
    SHORT = "short"      # 3-5 segments
    MEDIUM = "medium"    # 6-10 segments  
    LONG = "long"        # 11-15 segments


class TargetAge(str, Enum):
    """Target age groups."""
    TODDLER = "3-5"      # Toddlers
    PRESCHOOL = "4-6"    # Preschoolers
    EARLY_SCHOOL = "6-8" # Early school age


class StoryRequest(BaseModel):
    """Request model for story generation."""
    
    # User inputs
    image_descriptions: Optional[List[str]] = Field(
        None, 
        description="Descriptions of uploaded images",
        max_items=5
    )
    text_instructions: Optional[str] = Field(
        None,
        description="User's text instructions for story theme/content",
        max_length=500
    )
    
    # Story preferences
    target_age: TargetAge = Field(
        TargetAge.TODDLER,
        description="Target age group for the story"
    )
    story_length: StoryLength = Field(
        StoryLength.MEDIUM,
        description="Desired story length"
    )
    theme: Optional[str] = Field(
        None,
        description="Optional story theme (adventure, friendship, etc.)",
        max_length=100
    )
    
    # User context
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")


class VisualDescription(BaseModel):
    """Visual description for a story segment."""
    
    scene_description: str = Field(
        ...,
        description="Detailed description of the scene for image generation"
    )
    composition: str = Field(
        ...,
        description="Composition and layout details"
    )
    color_palette: List[str] = Field(
        [],
        description="Suggested color palette for the scene"
    )
    mood: str = Field(
        ...,
        description="Visual mood and atmosphere"
    )
    style_notes: Optional[str] = Field(
        None,
        description="Additional style recommendations"
    )


class StorySegment(BaseModel):
    """Individual segment of a story."""
    
    segment_id: int = Field(..., description="Segment number/ID")
    text: str = Field(..., description="Story text for this segment")
    visual_description: VisualDescription = Field(
        ...,
        description="Visual description for illustration"
    )
    duration_seconds: int = Field(
        30,
        description="Estimated reading/viewing time in seconds"
    )
    
    # Optional enhancements
    sound_effects: Optional[List[str]] = Field(
        None,
        description="Suggested sound effects for this segment"
    )
    interactive_elements: Optional[List[str]] = Field(
        None,
        description="Interactive elements (questions, actions)"
    )
    emotional_tone: Optional[str] = Field(
        None,
        description="Emotional tone of this segment"
    )


class StoryResponse(BaseModel):
    """Complete generated story response."""
    
    # Story content
    title: str = Field(..., description="Story title")
    segments: List[StorySegment] = Field(
        ...,
        description="List of story segments in order"
    )
    
    # Metadata
    total_duration: int = Field(
        ...,
        description="Total estimated story duration in seconds"
    )
    generated_at: Optional[str] = Field(
        None,
        description="Generation timestamp"
    )
    metadata: Dict[str, Any] = Field(
        {},
        description="Additional metadata about the story generation"
    )
    
    # Story summary
    summary: Optional[str] = Field(
        None,
        description="Brief summary of the story"
    )
    themes: Optional[List[str]] = Field(
        None,
        description="Main themes present in the story"
    )
    characters: Optional[List[str]] = Field(
        None,
        description="Main characters in the story"
    )


class AgentResult(BaseModel):
    """Result from an individual agent."""
    
    agent_name: str = Field(..., description="Name of the agent")
    task_description: str = Field(..., description="Description of the task completed")
    result: str = Field(..., description="Agent's output/result")
    execution_time: Optional[float] = Field(None, description="Time taken to complete task")
    metadata: Dict[str, Any] = Field({}, description="Additional metadata")


class CrewExecutionResult(BaseModel):
    """Result from the entire crew execution."""
    
    final_result: StoryResponse = Field(..., description="Final story result")
    agent_results: List[AgentResult] = Field(
        [],
        description="Individual results from each agent"
    )
    total_execution_time: Optional[float] = Field(
        None,
        description="Total time for crew execution"
    )
    success: bool = Field(True, description="Whether execution was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class StoryGenerationConfig(BaseModel):
    """Configuration for story generation."""
    
    # Model settings
    model_name: str = Field("gpt-4", description="LLM model to use")
    temperature: float = Field(0.7, description="Temperature for generation")
    max_tokens: int = Field(2000, description="Maximum tokens per agent response")
    
    # Agent settings
    enable_verbose_logging: bool = Field(True, description="Enable verbose agent logging")
    allow_delegation: bool = Field(False, description="Allow agents to delegate tasks")
    
    # Processing settings
    process_type: str = Field("sequential", description="sequential or hierarchical")
    max_retry_attempts: int = Field(3, description="Max retry attempts on failure")
    
    # Quality settings
    min_story_segments: int = Field(3, description="Minimum number of story segments")
    max_story_segments: int = Field(15, description="Maximum number of story segments")
    require_visual_descriptions: bool = Field(True, description="Require visual descriptions") 