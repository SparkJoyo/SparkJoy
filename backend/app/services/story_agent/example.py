import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from base import Agent
from intake import IntakeAgent
from creative import CreativeAgent
from llm_providers import OpenAIProvider, ClaudeProvider, GrokProvider

PROVIDER = "grok"  # Change to "openai" or "claude"

creative_brief = """
**Creative Brief**

**1. Child's Profile:**
    * **Child's Name (for reference/use in story):** Olivia
    * **Child's Age:** 3
    * **Key Interests & Passions:** Not specified by parent
    * **Favorite Books/Characters:** Not specified by parent
    * **Child's Personality Insights:** Not specified by parent
    * **Any Fears or Sensitivities to Avoid:** Not specified by parent

**2. Story Vision & Goals:**
    * **Primary Purpose of the Book:** To celebrate Olivia learning to zip up her own jacket
    * **Key Message(s) or Theme(s) to Convey:** Pride in accomplishing a new skill (zipping jacket), having fun outdoors at the park 
    * **Desired Tone & Mood:** Not specified by parent
    * **Desired Story Length/Complexity:** Short and sweet

**3. Content & Element Preferences:**
    * **Main Character Ideas:** A girl like Olivia (possibly named Olivia)
    * **Supporting Character Ideas:** Not specified by parent
    * **Setting Preferences:** Getting ready to go out, then having fun at the park
    * **Specific Plot Points or Scene Ideas:** Girl zipping up her jacket by herself (make zipper sound like "Zzzzzzip!"), then going to the park to feed ducks
    * **'Must-Have' Elements:** Olivia or girl like her, zipping jacket by herself, zipper sound "Zzzzzzip!", going to park, feeding ducks
    * **'Elements to Strictly Avoid':** Not specified by parent

**4. Art Style & Visuals (if mentioned by parent):**
    * **Preferred Art Style Descriptors:** Not specified by parent
    * **Any Specific Visual Elements Mentioned:** Not specified by parent

**5. Additional Notes & Context from Parent:**
    * Olivia just learned to put on her own jacket with the zipper this morning before going to the park to feed ducks.
"""

async def main():
    if PROVIDER == "openai":
        provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    elif PROVIDER == "claude":
        provider = ClaudeProvider(api_key=os.getenv("CLAUDE_API_KEY"))
    elif PROVIDER == "grok":
        provider = GrokProvider(api_key=os.getenv("GROK_API_KEY"))
    else:
        raise ValueError(f"Unknown provider: {PROVIDER}")

    input0 = """
    Story. Girl. Ball. Park. Lily 2 yrs. She got a new bouncy ball today.
    """
    input1 = """
pls make a story for olivia she is 3. she just learned to put on her OWN jacket 
with the zipper! she did it all by herself before we went to the park this 
morning to feed ducks. can the story be about olivia or a girl like her getting 
ready to go out, zipping her jacket (make the zipper sound like Zzzzzzip!), 
and then having fun at the park? short and sweet please.
    """
    # intake_agent = IntakeAgent(provider)
    # system_prompt, user_prompt = intake_agent.get_formatted_prompts(parental_input=input1)
    # print("SYSTEM PROMPT:\n", system_prompt)
    # print("USER PROMPT:\n", user_prompt)
    # result = await intake_agent(parental_input=input1)
    # print(result)
    # user_prompt = f"""based on the parental input: 
    # {input1} 
    # generate 3 creative concepts for a picture book story."""
    creative_agent = CreativeAgent(provider)
    system_prompt, user_prompt = creative_agent.get_formatted_prompts(creative_brief_md=creative_brief)
    print("========== SYSTEM PROMPT ==========")
    print(system_prompt)
    print("========== USER PROMPT ==========")
    print(user_prompt)
    result = await creative_agent(creative_brief_md=creative_brief)
    print("========== RESULT ==========")
    print(result)

    # what if i just pass in the parental input directly and ask for 3 concepts?
    # Example usage
    # base_agent = Agent("base_agent", system_prompt="", user_template=input1, provider=provider)
    # system_prompt, user_prompt = base_agent.get_formatted_prompts(creative_brief_md=creative_brief)
    # print("========== SYSTEM PROMPT ==========")
    # print(system_prompt)
    # print("========== USER PROMPT ==========")
    # print(user_prompt)
    # result = await base_agent()
    # print("========== RESULT ==========")
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
