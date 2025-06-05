import pytest
import asyncio
from app.services.story_agent.intake import IntakeAgent
from app.services.story_agent.llm_providers import LLMProvider

class DummyProvider(LLMProvider):
    async def generate(self, messages, **kwargs):
        # Simulate a response for testing
        return "Simulated creative brief output"

@pytest.mark.asyncio
async def test_intake_agent_basic():
    provider = DummyProvider()
    agent = IntakeAgent(provider)
    parental_input = "My son Max is 5 and loves dinosaurs."
    result = await agent(input=parental_input)
    assert "Simulated creative brief output" in result
