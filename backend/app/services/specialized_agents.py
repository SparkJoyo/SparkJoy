"""
Specialized CrewAI agents for different story generation scenarios.

These agents can be mixed and matched based on the story requirements.
"""

# Disable CrewAI telemetry before importing
import os
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any


class SpecializedAgentFactory:
    """Factory for creating specialized story generation agents."""
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        """Initialize the agent factory with LLM configuration."""
        self.llm_config = llm_config or {
            "model": "gpt-4",
            "temperature": 0.7,
            "api_key": os.getenv("OPENAI_API_KEY")
        }
        self.llm = ChatOpenAI(**self.llm_config)
    
    def create_adventure_story_writer(self) -> Agent:
        """Create an agent specialized in adventure stories."""
        return Agent(
            role="Adventure Story Specialist",
            goal="Create exciting adventure stories that inspire curiosity and courage in children",
            backstory="""You are an expert at crafting thrilling yet age-appropriate adventure stories. 
            You know how to build excitement, create brave characters, and include just enough challenge 
            to keep children engaged without causing fear. Your stories often feature journeys, 
            discoveries, and characters overcoming obstacles through creativity and friendship.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_friendship_story_writer(self) -> Agent:
        """Create an agent specialized in friendship and social stories."""
        return Agent(
            role="Friendship Story Specialist",
            goal="Create heartwarming stories about friendship, kindness, and social connections",
            backstory="""You specialize in stories that teach valuable social lessons through 
            engaging narratives. You understand how to show rather than tell important lessons 
            about sharing, empathy, inclusion, and friendship. Your stories feature diverse 
            characters working together and supporting each other.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_educational_story_writer(self) -> Agent:
        """Create an agent specialized in educational stories."""
        return Agent(
            role="Educational Story Specialist",
            goal="Create engaging stories that seamlessly integrate learning concepts",
            backstory="""You excel at weaving educational content into captivating stories. 
            Whether it's numbers, letters, colors, animals, or science concepts, you make 
            learning feel like play. You understand child development and can present 
            information at the right level while maintaining story engagement.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_bedtime_story_writer(self) -> Agent:
        """Create an agent specialized in calming bedtime stories."""
        return Agent(
            role="Bedtime Story Specialist",
            goal="Create soothing, calming stories perfect for bedtime routines",
            backstory="""You are an expert at crafting gentle, peaceful stories that help 
            children wind down for sleep. You use soft language, gentle rhythms, and 
            calming imagery. Your stories often feature cozy settings, loving characters, 
            and peaceful resolutions that leave children feeling safe and content.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_cultural_story_writer(self) -> Agent:
        """Create an agent specialized in culturally diverse stories."""
        return Agent(
            role="Cultural Story Specialist",
            goal="Create inclusive stories that celebrate diversity and different cultures",
            backstory="""You specialize in creating stories that showcase the beauty of 
            different cultures, traditions, and ways of life. You research and respect 
            cultural authenticity while making stories accessible to all children. 
            Your stories promote understanding, acceptance, and celebration of diversity.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_interactive_story_designer(self) -> Agent:
        """Create an agent specialized in interactive story elements."""
        return Agent(
            role="Interactive Story Designer",
            goal="Design engaging interactive elements that make stories come alive",
            backstory="""You are an expert at creating interactive story experiences. 
            You know how to incorporate sounds, movements, questions, and participation 
            opportunities that engage children actively in the story. You understand 
            child psychology and what interactive elements work best for different ages.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_character_developer(self) -> Agent:
        """Create an agent specialized in character development."""
        return Agent(
            role="Character Development Specialist",
            goal="Create memorable, relatable characters that children connect with emotionally",
            backstory="""You excel at creating characters that feel real and relatable to 
            children. You understand how to give characters distinct personalities, quirks, 
            and growth arcs that resonate with young audiences. Your characters are diverse, 
            inclusive, and serve as positive role models.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_dialogue_specialist(self) -> Agent:
        """Create an agent specialized in natural, engaging dialogue."""
        return Agent(
            role="Dialogue Specialist",
            goal="Create natural, engaging dialogue that brings characters to life",
            backstory="""You are skilled at writing dialogue that sounds natural and 
            age-appropriate for children. You understand how different characters would 
            speak and can create conversations that advance the plot while revealing 
            character personalities. Your dialogue is engaging and easy to read aloud.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_world_builder(self) -> Agent:
        """Create an agent specialized in building story worlds and settings."""
        return Agent(
            role="World Building Specialist",
            goal="Create vivid, imaginative settings that transport children to new worlds",
            backstory="""You excel at creating immersive story worlds that spark children's 
            imagination. Whether it's a magical forest, underwater kingdom, or neighborhood 
            playground, you make settings feel real and exciting. You pay attention to 
            sensory details that help children visualize and feel part of the story world.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )
    
    def create_emotion_specialist(self) -> Agent:
        """Create an agent specialized in emotional intelligence and development."""
        return Agent(
            role="Emotional Intelligence Specialist",
            goal="Integrate emotional learning and development into stories naturally",
            backstory="""You specialize in helping children understand and process emotions 
            through storytelling. You know how to address feelings like frustration, joy, 
            sadness, and excitement in age-appropriate ways. Your stories help children 
            develop emotional vocabulary and coping strategies.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            tools=[]
        )


class AgentTeamBuilder:
    """Builder class for creating specialized agent teams based on story requirements."""
    
    def __init__(self):
        self.factory = SpecializedAgentFactory()
        self.teams = {
            "adventure": self._build_adventure_team,
            "friendship": self._build_friendship_team,
            "educational": self._build_educational_team,
            "bedtime": self._build_bedtime_team,
            "cultural": self._build_cultural_team,
            "interactive": self._build_interactive_team
        }
    
    def build_team(self, story_type: str, custom_agents: list = None) -> list:
        """Build a team of agents for a specific story type."""
        if story_type in self.teams:
            base_team = self.teams[story_type]()
        else:
            base_team = self._build_default_team()
        
        if custom_agents:
            base_team.extend(custom_agents)
        
        return base_team
    
    def _build_adventure_team(self) -> list:
        """Build team for adventure stories."""
        return [
            self.factory.create_adventure_story_writer(),
            self.factory.create_character_developer(),
            self.factory.create_world_builder(),
            self.factory.create_interactive_story_designer()
        ]
    
    def _build_friendship_team(self) -> list:
        """Build team for friendship stories."""
        return [
            self.factory.create_friendship_story_writer(),
            self.factory.create_character_developer(),
            self.factory.create_dialogue_specialist(),
            self.factory.create_emotion_specialist()
        ]
    
    def _build_educational_team(self) -> list:
        """Build team for educational stories."""
        return [
            self.factory.create_educational_story_writer(),
            self.factory.create_interactive_story_designer(),
            self.factory.create_character_developer()
        ]
    
    def _build_bedtime_team(self) -> list:
        """Build team for bedtime stories."""
        return [
            self.factory.create_bedtime_story_writer(),
            self.factory.create_world_builder(),
            self.factory.create_emotion_specialist()
        ]
    
    def _build_cultural_team(self) -> list:
        """Build team for cultural stories."""
        return [
            self.factory.create_cultural_story_writer(),
            self.factory.create_character_developer(),
            self.factory.create_world_builder(),
            self.factory.create_dialogue_specialist()
        ]
    
    def _build_interactive_team(self) -> list:
        """Build team for interactive stories."""
        return [
            self.factory.create_interactive_story_designer(),
            self.factory.create_character_developer(),
            self.factory.create_dialogue_specialist(),
            self.factory.create_emotion_specialist()
        ]
    
    def _build_default_team(self) -> list:
        """Build default balanced team."""
        return [
            self.factory.create_adventure_story_writer(),
            self.factory.create_character_developer(),
            self.factory.create_world_builder()
        ] 