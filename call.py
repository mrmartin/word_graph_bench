import openai
import sys


def call(prompt: str, json_output: bool = False) -> str:
    """Simple synchronous function that takes a prompt and returns an AI response."""
    try:
        # Create synchronous OpenAI client
        client = openai.OpenAI(
            base_url="http://localhost:8000/v1",#"https://chat.martintech.co.uk/v1",
            api_key="EMPTY",
            timeout=600.0
        )
        
        # Prepare messages
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise responses."},
            {"role": "user", "content": prompt}
        ]
        
        # Add JSON instruction if needed
        if json_output:
            messages[0]["content"] += " Always respond with valid JSON only."
                
        # Make synchronous request
        response = client.chat.completions.create(
            model="qwen32-awq",
            messages=messages,
            temperature=0.0,
            max_tokens=20000
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f" error: {e}", flush=True)
        return f"Error: {e}"
