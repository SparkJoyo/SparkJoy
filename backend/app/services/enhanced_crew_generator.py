"""
Enhanced CrewAI Story Generator with Dynamic Agent Selection

This service intelligently selects and orchestrates specialized agents 
based on the story requirements and user inputs.
"""

# Disable CrewAI telemetry before importing
import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from typing import List, Dict, Any, Optional
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import asyncio
import json
from datetime import datetime

from ..models.story_models import (
    StoryRequest, StoryResponse, StorySegment, VisualDescription,
    CrewExecutionResult, AgentResult, StoryGenerationConfig
)
from .specialized_agents import SpecializedAgentFactory, AgentTeamBuilder


class EnhancedCrewStoryGenerator:
    """
    Enhanced multi-agent story generation system with dynamic agent selection.
    
    This system can:
    1. Analyze story requirements and select appropriate specialized agents
    2. Execute different workflow patterns (sequential, parallel, hierarchical)
    3. Handle complex story generation with multiple specialized roles
    4. Provide detailed execution tracking and results
    """
    
    def __init__(self, config: StoryGenerationConfig = None):
        """Initialize the enhanced crew generator."""
        self.config = config or StoryGenerationConfig()
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent_factory = SpecializedAgentFactory()
        self.team_builder = AgentTeamBuilder()
        self.execution_history: List[CrewExecutionResult] = []
    
    async def generate_story_enhanced(self, story_request: StoryRequest) -> CrewExecutionResult:
        """
        Generate a story using dynamically selected specialized agents.
        
        Args:
            story_request: Story generation request with preferences
            
        Returns:
            CrewExecutionResult: Complete execution result with agent details
        """
        start_time = datetime.now()
        
        try:
            # 1. Analyze story requirements and select agents
            selected_agents = await self._select_agents(story_request)
            
            # 2. Create dynamic tasks based on selected agents
            tasks = await self._create_dynamic_tasks(story_request, selected_agents)
            
            # 3. Create and execute crew
            crew = Crew(
                agents=selected_agents,
                tasks=tasks,
                process=self._get_process_type(),
                verbose=self.config.enable_verbose_logging
            )
            
            # 4. Execute crew with retry logic
            raw_result = await self._execute_with_retry(crew)
            
            # 5. Parse and structure results
            story_response = await self._parse_enhanced_result(raw_result, story_request)
            
            # 6. Create execution result
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = CrewExecutionResult(
                final_result=story_response,
                agent_results=await self._extract_agent_results(crew),
                total_execution_time=execution_time,
                success=True
            )
            
            self.execution_history.append(result)
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            error_result = CrewExecutionResult(
                final_result=self._create_error_story_response(),
                agent_results=[],
                total_execution_time=execution_time,
                success=False,
                error_message=str(e)
            )
            
            self.execution_history.append(error_result)
            return error_result
    
    async def _select_agents(self, story_request: StoryRequest) -> List[Agent]:
        """
        Dynamically select agents based on story requirements.
        
        Args:
            story_request: Story generation request
            
        Returns:
            List[Agent]: Selected specialized agents
        """
        selected_agents = []
        
        # Always include core agents
        selected_agents.extend([
            self.agent_factory.create_character_developer(),
            self.agent_factory.create_world_builder()
        ])
        
        # Add specialized agents based on theme/instructions
        theme = story_request.theme or ""
        instructions = story_request.text_instructions or ""
        combined_text = f"{theme} {instructions}".lower()
        
        # Adventure stories
        if any(word in combined_text for word in ["adventure", "journey", "explore", "quest", "discover"]):
            selected_agents.append(self.agent_factory.create_adventure_story_writer())
        
        # Friendship/social stories
        elif any(word in combined_text for word in ["friend", "friendship", "share", "kind", "help", "together"]):
            selected_agents.append(self.agent_factory.create_friendship_story_writer())
            selected_agents.append(self.agent_factory.create_emotion_specialist())
        
        # Educational stories
        elif any(word in combined_text for word in ["learn", "count", "abc", "color", "number", "teach"]):
            selected_agents.append(self.agent_factory.create_educational_story_writer())
        
        # Bedtime stories
        elif any(word in combined_text for word in ["bedtime", "sleep", "calm", "peaceful", "quiet", "dream"]):
            selected_agents.append(self.agent_factory.create_bedtime_story_writer())
        
        # Cultural stories
        elif any(word in combined_text for word in ["culture", "tradition", "family", "heritage", "celebrate"]):
            selected_agents.append(self.agent_factory.create_cultural_story_writer())
        
        # Default to adventure if no specific theme detected
        else:
            selected_agents.append(self.agent_factory.create_adventure_story_writer())
        
        # Add interactive elements for younger children
        if story_request.target_age.value in ["3-5", "4-6"]:
            selected_agents.append(self.agent_factory.create_interactive_story_designer())
        
        # Add dialogue specialist for longer stories
        if story_request.story_length.value in ["medium", "long"]:
            selected_agents.append(self.agent_factory.create_dialogue_specialist())
        
        return selected_agents
    
    async def _create_dynamic_tasks(self, story_request: StoryRequest, agents: List[Agent]) -> List[Task]:
        """
        Create tasks dynamically based on selected agents.
        
        Args:
            story_request: Story generation request
            agents: Selected agents
            
        Returns:
            List[Task]: Dynamic task list
        """
        tasks = []
        agent_roles = [agent.role for agent in agents]
        
        # 1. Analysis and Planning Task (always first)
        analysis_task = Task(
            description=f"""
            Analyze the story requirements and create a comprehensive plan:
            
            Input Analysis:
            - Images: {story_request.image_descriptions or 'None'}
            - Instructions: {story_request.text_instructions or 'General story'}
            - Theme: {story_request.theme or 'Open theme'}
            - Target Age: {story_request.target_age.value}
            - Length: {story_request.story_length.value}
            
            Create a detailed story plan including:
            1. Core story concept and message
            2. Main characters and their roles
            3. Setting and world details
            4. Story structure and key scenes
            5. Tone and emotional arc
            6. Visual style recommendations
            
            This plan will guide all other agents in creating a cohesive story.
            """,
            agent=agents[0],  # Use first agent for planning
            expected_output="Comprehensive story plan and analysis"
        )
        tasks.append(analysis_task)
        
        # 2. Story Writing Tasks
        story_writers = [agent for agent in agents if "Story" in agent.role and "Specialist" in agent.role]
        if story_writers:
            writing_task = Task(
                description=f"""
                Based on the story plan, write the main story content:
                
                Requirements:
                - Target age: {story_request.target_age.value}
                - Story length: {story_request.story_length.value}
                - Incorporate elements from the analysis
                - Create {self._get_segment_count(story_request.story_length)} story segments
                - Each segment should be 1-2 sentences for young readers
                - Include clear beginning, middle, and end
                - Ensure age-appropriate language and themes
                
                Structure the story for easy page-by-page presentation.
                """,
                agent=story_writers[0],
                expected_output="Complete story text divided into segments",
                context=[analysis_task]
            )
            tasks.append(writing_task)
        
        # 3. Character Development Task
        character_agents = [agent for agent in agents if "Character" in agent.role]
        if character_agents:
            character_task = Task(
                description="""
                Develop rich, memorable characters for the story:
                
                1. Create detailed character profiles
                2. Define personality traits and quirks
                3. Establish character relationships
                4. Plan character growth arcs
                5. Ensure characters are relatable and diverse
                6. Add dialogue that reveals personality
                
                Characters should serve the story while being engaging for children.
                """,
                agent=character_agents[0],
                expected_output="Detailed character profiles and development",
                context=tasks[-1:] if tasks else []
            )
            tasks.append(character_task)
        
        # 4. World Building Task
        world_agents = [agent for agent in agents if "World" in agent.role]
        if world_agents:
            world_task = Task(
                description="""
                Create an immersive story world:
                
                1. Develop detailed setting descriptions
                2. Create sensory details (sights, sounds, smells)
                3. Design world rules and logic
                4. Plan visual elements for each scene
                5. Ensure world consistency throughout story
                6. Make the world feel magical yet believable
                
                The world should enhance the story and spark imagination.
                """,
                agent=world_agents[0],
                expected_output="Complete world description and scene details",
                context=tasks[-2:] if len(tasks) >= 2 else tasks
            )
            tasks.append(world_task)
        
        # 5. Interactive Elements Task
        interactive_agents = [agent for agent in agents if "Interactive" in agent.role]
        if interactive_agents:
            interactive_task = Task(
                description="""
                Design engaging interactive elements:
                
                1. Add questions for audience participation
                2. Include sound effects and actions
                3. Create movement opportunities  
                4. Design call-and-response moments
                5. Plan visual cues for interaction
                6. Ensure age-appropriate interactivity
                
                Interactive elements should enhance engagement without overwhelming the story.
                """,
                agent=interactive_agents[0],
                expected_output="Interactive elements and participation cues",
                context=tasks[-2:] if len(tasks) >= 2 else tasks
            )
            tasks.append(interactive_task)
        
        # 6. Final Assembly and Quality Review Task
        final_task = Task(
            description="""
            Assemble the final story package and conduct quality review:
            
            1. Integrate all story elements seamlessly
            2. Ensure consistency across all segments
            3. Verify age-appropriateness and safety
            4. Check for positive messaging
            5. Optimize pacing and flow
            6. Create final visual descriptions for each segment
            7. Add metadata and story summary
            
            Deliver a complete, polished story ready for presentation.
            """,
            agent=agents[-1],  # Use last agent for final review
            expected_output="Complete polished story with all elements integrated",
            context=tasks  # Include all previous tasks as context
        )
        tasks.append(final_task)
        
        return tasks
    
    def _get_segment_count(self, story_length) -> int:
        """Get target segment count based on story length."""
        length_map = {
            "short": 5,
            "medium": 8,
            "long": 12
        }
        return length_map.get(story_length.value, 8)
    
    def _get_process_type(self) -> Process:
        """Get process type based on configuration."""
        if self.config.process_type == "hierarchical":
            return Process.hierarchical
        return Process.sequential
    
    async def _execute_with_retry(self, crew: Crew) -> str:
        """Execute crew with retry logic."""
        for attempt in range(self.config.max_retry_attempts):
            try:
                result = crew.kickoff()
                return result
            except Exception as e:
                if attempt == self.config.max_retry_attempts - 1:
                    raise e
                await asyncio.sleep(1)  # Brief delay before retry
        
        raise Exception("All retry attempts failed")
    
    async def _parse_enhanced_result(self, raw_result: str, request: StoryRequest) -> StoryResponse:
        """Parse the enhanced crew result into a structured response."""
        
        # Extract story segments (implement sophisticated parsing)
        segments = await self._extract_story_segments_enhanced(raw_result)
        
        # Extract metadata
        title = self._extract_title_enhanced(raw_result)
        summary = self._extract_summary(raw_result)
        themes = self._extract_themes(raw_result)
        characters = self._extract_characters(raw_result)
        
        return StoryResponse(
            title=title,
            segments=segments,
            total_duration=len(segments) * 30,
            generated_at=datetime.now().isoformat(),
            summary=summary,
            themes=themes,
            characters=characters,
            metadata={
                "target_age": request.target_age.value,
                "story_length": request.story_length.value,
                "generated_by": "Enhanced CrewAI Multi-Agent System",
                "generation_approach": "dynamic_agent_selection"
            }
        )
    
    async def _extract_story_segments_enhanced(self, result: str) -> List[StorySegment]:
        """Extract and structure story segments from crew result."""
        # Implement sophisticated parsing logic
        # This is a placeholder - you'd implement actual parsing
        segments = []
        
        # Parse segments from the result
        # Create StorySegment objects with VisualDescription
        
        return segments
    
    def _extract_title_enhanced(self, result: str) -> str:
        """Extract story title using enhanced parsing."""
        # Implement enhanced title extraction
        return "Generated Story"
    
    def _extract_summary(self, result: str) -> str:
        """Extract story summary."""
        # Implement summary extraction
        return "A wonderful children's story."
    
    def _extract_themes(self, result: str) -> List[str]:
        """Extract story themes."""
        # Implement theme extraction
        return []
    
    def _extract_characters(self, result: str) -> List[str]:
        """Extract main characters."""
        # Implement character extraction
        return []
    
    async def _extract_agent_results(self, crew: Crew) -> List[AgentResult]:
        """Extract individual agent results from crew execution."""
        # Implement agent result extraction
        return []
    
    def _create_error_story_response(self) -> StoryResponse:
        """Create a fallback story response in case of errors."""
        return StoryResponse(
            title="Story Generation Error",
            segments=[],
            total_duration=0,
            generated_at=datetime.now().isoformat(),
            metadata={"error": True}
        )
    
    def get_execution_history(self) -> List[CrewExecutionResult]:
        """Get execution history for analysis and debugging."""
        return self.execution_history
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from execution history."""
        if not self.execution_history:
            return {}
        
        successful_runs = [r for r in self.execution_history if r.success]
        avg_execution_time = sum(r.total_execution_time for r in successful_runs) / len(successful_runs) if successful_runs else 0
        
        return {
            "total_executions": len(self.execution_history),
            "successful_executions": len(successful_runs),
            "success_rate": len(successful_runs) / len(self.execution_history) * 100,
            "average_execution_time": avg_execution_time,
            "total_execution_time": sum(r.total_execution_time for r in self.execution_history)
        } 