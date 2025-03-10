"""
streaming_responses.py

This module implements a streaming response mechanism. Instead of waiting for the entire
LLM output, responses can be streamed back incrementally.
"""

import time
from typing import Generator

def stream_response(response: str, chunk_size: int = 20) -> Generator[str, None, None]:
    """
    Generator that yields chunks of the response string.
    """
    for i in range(0, len(response), chunk_size):
        yield response[i:i + chunk_size]
        time.sleep(0.1)  # Simulate delay for streaming
