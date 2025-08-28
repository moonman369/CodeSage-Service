from .base_llm_client import BaseLLMClient
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

# Replace this with real OpenAI or other client later
class OpenRouterAIClient(BaseLLMClient):
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.3):
        self.api_key = os.getenv("SUMMARIZER_OPENROUTER_API_KEY")
        self.api_url = os.getenv("SUMMARIZER_OPENROUTER_API_URL")
        self.openrouter_model = os.getenv("SUMMARIZER_OPENROUTER_MODEL")
        if not self.api_key:
            raise ValueError("OpenRouter API key not found in environment variables.")
        if not self.api_url:
            raise ValueError("OpenRouter API URL not found in environment variables.")
        if not self.openrouter_model:
            raise ValueError("OpenRouter model not found in environment variables.")
        self.model = model
        self.temperature = temperature

    def generate_response(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        try:
            client = OpenAI(
                base_url=self.api_url,
                api_key=self.api_key,
            )
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
                    "X-Title": "CodeSage", # Optional. Site title for rankings on openrouter.ai.
                },
                # model="openai/gpt-4o",
                model=self.openrouter_model,
                messages=messages,
                max_tokens=4000
            )
            print(f"[✅] OpenAI API Response: {completion.choices[0].message.content}")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[❌] OpenAI API Error: {e}")
            return ""