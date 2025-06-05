import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from intake import IntakeAgent
from llm_providers import OpenAIProvider


async def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    provider = OpenAIProvider(api_key=api_key)
    agent = IntakeAgent(provider)

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
    result = await agent(input=input1)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
