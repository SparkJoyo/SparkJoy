import asyncio
import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from base import Agent
from intake import IntakeAgent
from creative import CreativeAgent
from llm_providers import OpenAIProvider, ClaudeProvider, GrokProvider, TogetherAIProvider


# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_filename = log_dir / f"llm_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


PROVIDER = "together"  # Change to "openai" or "claude"

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

creative_brief_test_without_structured_creative_brief = f"""
{input1}
"""

# Optional: Set this to a string to add a custom comment at the top of the log file for this run.
USER_RUN_COMMENT = "Testing DS model without structured creative brief."
if USER_RUN_COMMENT:
    RUN_COMMENT = f"""
# =============================================
# USER COMMENT:
# {USER_RUN_COMMENT}
# =============================================
"""
else:
    RUN_COMMENT = f"""
# =============================================
# LLM RUN - {datetime.now().isoformat()}
# Input: 
# {input1}
# Main Creative Brief (truncated):
# {(' '.join(line.strip() for line in str(creative_brief).splitlines() if line)[:300])}
# =============================================
"""

# Write the run comment at the top of the log file
with open(log_filename, "w") as f:
    f.write(RUN_COMMENT)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    if PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        provider = OpenAIProvider(api_key=api_key)
        model_version = provider.model
    elif PROVIDER == "claude":
        api_key = os.getenv("CLAUDE_API_KEY")
        provider = ClaudeProvider(api_key=api_key)
        model_version = provider.model
    elif PROVIDER == "grok":
        api_key = os.getenv("GROK_API_KEY")
        provider = GrokProvider(api_key=api_key)
        model_version = provider.model
    elif PROVIDER == "together":
        api_key = os.getenv("TOGETHER_API_KEY")
        provider = TogetherAIProvider(api_key=api_key)
        model_version = provider.model
    else:
        raise ValueError(f"Unknown provider: {PROVIDER}")

    creative_agent = CreativeAgent(provider)
    system_prompt, user_prompt = creative_agent.get_formatted_prompts(creative_brief_md=creative_brief_test_without_structured_creative_brief)

    logger.info(f"Model Provider: {PROVIDER}")
    logger.info(f"Model Version: {model_version}")
    logger.info("========== SYSTEM PROMPT ==========")
    logger.info(system_prompt)
    logger.info("========== USER PROMPT ==========")
    logger.info(user_prompt)

    result = await creative_agent(creative_brief_md=creative_brief)
    logger.info("========== RESULT ==========")
    logger.info(result)

if __name__ == "__main__":
    asyncio.run(main())
