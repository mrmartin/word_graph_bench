import asyncio
import openai
import sys
from typing import Optional
import threading
import time

# Configuration
MAX_CONCURRENT_CALLS = 16

# Global components for async processing
_semaphore: Optional[asyncio.Semaphore] = None
_client: Optional[openai.AsyncOpenAI] = None
_loop: Optional[asyncio.AbstractEventLoop] = None
_loop_thread: Optional[threading.Thread] = None

def _initialize_async_components():
    """Initialize async components in a separate thread."""
    global _semaphore, _client, _loop, _loop_thread
    
    if _loop is None:
        def run_event_loop():
            global _loop, _semaphore, _client
            _loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop)
            
            # Create semaphore to limit concurrent requests
            _semaphore = asyncio.Semaphore(MAX_CONCURRENT_CALLS)
            
            # Create async OpenAI client
            _client = openai.AsyncOpenAI(
                base_url="https://chat.martintech.co.uk/v1",#http://localhost:8000/v1
                api_key="EMPTY",
                timeout=600.0
            )
            
            _loop.run_forever()
        
        _loop_thread = threading.Thread(target=run_event_loop, daemon=True)
        _loop_thread.start()
        
        # Wait for loop to be ready
        while _loop is None or _semaphore is None or _client is None:
            time.sleep(0.01)

async def _async_call(prompt: str, json_output: bool = False, call_id: int = 0) -> str:
    """Async implementation with semaphore for concurrency control."""
    global _semaphore, _client
    
    print(f"[{call_id}] Waiting for slot...", end="", flush=True)
    async with _semaphore:  # Limit to 16 concurrent requests
        print(f" calling LLM...", end="", flush=True)
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise responses."},
                {"role": "user", "content": prompt}
            ]
            
            # Add JSON instruction if needed
            if json_output:
                messages[0]["content"] += " Always respond with valid JSON only."
            
            # Make async request
            response = await _client.chat.completions.create(
                model="qwen32-awq",
                messages=messages,
                temperature=0.0,
                max_tokens=20000
            )
            
            print(f" done!", flush=True)
            return response.choices[0].message.content
            
        except Exception as e:
            print(f" error: {e}", flush=True)
            return f"Error: {e}"

# Global counter for call IDs
_call_counter = 0
_counter_lock = threading.Lock()

def call(prompt: str, json_output: bool = False) -> str:
    """Synchronous function that uses async implementation with concurrency control."""
    global _loop, _call_counter
    
    # Get unique call ID
    with _counter_lock:
        _call_counter += 1
        call_id = _call_counter
    
    # Initialize async components if not done yet
    _initialize_async_components()
    
    # Submit task to the event loop running in the background thread
    future = asyncio.run_coroutine_threadsafe(_async_call(prompt, json_output, call_id), _loop)
    
    try:
        # Wait for result (this will block if all 16 slots are busy)
        result = future.result(timeout=600.0)
        return result
    except Exception as e:
        print(f"[{call_id}] Error: {e}", flush=True)
        return f"Error: {e}"