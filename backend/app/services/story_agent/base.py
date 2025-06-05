# agents/base.py
from __future__ import annotations
import openai, os, textwrap, asyncio
from typing import Any, Dict
from app.services.story_agent.llm_providers import LLMProvider

openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self, name: str, system_prompt: str, user_template: str, provider: LLMProvider):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.user_template = textwrap.dedent(user_template).strip()
        self.provider = provider

    async def __call__(self, **kwargs) -> str:
        user_msg = self.user_template.format(**kwargs)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_msg}
        ]
        return await self.provider.generate(messages, **kwargs)

# Example usage
# provider = OpenAIProvider(api_key="sk-...", model="gpt-4o-mini")
# agent = Agent("myagent", "You are helpful.", "Hello, {name}!", provider)
# result = await agent(name="Alice")