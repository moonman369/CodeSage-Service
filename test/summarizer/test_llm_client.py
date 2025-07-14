from core.summarizer.openrouter_ai_client import OpenRouterAIClient

def test_openrouter_ai_client():

    client = OpenRouterAIClient()
    prompt = "What is the capital of France?"
    
    print(f"Sending prompt to OpenRouter: {prompt}")
    response = client.generate_response(prompt)
    
    print(f"Received response: {response}")

if __name__ == "__main__":
    test_openrouter_ai_client()
