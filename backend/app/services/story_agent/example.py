import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from intake import IntakeAgent
from llm_providers import OpenAIProvider, ClaudeProvider

PROVIDER = "claude"  # Change to "openai" or "claude"

async def main():
    if PROVIDER == "openai":
        provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    elif PROVIDER == "claude":
        provider = ClaudeProvider(api_key=os.getenv("CLAUDE_API_KEY"))
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
    intake_agent = IntakeAgent(provider)
    system_prompt, user_prompt = intake_agent.get_formatted_prompts(parental_input=input1)
    # print("SYSTEM PROMPT:\n", system_prompt)
    # print("USER PROMPT:\n", user_prompt)
    result = await intake_agent(parental_input=input1)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
