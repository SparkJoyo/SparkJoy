# agents/intake.py
from app.services.story_agent.base import Agent
from app.services.story_agent.intake_prompt_v0 import SYSTEM, TEMPLATE

class IntakeAgent(Agent):
    """
    IntakeAgent transforms raw, unstructured parental input into a structured Creative Brief in Markdown format.
    
    Output:
        creative_brief_md (str): A structured creative brief in Markdown, suitable for downstream agents.

    """
    def __init__(self, provider, system_prompt=None, user_template=None):
        super().__init__(
            "Intake",
            system_prompt if system_prompt is not None else SYSTEM,
            user_template if user_template is not None else TEMPLATE,
            provider
        )
