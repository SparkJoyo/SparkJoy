"""
FastAPI routes for CrewAI-based story generation.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import asyncio
import logging

# Import telemetry utilities first to disable telemetry
from ..utils.telemetry import disable_crewai_telemetry, get_telemetry_status

from ..models.story_models import (
    StoryRequest, StoryResponse, CrewExecutionResult, StoryGenerationConfig
)
from ..services.crew_story_generator import CrewStoryGenerator
from ..services.enhanced_crew_generator import EnhancedCrewStoryGenerator
from ..services.specialized_agents import AgentTeamBuilder

# Ensure telemetry is disabled
disable_crewai_telemetry()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/crew-stories", tags=["CrewAI Story Generation"])

# Global instances (in production, use dependency injection)
crew_generator = None
enhanced_generator = None


def get_crew_generator() -> CrewStoryGenerator:
    """Get or create CrewAI story generator instance."""
    global crew_generator
    if crew_generator is None:
        crew_generator = CrewStoryGenerator()
    return crew_generator


def get_enhanced_generator() -> EnhancedCrewStoryGenerator:
    """Get or create enhanced CrewAI story generator instance."""
    global enhanced_generator
    if enhanced_generator is None:
        enhanced_generator = EnhancedCrewStoryGenerator()
    return enhanced_generator


@router.post("/generate", response_model=StoryResponse)
async def generate_story_basic(
    story_request: StoryRequest,
    generator: CrewStoryGenerator = Depends(get_crew_generator)
):
    """
    Generate a story using the basic CrewAI multi-agent system.
    
    This endpoint uses a fixed set of agents in a sequential workflow.
    """
    try:
        logger.info(f"Starting basic story generation for user: {story_request.user_id}")
        
        # Generate story using basic crew
        story_response = await generator.generate_story(story_request)
        
        logger.info(f"Story generation completed successfully")
        return story_response
        
    except Exception as e:
        logger.error(f"Story generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Story generation failed: {str(e)}"
        )


@router.post("/generate-enhanced", response_model=CrewExecutionResult)
async def generate_story_enhanced(
    story_request: StoryRequest,
    config: StoryGenerationConfig = None,
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """
    Generate a story using the enhanced CrewAI system with dynamic agent selection.
    
    This endpoint intelligently selects specialized agents based on story requirements.
    """
    try:
        logger.info(f"Starting enhanced story generation for user: {story_request.user_id}")
        
        # Update generator config if provided
        if config:
            generator.config = config
        
        # Generate story using enhanced crew
        execution_result = await generator.generate_story_enhanced(story_request)
        
        logger.info(f"Enhanced story generation completed. Success: {execution_result.success}")
        return execution_result
        
    except Exception as e:
        logger.error(f"Enhanced story generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Enhanced story generation failed: {str(e)}"
        )


@router.post("/generate-by-theme/{theme}")
async def generate_story_by_theme(
    theme: str,
    story_request: StoryRequest,
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """
    Generate a story with a specific theme using specialized agent teams.
    
    Available themes: adventure, friendship, educational, bedtime, cultural, interactive
    """
    try:
        # Override the theme in the request
        story_request.theme = theme
        
        logger.info(f"Generating {theme} story for user: {story_request.user_id}")
        
        # Use team builder to get specialized agents
        team_builder = AgentTeamBuilder()
        if theme not in ["adventure", "friendship", "educational", "bedtime", "cultural", "interactive"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported theme: {theme}. Available themes: adventure, friendship, educational, bedtime, cultural, interactive"
            )
        
        execution_result = await generator.generate_story_enhanced(story_request)
        
        return execution_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Theme-based story generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Theme-based story generation failed: {str(e)}"
        )


@router.post("/generate-async")
async def generate_story_async(
    story_request: StoryRequest,
    background_tasks: BackgroundTasks,
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """
    Start asynchronous story generation and return immediately with a task ID.
    
    Use the /status/{task_id} endpoint to check progress.
    """
    try:
        # Create a unique task ID
        import uuid
        task_id = str(uuid.uuid4())
        
        # Store task status (in production, use Redis or database)
        task_status = {
            "task_id": task_id,
            "status": "started",
            "story_request": story_request.dict(),
            "result": None,
            "error": None
        }
        
        # Store in global dict (use proper storage in production)
        if not hasattr(generate_story_async, "tasks"):
            generate_story_async.tasks = {}
        generate_story_async.tasks[task_id] = task_status
        
        # Start background task
        background_tasks.add_task(
            _generate_story_background,
            task_id,
            story_request,
            generator
        )
        
        return JSONResponse(
            content={
                "task_id": task_id,
                "status": "started",
                "message": "Story generation started in background"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to start async story generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start async generation: {str(e)}"
        )


async def _generate_story_background(
    task_id: str,
    story_request: StoryRequest,
    generator: EnhancedCrewStoryGenerator
):
    """Background task for story generation."""
    try:
        # Update status
        generate_story_async.tasks[task_id]["status"] = "processing"
        
        # Generate story
        result = await generator.generate_story_enhanced(story_request)
        
        # Update with results
        generate_story_async.tasks[task_id].update({
            "status": "completed",
            "result": result.dict()
        })
        
    except Exception as e:
        # Update with error
        generate_story_async.tasks[task_id].update({
            "status": "failed",
            "error": str(e)
        })


@router.get("/status/{task_id}")
async def get_generation_status(task_id: str):
    """Get the status of an asynchronous story generation task."""
    if not hasattr(generate_story_async, "tasks"):
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_id not in generate_story_async.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_status = generate_story_async.tasks[task_id]
    
    return JSONResponse(content={
        "task_id": task_id,
        "status": task_status["status"],
        "result": task_status.get("result"),
        "error": task_status.get("error")
    })


@router.get("/metrics")
async def get_generation_metrics(
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """Get performance metrics from the story generation system."""
    try:
        metrics = generator.get_performance_metrics()
        return JSONResponse(content=metrics)
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get metrics: {str(e)}"
        )


@router.get("/execution-history")
async def get_execution_history(
    limit: int = 10,
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """Get recent execution history for analysis."""
    try:
        history = generator.get_execution_history()
        
        # Return limited recent history
        recent_history = history[-limit:] if len(history) > limit else history
        
        return JSONResponse(content={
            "total_executions": len(history),
            "recent_executions": [
                {
                    "execution_time": exec.total_execution_time,
                    "success": exec.success,
                    "error_message": exec.error_message,
                    "agent_count": len(exec.agent_results),
                    "story_title": exec.final_result.title if exec.success else None
                }
                for exec in recent_history
            ]
        })
        
    except Exception as e:
        logger.error(f"Failed to get execution history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get execution history: {str(e)}"
        )


@router.post("/config", response_model=Dict[str, Any])
async def update_generation_config(
    config: StoryGenerationConfig,
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """Update the story generation configuration."""
    try:
        # Update the generator config
        generator.config = config
        
        logger.info("Story generation configuration updated")
        
        return JSONResponse(content={
            "message": "Configuration updated successfully",
            "config": config.dict()
        })
        
    except Exception as e:
        logger.error(f"Failed to update config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )


@router.get("/config")
async def get_generation_config(
    generator: EnhancedCrewStoryGenerator = Depends(get_enhanced_generator)
):
    """Get the current story generation configuration."""
    try:
        return JSONResponse(content=generator.config.dict())
        
    except Exception as e:
        logger.error(f"Failed to get config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get configuration: {str(e)}"
        )


@router.get("/available-themes")
async def get_available_themes():
    """Get list of available story themes and their descriptions."""
    themes = {
        "adventure": {
            "name": "Adventure",
            "description": "Exciting stories with journeys, discoveries, and brave characters",
            "suitable_for": ["3-5", "4-6", "6-8"],
            "agents": ["Adventure Story Specialist", "Character Developer", "World Builder", "Interactive Designer"]
        },
        "friendship": {
            "name": "Friendship",
            "description": "Heartwarming stories about friendship, kindness, and social connections",
            "suitable_for": ["3-5", "4-6", "6-8"],
            "agents": ["Friendship Story Specialist", "Character Developer", "Dialogue Specialist", "Emotion Specialist"]
        },
        "educational": {
            "name": "Educational",
            "description": "Learning-focused stories that teach concepts through engaging narratives",
            "suitable_for": ["4-6", "6-8"],
            "agents": ["Educational Story Specialist", "Interactive Designer", "Character Developer"]
        },
        "bedtime": {
            "name": "Bedtime",
            "description": "Calming, peaceful stories perfect for bedtime routines",
            "suitable_for": ["3-5", "4-6"],
            "agents": ["Bedtime Story Specialist", "World Builder", "Emotion Specialist"]
        },
        "cultural": {
            "name": "Cultural",
            "description": "Stories celebrating diversity and different cultures",
            "suitable_for": ["4-6", "6-8"],
            "agents": ["Cultural Story Specialist", "Character Developer", "World Builder", "Dialogue Specialist"]
        },
        "interactive": {
            "name": "Interactive",
            "description": "Stories with participation opportunities and interactive elements",
            "suitable_for": ["3-5", "4-6"],
            "agents": ["Interactive Designer", "Character Developer", "Dialogue Specialist", "Emotion Specialist"]
        }
    }
    
    return JSONResponse(content=themes)


@router.get("/telemetry-status")
async def get_telemetry_status_endpoint():
    """Get the current telemetry configuration status."""
    try:
        status = get_telemetry_status()
        return JSONResponse(content={
            "message": "Telemetry status retrieved successfully",
            "telemetry_status": status,
            "recommendation": "Telemetry is disabled" if status["telemetry_disabled"] else "Consider disabling telemetry for privacy"
        })
        
    except Exception as e:
        logger.error(f"Failed to get telemetry status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get telemetry status: {str(e)}"
        ) 