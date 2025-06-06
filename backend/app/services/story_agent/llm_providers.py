from typing import List, Dict, Any
import openai
import anthropic
import together
import xai_sdk
import httpx

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
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
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
        return resp.content[0].text           # ≥ 1.3.5
# If you prefer sync calls, swap in:  from openai import OpenAI


class TogetherAIProvider(LLMProvider):
    """
    Async provider for Together AI's chat completions API.
    Requires: together API key (https://docs.together.ai/docs/inference)
    Example usage:
        provider = TogetherAIProvider(api_key="TOGETHER_API_KEY", model="mistralai/Mixtral-8x7B-Instruct-v0.1")
        messages = provider.format_messages("You are helpful.", "Hello!")
        result = await provider.generate(messages)
    """
    def __init__(self, api_key: str, model: str = "deepseek-ai/DeepSeek-R1"):
        self.client = together.AsyncClient(api_key=api_key)
        self.model = model

    async def generate(self, messages, **kwargs):
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7)
        )
        return resp.choices[0].message.content


class GrokProvider(LLMProvider):
    """
    Asynchronous provider for xAI Grok models via the native REST API.
    Example
    -------
    prov = GrokProvider(api_key="XAI_API_KEY", model="grok-2-latest")
    msgs = prov.format_messages("You are a helpful assistant.", "Hello Grok!")
    answer = await prov.generate(msgs)
    """
    _BASE_URL = "https://api.x.ai/v1"

    def __init__(self, api_key: str, model: str = "grok-3"):
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self._BASE_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            timeout=30.0,
        )

    # ────────────────────────────────────────────────
    # Message helpers
    # ────────────────────────────────────────────────
    def format_messages(
        self,
        system_prompt: str,
        user_msg: str,
        **_: Any
    ) -> List[Dict[str, str]]:
        """
        Grok follows the OpenAI-style schema: each message has a role and content.
        """
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ]

    # ────────────────────────────────────────────────
    # Generation
    # ────────────────────────────────────────────────
    async def generate(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Sends a chat completion request and returns the assistant’s reply text.
        """
        payload = {
            "model":       self.model,
            "messages":    messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens":  kwargs.get("max_tokens", 1024),
            # You can pass in any other Grok/Chat-Completions params here
        }

        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()        # raises if xAI returns 4xx/5xx
        data = resp.json()

        # xAI mirrors the OpenAI response shape:
        return data["choices"][0]["message"]["content"]

    async def __aexit__(self, *exc):
        await self._client.aclose()
