import pytest
from unittest.mock import AsyncMock, patch
from app.services.story_agent.llm_providers import OpenAIProvider

@pytest.mark.asyncio
async def test_openai_provider_generate():
    # Patch openai.AsyncOpenAI
    with patch("openai.AsyncOpenAI") as MockAsyncOpenAI:
        mock_client = MockAsyncOpenAI.return_value
        mock_chat = mock_client.chat
        mock_completions = mock_chat.completions
        mock_create = mock_completions.create
        mock_create.return_value = AsyncMock()
        mock_create.return_value.choices = [type("obj", (), {"message": type("obj", (), {"content": "test output"})()})]

        provider = OpenAIProvider(api_key="fake-key", model="gpt-4o")
        messages = [{"role": "system", "content": "sys"}, {"role": "user", "content": "hi"}]
        result = await provider.generate(messages)
        assert result == "test output"
        mock_create.assert_awaited_once() 