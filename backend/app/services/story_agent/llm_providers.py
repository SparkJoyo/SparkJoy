from typing import List, Dict, Any
import openai
import anthropic

class LLMProvider:
    def format_messages(self, system_prompt, user_msg, **kwargs):
        # Default: OpenAI-style
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(self, messages, **kwargs):
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7)
        )
        return resp.choices[0].message.content
    

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model

    def format_messages(self, system_prompt, user_msg, **kwargs):
        # Claude expects a single system prompt and a single user message string
        # We'll concatenate if needed
        return [
            {"role": "user", "content": f"{system_prompt}\n\n{user_msg}"}
        ]

    async def generate(self, messages, **kwargs):
        # Claude expects a list of messages, but typically just one user message
        resp = await self.client.messages.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1024),
        )
        return resp.content[0].text