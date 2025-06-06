# agents/intake.py
from app.services.story_agent.base import Agent

SYSTEM = """
You are a highly creative AI assistant specializing in generating distinct,
imaginative, and engaging story concepts for children's picture books.
Transform a 'Creative Brief' into multiple distinct, imaginative, and 
engaging story concepts formatted in structured Markdown. Ensure all 
concepts are creative, align strictly with the brief's details, and 
follow the requested output format precisely.
"""

TEMPLATE = """
You are a Creative Idea Generator for children's picture books.
Based on the following 'Creative Brief' (provided in Markdown):
Generate 3 distinct, imaginative, and engaging story concepts. Format your output as a single Markdown document.
Each concept should start with a Level 3 Markdown heading (e.g., ### Concept 1).
Under each concept heading, provide the following details using bolded labels and then the information:
- **Title:** [Potential title]
- **Plot Summary:** [2-3 sentence plot idea]
- **Key Characters:** [List main character ideas as bullet points]

Example for one concept:
### Concept 1: The Magical Crayon
- **Title:** Lily and the Magical Crayon
- **Plot Summary:** Lily finds a sparkling crayon. She draws a friendly dragon, which pops off the page! Together they explore, drawing solutions to small challenges they encounter.
- **Key Characters:**
    - Lily (as described in brief)
    - Sparky the Drawn Dragon

Ensure concepts align with the child's age, interests, and desired themes from the brief.
Output ONLY the Markdown content for the 3 concepts. Do not include any preamble.

--- Creative Brief ---
{creative_brief_md}
--- End Creative Brief ---

LET'S BRAINSTROM!
"""

class CreativeAgent(Agent):
    """
    CreativeAgent generates multiple creative story concepts for children's picture books based on a structured Creative Brief.
    
    Input (for __call__):
        creative_brief_md (str): The structured creative brief in Markdown, typically produced by IntakeAgent.
        (Pass as 'creative_brief_md' kwarg.)
    
    Output:
        concepts_md (str): Markdown-formatted list of creative story concepts.
    """
    def __init__(self, provider, system_prompt=None, user_template=None):
        super().__init__(
            "Creative",
            system_prompt if system_prompt is not None else SYSTEM,
            user_template if user_template is not None else TEMPLATE,
            provider
        )
