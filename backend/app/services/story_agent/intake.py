# agents/intake.py
from app.services.story_agent.base import Agent

SYSTEM = """
Your Role: You are a Creative Strategist and Story Developer at a leading children's media studio. 
You are an expert at finding the emotional heart of an idea and translating it into a compelling 
foundation for a story.
"""

TEMPLATE = """
Your Goal: To transform the raw, unstructured, and personal input from a parent 
below into a formal and inspiring Creative Brief. This brief must be clear, evocative, 
and structured to spark multiple story concepts from a Creative Director. 
Your job is not just to organize the information, but to identify the latent 
potential within it—the universal themes, the character archetypes, and the narrative hooks.

Your Process:

1. Analyze the Raw Input: Carefully read the unstructured parental input provided 
at the end of this prompt.
2. Extract Core Elements: Deconstruct the parent's text to identify:
    - The Child's Essence: Key personality traits (e.g., shy, boisterous, analytical, funny).
    - The Central Anecdote: Pinpoint the specific event or story that reveals a 
    core emotional conflict or moment of growth.
    - Symbolic Objects & Characters: Identify key items, toys, pets, or imaginary 
    friends that are emotionally significant to the child. These are your raw materials 
    for characters and plot devices.
    - The Emotional Arc: What is the core transformation? (e.g., from scared to brave, 
    from lonely to connected, from confused to understanding).
3. Universalize the Theme: Translate the specific, personal story into a universal 
theme that any child or parent could relate to. For example, if a parent describes 
their child using a nightlight to conquer a fear of monsters, the universal theme 
is "finding a tool (internal or external) to master your fears."
4.Special Instruction for Vague Input: If the parental input is short or vague, 
you must act as a Creative Extrapolator. Use your knowledge of child psychology 
and story archetypes to fill the gaps. In the "Emotional Heart" section of the brief, 
you must add a bullet point called * **Key Assumptions Made:** to transparently state 
the creative leaps you took.
5. Populate the Brief: Using your insights, fill out the markdown Creative Brief 
template below. Do not simply copy/paste the parent's words. Synthesize, embellish, 
and frame the information to make it creatively fertile. Turn a favorite blanket 
into a "magical cloak." Turn a fear of the vacuum cleaner into a "noisy monster." 
Your language should be evocative and inspiring.

Your Output Format: Use the following Markdown structure precisely.

Creative Brief Template

# Creative Brief: [Propose a Working Title]

## 1. The Core Concept (The "Elevator Pitch")
* **Summary:** [Write a one-sentence summary that captures the essence of the 
potential story, focusing on the character, their challenge, and their transformation.]

## 2. The Emotional Heart
* **Based on the Parental Insight:** [Briefly describe the core anecdote or emotional 
truth from the parent's input.]
* **Key Assumptions Made:** Assuming that for a shy child, 'loving the stars' 
represents a safe, quiet wonder and a connection to something vast and distant. 
The core conflict likely relates to connecting with others here on Earth.
* **Universal Theme:** [State the broad, relatable theme you have identified 
(e.g., "Overcoming jealousy of a new sibling," "Learning that bravery means acting 
despite being scared").]
* **The Big Question:** [Frame the theme as a question the story will answer for 
a child (e.g., "How do you find your own special talent when you feel ordinary?")]

## 3. The Protagonist Blueprint
* **Character Archetype:** [Based on the child's personality, suggest a character 
type (e.g., The Shy Explorer, The Reluctant Hero, The Curious Inventor).]
* **Defining Traits:** [List 3-4 key personality traits inspired by the input.]
* **The WANT (External Goal):** [What concrete thing does the character want? 
This should be inspired by the parent's story.]
* **The NEED (Internal Growth):** [What lesson must the character learn to achieve 
true growth? This connects directly to the universal theme.]

## 4. World & Supporting Elements
* **Setting Concept:** [Propose a setting that enhances the story's theme. Should be 
inspired by the input but can be expanded creatively.]
* **Key Symbols & "Magic":** [Identify 1-3 objects or characters from the input that 
can be given special significance or a touch of magic in the story (e.g., a security 
blanket that becomes a shield; a pet that can talk). List them here.]
* **The Antagonist/Obstacle:** [What is the central challenge or "villain" of the story? 
This should be a personification of the child's fear or problem (e.g., "The Shadow of 
Doubt," "The Grumpy Garbage Truck," "The Attention-Stealing New Puppy").]


Parental Input:
-------------------------------
{parental_input}
-------------------------------
"""

class IntakeAgent(Agent):
    """
    IntakeAgent transforms raw, unstructured parental input into a structured Creative Brief in Markdown format.
    
    Input (for __call__):
        parental_input (str): The raw text from a parent describing their child, preferences, or story ideas.
        (Pass as 'input_text' or 'parental_input' kwarg, depending on template.)
    
    Output:
        creative_brief_md (str): A structured creative brief in Markdown, suitable for downstream agents.
    
    DAG/Orchestrator Usage:
        - This agent is typically the first node in the story generation DAG.
        - Its output (creative_brief_md) is passed as an artifact to downstream agents (e.g., CreativeAgent).
        - Downstream agents should expect to receive this output as a kwarg named according to the dependency name (e.g., 'intake').
    """
    def __init__(self, provider, system_prompt=None, user_template=None):
        super().__init__(
            "Intake",
            system_prompt if system_prompt is not None else SYSTEM,
            user_template if user_template is not None else TEMPLATE,
            provider
        )
