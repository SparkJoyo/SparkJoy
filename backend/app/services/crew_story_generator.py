"""
CrewAI Multi-Agent Story Generation Service

This service uses multiple AI agents to collaboratively generate personalized stories.
Each agent has a specific role in the story creation process.
"""

# Disable CrewAI telemetry before importing
import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from typing import List, Dict, Any, Optional
from crewai import Agent, Task, Crew, Process
from crewai.agent import Agent
from crewai.task import Task
from langchain_openai import ChatOpenAI
from ..models.story_models import StoryRequest, StoryResponse, StorySegment


class CrewStoryGenerator:
    """
    Multi-agent story generation system using CrewAI framework.
    
    Agents:
    1. Story Analyst - Analyzes images and user inputs
    2. Story Writer - Creates the main story content
    3. Story Enhancer - Adds emotional depth and engagement
    4. Visual Coordinator - Plans visual elements for each segment
    5. Quality Reviewer - Reviews and refines the final story
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all the agents with their specific roles and capabilities."""
        
        # Agent 1: Story Analyst
        self.story_analyst = Agent(
            role="Story Analyst",
            goal="Analyze uploaded images and user inputs to extract key elements for story creation",
            backstory="""You are an expert at understanding visual content and user preferences. 
            You excel at identifying themes, characters, settings, and emotions from images and text inputs.
            Your analysis forms the foundation for compelling stories.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 2: Story Writer
        self.story_writer = Agent(
            role="Children's Story Writer",
            goal="Create engaging, age-appropriate stories for children aged 3-5",
            backstory="""You are a talented children's author with years of experience writing 
            bedtime stories. You know how to craft simple yet captivating narratives that 
            engage young minds while being educational and fun. You excel at creating stories 
            with clear structure, simple language, and positive messages.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 3: Story Enhancer
        self.story_enhancer = Agent(
            role="Story Enhancement Specialist",
            goal="Add emotional depth, sensory details, and interactive elements to stories",
            backstory="""You specialize in making stories more immersive and emotionally 
            resonant. You add rich sensory descriptions, emotional beats, and interactive 
            elements that make stories come alive for children. You ensure stories have 
            proper pacing and emotional arcs.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 4: Visual Coordinator
        self.visual_coordinator = Agent(
            role="Visual Story Coordinator",
            goal="Plan visual elements and scene descriptions for each story segment",
            backstory="""You are an expert at visualizing stories and planning how they 
            should look when illustrated. You understand composition, color psychology, 
            and how visuals can enhance storytelling for children. You create detailed 
            visual descriptions for each story segment.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Agent 5: Quality Reviewer
        self.quality_reviewer = Agent(
            role="Story Quality Reviewer",
            goal="Review and refine stories to ensure they meet quality standards",
            backstory="""You are a meticulous editor and child development expert who 
            ensures stories are appropriate, engaging, and well-structured. You check 
            for consistency, age-appropriateness, positive messaging, and overall quality. 
            You make final refinements to perfect the story.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_tasks(self, story_request: StoryRequest) -> List[Task]:
        """Create tasks for each agent based on the story request."""
        
        # Task 1: Analyze inputs
        analysis_task = Task(
            description=f"""
            Analyze the following inputs for story creation:
            - Images: {story_request.image_descriptions if story_request.image_descriptions else 'None provided'}
            - User instructions: {story_request.text_instructions if story_request.text_instructions else 'None provided'}
            - Target age: {story_request.target_age}
            - Story length: {story_request.story_length}
            
            Extract and identify:
            1. Main characters or subjects
            2. Setting and environment
            3. Mood and tone
            4. Key themes or messages
            5. Visual elements to incorporate
            6. Story direction suggestions
            
            Provide a comprehensive analysis that will guide the story creation process.
            """,
            agent=self.story_analyst,
            expected_output="A detailed analysis document with identified story elements"
        )
        
        # Task 2: Write initial story
        writing_task = Task(
            description=f"""
            Based on the analyst's findings, create an engaging children's story with:
            - Target age: {story_request.target_age}
            - Length: {story_request.story_length}
            - Clear beginning, middle, and end
            - Age-appropriate language and themes
            - Positive message or lesson
            - Incorporates elements from the analysis
            
            Structure the story in segments suitable for page-by-page presentation.
            Each segment should be 1-2 sentences for easy reading.
            """,
            agent=self.story_writer,
            expected_output="A structured story divided into segments",
            context=[analysis_task]
        )
        
        # Task 3: Enhance the story
        enhancement_task = Task(
            description="""
            Enhance the story by adding:
            1. Sensory details (sounds, textures, smells)
            2. Emotional depth and character development
            3. Interactive elements (questions, sounds to make)
            4. Rhythmic language and repetition where appropriate
            5. Ensure smooth flow between segments
            
            Maintain the original structure but make it more engaging and immersive.
            """,
            agent=self.story_enhancer,
            expected_output="An enhanced version of the story with richer details",
            context=[writing_task]
        )
        
        # Task 4: Plan visual elements
        visual_task = Task(
            description="""
            For each story segment, create detailed visual descriptions including:
            1. Scene composition and layout
            2. Character positions and expressions
            3. Background elements and setting details
            4. Color palette suggestions
            5. Visual style recommendations
            6. How to incorporate user-uploaded images
            
            Ensure visual continuity across segments while maintaining visual interest.
            """,
            agent=self.visual_coordinator,
            expected_output="Visual descriptions for each story segment",
            context=[enhancement_task]
        )
        
        # Task 5: Final review and refinement
        review_task = Task(
            description="""
            Conduct a final review of the complete story package:
            1. Check age-appropriateness and safety
            2. Ensure consistency across segments
            3. Verify positive messaging
            4. Check language complexity
            5. Ensure visual descriptions align with story
            6. Make final refinements
            
            Provide the final, polished story ready for presentation.
            """,
            agent=self.quality_reviewer,
            expected_output="Final polished story with all elements refined",
            context=[visual_task]
        )
        
        return [analysis_task, writing_task, enhancement_task, visual_task, review_task]
    
    async def generate_story(self, story_request: StoryRequest) -> StoryResponse:
        """
        Generate a complete story using the multi-agent crew.
        
        Args:
            story_request: Request containing images, instructions, and preferences
            
        Returns:
            StoryResponse: Complete story with segments and visual descriptions
        """
        
        # Create tasks
        tasks = self._create_tasks(story_request)
        
        # Create crew
        crew = Crew(
            agents=[
                self.story_analyst,
                self.story_writer, 
                self.story_enhancer,
                self.visual_coordinator,
                self.quality_reviewer
            ],
            tasks=tasks,
            process=Process.sequential,  # Tasks run in sequence
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Parse the result and create story response
        return self._parse_crew_result(result, story_request)
    
    def _parse_crew_result(self, result: str, request: StoryRequest) -> StoryResponse:
        """Parse the crew result into a structured StoryResponse."""
        
        # This is a simplified parser - you'd implement more sophisticated parsing
        segments = self._extract_story_segments(result)
        
        return StoryResponse(
            title=self._extract_title(result),
            segments=segments,
            total_duration=len(segments) * 30,  # Estimate 30 seconds per segment
            metadata={
                "target_age": request.target_age,
                "generated_by": "CrewAI Multi-Agent System",
                "agents_used": ["analyst", "writer", "enhancer", "visual_coordinator", "reviewer"]
            }
        )
    
    def _extract_story_segments(self, result: str) -> List[StorySegment]:
        """Extract story segments from the crew result."""
        # Implement parsing logic based on the crew's output format
        # This is a placeholder implementation
        
        segments = []
        # Parse the result and create StorySegment objects
        # You'd implement actual parsing logic here
        
        return segments
    
    def _extract_title(self, result: str) -> str:
        """Extract the story title from the crew result."""
        # Implement title extraction logic
        return "Generated Story" 