"""
xAI Grok API client for OpenManus.
"""

import os
import httpx
import json
import asyncio
from typing import Dict, List, Optional, Union, Any

from app.logger import logger
from app.config import config


class GrokClient:
    """
    Client for the xAI Grok API.
    """
    
    def __init__(self, api_key: str, model: str = "grok-2-latest", timeout: int = 180):
        """
        Initialize the Grok client.
        
        Args:
            api_key: xAI API key
            model: Model to use (default: grok-2-latest)
            timeout: Timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.base_url = "https://api.x.ai/v1"
        self.http_client = httpx.AsyncClient(timeout=timeout)
        
    async def chat_completions_create(self, 
                              messages: List[Dict[str, str]],
                              max_tokens: int = 4096,
                              temperature: float = 0.0, 
                              stream: bool = False,
                              tools: Optional[List[Dict]] = None,
                              tool_choice: Optional[str] = None,
                              **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to the Grok API.
        
        Args:
            messages: List of messages in the conversation
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            stream: Whether to stream the response
            tools: Optional list of tools
            tool_choice: Optional tool choice
            
        Returns:
            The API response
        """
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }
        
        # Add tools if provided
        if tools:
            data["tools"] = tools
            
        if tool_choice:
            data["tool_choice"] = tool_choice
            
        # Add any additional parameters
        for key, value in kwargs.items():
            data[key] = value
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"Sending request to Grok API with model: {self.model}")
            
            response = await self.http_client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            
            if stream:
                # Return the streaming response for the caller to process
                return response
            else:
                # Parse JSON and return
                return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Grok API HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Grok API request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error with Grok API: {e}")
            raise
            
    async def close(self):
        """Close the HTTP client session."""
        await self.http_client.aclose()
