# agents/intake.py
from app.services.story_agent.base import Agent

SYSTEM = """
Your role is to meticulously transform raw parental input for a children's picture 
book into a structured Markdown 'Creative Brief'. Follow the provided template exactly. 
For any information not found in the input, state 'Not specified by parent'. 
Fabricate nothing. Output only the completed brief.
"""

TEMPLATE = """
Analyze the provided `{input}` to produce a structured 'Creative Brief' in Markdown.
Your output MUST strictly follow the format and sections detailed below.

Key Instructions:
* Extract information from `{input}` for every field in the template.
* For each field, if the corresponding information is not found in the input, you MUST explicitly state 'Not specified by parent'.
* Do NOT invent or infer any information.
* Your final output MUST be ONLY the 'Creative Brief' Markdown document, matching the structure shown.

Parental Input:
-------------------------------
{input}
-------------------------------

**Creative Brief for Picture Book Project**

**1. Child's Profile:**
    * **Child's Name (for reference/use in story):** [Extracted name(s) or 'Not specified by parent']
    * **Child's Age:** [Extracted age or 'Not specified by parent']
    * **Key Interests & Passions:** [List extracted interests (e.g., dinosaurs, space, art) OR 'Not specified by parent']
    * **Favorite Books/Characters:** [List extracted favorites OR 'Not specified by parent']
    * **Child's Personality Insights:** [List extracted insights (e.g., adventurous, shy) OR 'Not specified by parent']
    * **Any Fears or Sensitivities to Avoid:** [List extracted fears/sensitivities OR 'Not specified by parent']

**2. Story Vision & Goals:**
    * **Primary Purpose of the Book:** [Extracted purpose (e.g., entertainment, specific lesson) OR 'Not specified by parent']
    * **Key Message(s) or Theme(s) to Convey:** [List extracted themes OR 'Not specified by parent']
    * **Desired Tone & Mood:** [List extracted tones (e.g., lighthearted, whimsical) OR 'Not specified by parent']
    * **Desired Story Length/Complexity:** [Extracted details OR 'Not specified by parent']

**3. Content & Element Preferences:**
    * **Main Character Ideas:** [Extracted ideas (e.g., child as protagonist, specific character concepts) OR 'Not specified by parent']
    * **Supporting Character Ideas:** [List extracted ideas (e.g., family members, pets) OR 'Not specified by parent']
    * **Setting Preferences:** [List extracted preferences (e.g., park, magical forest) OR 'Not specified by parent']
    * **Specific Plot Points or Scene Ideas:** [List extracted ideas OR 'Not specified by parent']
    * **'Must-Have' Elements:** [List extracted elements (objects, phrases) OR 'Not specified by parent']
    * **'Elements to Strictly Avoid':** [List extracted elements OR 'Not specified by parent']

**4. Art Style & Visuals (if mentioned by parent):**
    * **Preferred Art Style Descriptors:** [List extracted descriptors (e.g., cartoonish, watercolor) OR 'Not specified by parent']
    * **Any Specific Visual Elements Mentioned:** [List extracted elements (e.g., bright colors, no scary images) OR 'Not specified by parent']

**5. Additional Notes & Context from Parent:**
    * [Include any other relevant extracted information or direct quotes OR 'Not specified by parent']
"""

class CreativeAgent(Agent):
    def __init__(self, provider, system_prompt=None, user_template=None):
        super().__init__(
            "Creative",
            system_prompt if system_prompt is not None else SYSTEM,
            user_template if user_template is not None else TEMPLATE,
            provider
        )
