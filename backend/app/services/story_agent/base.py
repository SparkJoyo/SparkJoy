# agents/base.py
from __future__ import annotations
import openai, os, textwrap, asyncio, string
from typing import Any, Dict
from app.services.story_agent.llm_providers import LLMProvider

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_required_variables(template):
    return {v for _, v, _, _ in string.Formatter().parse(template) if v}

class Agent:
    def __init__(self, name: str, system_prompt: str, user_template: str, provider: LLMProvider):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.user_template = textwrap.dedent(user_template).strip()
        self.provider = provider

    def _format_user_message(self, **kwargs):
        required = get_required_variables(self.user_template)
        missing = required - kwargs.keys()
        if missing:
            raise ValueError(f"Missing required variables for user_template: {missing}")
        return self.user_template.format(**kwargs)

    def get_formatted_prompts(self, **kwargs):
        user_msg = self._format_user_message(**kwargs)
        return self.system_prompt, user_msg

    async def __call__(self, **kwargs) -> str:
        user_msg = self._format_user_message(**kwargs)
        messages = self.provider.format_messages(
            self.system_prompt, 
            user_msg, 
            **kwargs)
        return await self.provider.generate(messages, **kwargs)

# Example usage
# provider = OpenAIProvider(api_key="sk-...", model="gpt-4o-mini")
# agent = Agent("myagent", "You are helpful.", "Hello, {name}!", provider)
# result = await agent(name="Alice")