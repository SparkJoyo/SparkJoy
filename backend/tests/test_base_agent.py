import pytest
import asyncio
from app.services.story_agent.base import Agent
from app.services.story_agent.llm_providers import LLMProvider

class DummyProvider(LLMProvider):
    async def generate(self, messages, **kwargs):
        # Return the messages for inspection
        return messages

@pytest.mark.asyncio
async def test_agent_message_formatting():
    provider = DummyProvider()
    agent = Agent(
        name="TestAgent",
        system_prompt="System prompt.",
        user_template="Hello, {name}!",
        provider=provider
    )
    result = await agent(name="Alice")
    assert result[0]["role"] == "system"
    assert result[0]["content"] == "System prompt."
    assert result[1]["role"] == "user"
    assert result[1]["content"] == "Hello, Alice!" 