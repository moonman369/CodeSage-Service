from .interfaces import LLMClientInterface
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

# Replace this with real OpenAI or other client later
class OpenRouterAIClient(LLMClientInterface):
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.3):
        self.api_key = os.getenv("SUMMARIZER_OPENROUTER_API_KEY") or ""
        self.model = model
        self.temperature = temperature

    def generate_response(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
                    "X-Title": "CodeSage", # Optional. Site title for rankings on openrouter.ai.
                },
                # model="openai/gpt-4o",
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                messages=messages,
                max_tokens=4000
            )
            print(f"[✅] OpenAI API Response: {completion.choices[0].message.content}")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[❌] OpenAI API Error: {e}")
            return ""