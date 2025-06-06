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

# Optional: Set this to a string to add a custom comment at the top of the log file for this run.
USER_RUN_COMMENT = "new prompt design for intake agent"
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

AGENT_CONFIGS = {
    "intake": {
        "provider_name": "openai",
        "provider_kwargs": {"model": "gpt-4"},
        "system_prompt": None,
        "user_template": None,
    },
    "creative": {
        "provider_name": "together",
        "provider_kwargs": {"model": "deepseek-ai/DeepSeek-R1"},
        "system_prompt": None,
        "user_template": None,
    },
    # Add more agents as needed
}

class Orchestrator:
    def __init__(self, agent_configs):
        self.agent_configs = agent_configs

    def _get_provider(self, provider_name, provider_kwargs):
        if provider_name == "openai":
            return OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), **provider_kwargs)
        elif provider_name == "claude":
            return ClaudeProvider(api_key=os.getenv("CLAUDE_API_KEY"), **provider_kwargs)
        elif provider_name == "grok":
            return GrokProvider(api_key=os.getenv("GROK_API_KEY"), **provider_kwargs)
        elif provider_name == "together":
            return TogetherAIProvider(api_key=os.getenv("TOGETHER_API_KEY"), **provider_kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

    async def run(self):
        """
        Run the orchestrator.
        """
        # intake
        provider = self._get_provider(AGENT_CONFIGS["intake"]["provider_name"], 
                                      AGENT_CONFIGS["intake"]["provider_kwargs"])
        intake_agent = IntakeAgent(provider, 
                                   AGENT_CONFIGS["intake"]["system_prompt"], 
                                   AGENT_CONFIGS["intake"]["user_template"])
        logger.info(f"========== INTAKE MODEL =================================")
        system_prompt, user_prompt = intake_agent.get_formatted_prompts(parental_input=input1)
        logger.info(f"========== INTAKE SYSTEM PROMPT ==========================")
        logger.info(f"========== INTAKE USER PROMPT ===========================")
        intake_md = await intake_agent(parental_input=input1)
        logger.info(f"========== INTAKE RESULT =================================")

        # concepts
        provider = self._get_provider(AGENT_CONFIGS["creative"]["provider_name"], 
                                      AGENT_CONFIGS["creative"]["provider_kwargs"])
        creative_agent = CreativeAgent(provider, 
                                       AGENT_CONFIGS["creative"]["system_prompt"], 
                                       AGENT_CONFIGS["creative"]["user_template"])
        logger.info(f"========== CREATIVE MODEL =================================")
        system_prompt, user_prompt = creative_agent.get_formatted_prompts(creative_brief_md=intake_md)
        logger.info(f"========== CREATIVE SYSTEM PROMPT ==========================")
        logger.info(f"========== CREATIVE USER PROMPT ===========================")
        concepts_md = await creative_agent(creative_brief_md=intake_md)
        logger.info(f"========== CREATIVE RESULT =================================")

        return {
            "intake_md": intake_md,
            "concepts": concepts_md,
        }

async def main():
    orchestrator = Orchestrator(AGENT_CONFIGS)
    result = await orchestrator.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
