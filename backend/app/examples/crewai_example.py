"""
Example usage of the CrewAI Story Generation System

This example demonstrates how to use the multi-agent story generation system
with different configurations and scenarios.
"""

import asyncio
import os
import json
from typing import Dict, Any

# Set up environment variables (in production, use proper config management)
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

from ..models.story_models import (
    StoryRequest, StoryLength, TargetAge, StoryGenerationConfig
)
from ..services.enhanced_crew_generator import EnhancedCrewStoryGenerator
from ..services.specialized_agents import AgentTeamBuilder


async def basic_story_example():
    """Example of basic story generation."""
    print("=== Basic Story Generation Example ===")
    
    # Create a story request
    story_request = StoryRequest(
        text_instructions="Create a story about a brave little rabbit who goes on an adventure",
        target_age=TargetAge.TODDLER,
        story_length=StoryLength.SHORT,
        theme="adventure",
        user_id="example_user_123"
    )
    
    # Create generator
    generator = EnhancedCrewStoryGenerator()
    
    # Generate story
    try:
        result = await generator.generate_story_enhanced(story_request)
        
        if result.success:
            print(f"✅ Story generated successfully!")
            print(f"Title: {result.final_result.title}")
            print(f"Segments: {len(result.final_result.segments)}")
            print(f"Execution time: {result.total_execution_time:.2f} seconds")
            print(f"Agents used: {len(result.agent_results)}")
        else:
            print(f"❌ Story generation failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def image_based_story_example():
    """Example of story generation with image descriptions."""
    print("\n=== Image-Based Story Generation Example ===")
    
    # Create story request with image descriptions
    story_request = StoryRequest(
        image_descriptions=[
            "A child's bedroom with toys scattered around",
            "A magical forest with glowing mushrooms",
            "A friendly dragon sitting by a lake"
        ],
        text_instructions="Use these images to create a bedtime story",
        target_age=TargetAge.PRESCHOOL,
        story_length=StoryLength.MEDIUM,
        theme="bedtime",
        user_id="example_user_456"
    )
    
    # Create generator with custom config
    config = StoryGenerationConfig(
        model_name="gpt-4",
        temperature=0.6,  # Lower temperature for more consistent bedtime stories
        enable_verbose_logging=True,
        process_type="sequential"
    )
    
    generator = EnhancedCrewStoryGenerator(config)
    
    try:
        result = await generator.generate_story_enhanced(story_request)
        
        if result.success:
            print(f"✅ Image-based story generated!")
            print(f"Title: {result.final_result.title}")
            print(f"Summary: {result.final_result.summary}")
            print(f"Characters: {result.final_result.characters}")
            print(f"Themes: {result.final_result.themes}")
        else:
            print(f"❌ Generation failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def educational_story_example():
    """Example of educational story generation."""
    print("\n=== Educational Story Generation Example ===")
    
    story_request = StoryRequest(
        text_instructions="Teach children about counting and numbers through a fun story",
        target_age=TargetAge.EARLY_SCHOOL,
        story_length=StoryLength.MEDIUM,
        theme="educational",
        user_id="example_user_789"
    )
    
    generator = EnhancedCrewStoryGenerator()
    
    try:
        result = await generator.generate_story_enhanced(story_request)
        
        if result.success:
            print(f"✅ Educational story created!")
            
            # Display each segment
            for i, segment in enumerate(result.final_result.segments, 1):
                print(f"\n--- Segment {i} ---")
                print(f"Text: {segment.text}")
                print(f"Visual: {segment.visual_description.scene_description}")
                if segment.interactive_elements:
                    print(f"Interactive: {segment.interactive_elements}")
        else:
            print(f"❌ Generation failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def performance_analysis_example():
    """Example of performance analysis and metrics."""
    print("\n=== Performance Analysis Example ===")
    
    generator = EnhancedCrewStoryGenerator()
    
    # Generate multiple stories to analyze performance
    story_requests = [
        StoryRequest(
            text_instructions=f"Story {i} about friendship",
            target_age=TargetAge.TODDLER,
            story_length=StoryLength.SHORT,
            theme="friendship",
            user_id=f"test_user_{i}"
        )
        for i in range(3)
    ]
    
    print("Generating multiple stories for performance analysis...")
    
    for i, request in enumerate(story_requests, 1):
        print(f"Generating story {i}/3...")
        try:
            result = await generator.generate_story_enhanced(request)
            print(f"  ✅ Story {i} completed in {result.total_execution_time:.2f}s")
        except Exception as e:
            print(f"  ❌ Story {i} failed: {str(e)}")
    
    # Get performance metrics
    metrics = generator.get_performance_metrics()
    print(f"\n📊 Performance Metrics:")
    print(f"Total executions: {metrics.get('total_executions', 0)}")
    print(f"Success rate: {metrics.get('success_rate', 0):.1f}%")
    print(f"Average execution time: {metrics.get('average_execution_time', 0):.2f}s")


async def custom_agent_team_example():
    """Example of using custom agent teams."""
    print("\n=== Custom Agent Team Example ===")
    
    # Use the team builder to create specialized teams
    team_builder = AgentTeamBuilder()
    
    # Test different team types
    themes = ["adventure", "friendship", "educational", "bedtime"]
    
    for theme in themes:
        print(f"\n🎭 Building {theme} team...")
        
        agents = team_builder.build_team(theme)
        agent_roles = [agent.role for agent in agents]
        
        print(f"Team composition for {theme}:")
        for role in agent_roles:
            print(f"  - {role}")
    
    # Example of generating with a specific team
    story_request = StoryRequest(
        text_instructions="A story about a magical adventure",
        target_age=TargetAge.PRESCHOOL,
        story_length=StoryLength.SHORT,
        theme="adventure"
    )
    
    generator = EnhancedCrewStoryGenerator()
    
    try:
        result = await generator.generate_story_enhanced(story_request)
        
        if result.success:
            print(f"\n✅ Adventure story with specialized team completed!")
            print(f"Agents involved: {result.final_result.metadata.get('agents_used', [])}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def configuration_examples():
    """Examples of different configuration options."""
    print("\n=== Configuration Examples ===")
    
    # High creativity config
    creative_config = StoryGenerationConfig(
        model_name="gpt-4",
        temperature=0.9,  # High creativity
        enable_verbose_logging=False,
        process_type="sequential",
        max_retry_attempts=2
    )
    
    # Conservative config for consistent results
    conservative_config = StoryGenerationConfig(
        model_name="gpt-4",
        temperature=0.3,  # Low creativity, more consistent
        enable_verbose_logging=True,
        process_type="sequential",
        max_retry_attempts=3
    )
    
    story_request = StoryRequest(
        text_instructions="A simple story about kindness",
        target_age=TargetAge.TODDLER,
        story_length=StoryLength.SHORT,
        theme="friendship"
    )
    
    print("Testing different configurations...")
    
    # Test creative config
    print("\n🎨 Creative Configuration (High Temperature):")
    creative_generator = EnhancedCrewStoryGenerator(creative_config)
    
    try:
        result = await creative_generator.generate_story_enhanced(story_request)
        if result.success:
            print(f"  ✅ Creative story: '{result.final_result.title}'")
        else:
            print(f"  ❌ Failed: {result.error_message}")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    # Test conservative config
    print("\n📐 Conservative Configuration (Low Temperature):")
    conservative_generator = EnhancedCrewStoryGenerator(conservative_config)
    
    try:
        result = await conservative_generator.generate_story_enhanced(story_request)
        if result.success:
            print(f"  ✅ Conservative story: '{result.final_result.title}'")
        else:
            print(f"  ❌ Failed: {result.error_message}")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")


def print_api_usage_examples():
    """Print examples of how to use the API endpoints."""
    print("\n=== API Usage Examples ===")
    
    # Basic generation
    basic_request = {
        "text_instructions": "Create a story about a brave little mouse",
        "target_age": "3-5",
        "story_length": "short",
        "theme": "adventure",
        "user_id": "user123"
    }
    
    print("📡 Basic Story Generation:")
    print("POST /crew-stories/generate")
    print(f"Body: {json.dumps(basic_request, indent=2)}")
    
    # Enhanced generation
    print("\n📡 Enhanced Story Generation:")
    print("POST /crew-stories/generate-enhanced")
    print(f"Body: {json.dumps(basic_request, indent=2)}")
    
    # Theme-based generation
    print("\n📡 Theme-Based Generation:")
    print("POST /crew-stories/generate-by-theme/bedtime")
    print(f"Body: {json.dumps(basic_request, indent=2)}")
    
    # Async generation
    print("\n📡 Async Generation:")
    print("POST /crew-stories/generate-async")
    print(f"Body: {json.dumps(basic_request, indent=2)}")
    print("Response: {\"task_id\": \"uuid-123\", \"status\": \"started\"}")
    print("Then check: GET /crew-stories/status/uuid-123")
    
    # Get available themes
    print("\n📡 Get Available Themes:")
    print("GET /crew-stories/available-themes")
    
    # Get metrics
    print("\n📡 Get Performance Metrics:")
    print("GET /crew-stories/metrics")


async def main():
    """Run all examples."""
    print("🚀 CrewAI Story Generation System Examples")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        print("⚠️  Please set your OPENAI_API_KEY environment variable before running examples")
        print("   You can set it by: export OPENAI_API_KEY='your-actual-api-key'")
        print("\nShowing API usage examples only:")
        print_api_usage_examples()
        return
    
    # Run examples
    await basic_story_example()
    await image_based_story_example()
    await educational_story_example()
    await performance_analysis_example()
    await custom_agent_team_example()
    await configuration_examples()
    
    print_api_usage_examples()
    
    print("\n🎉 All examples completed!")
    print("\nNext steps:")
    print("1. Set up your OpenAI API key")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the FastAPI server: uvicorn app.main:app --reload")
    print("4. Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    asyncio.run(main()) 