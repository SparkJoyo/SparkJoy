from typing import List, Dict, Any
import openai
# import anthropic

class LLMProvider:
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
    

# class ClaudeProvider(LLMProvider):
#     def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
#         self.client = anthropic.AsyncAnthropic(api_key=api_key)
#         self.model = model

#     async def generate(self, messages, **kwargs):
#         # Convert messages to Claude format if needed
#         # ...
#         resp = await self.client.messages.create(
#             model=self.model,
#             messages=messages,
#             temperature=kwargs.get("temperature", 0.7),
#             max_tokens=kwargs.get("max_tokens", 1024),
#         )
#         return resp.content[0].text