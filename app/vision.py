"""
Vision model initialization and utilities for OpenManus.
This module initializes the qwq-32b vision model based on the configuration in config.toml.
"""

import os
import requests
from app.llm import LLM
from app.logger import logger
from app.config import config

def check_vision_model_availability(base_url, timeout=2):
    """
    Check if the vision model endpoint is available
    
    Args:
        base_url (str): The base URL of the vision model
        timeout (int): Timeout in seconds
        
    Returns:
        bool: True if available, False otherwise
    """
    try:
        # Strip /v1 from the end if present for the health check
        check_url = base_url.rstrip('/v1')
        if not check_url.startswith(('http://', 'https://')):
            check_url = f"http://{check_url}"
            
        # Add a simple health check endpoint
        health_url = f"{check_url}/health" if check_url.endswith('/') else f"{check_url}/health"
        
        # Try a simple GET request to check if service is up
        response = requests.get(health_url, timeout=timeout)
        if response.status_code == 200:
            logger.info(f"Vision model endpoint is available: {base_url}")
            return True
        else:
            logger.warning(f"Vision model endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.warning(f"Vision model endpoint is not available: {e}")
        return False

def initialize_vision_model():
    """
    Initialize the qwq-32b vision model using the configuration in config.toml.
    
    Returns:
        LLM: The initialized vision model instance
    """
    try:
        # Get the vision model settings
        vision_config = config.llm.get("vision", None)
        if not vision_config:
            logger.warning("No vision model configuration found, falling back to default model")
            return LLM()
            
        # Check if the vision model endpoint is available
        if not check_vision_model_availability(vision_config.base_url):
            # Check if we should fall back to the default model
            fallback = getattr(vision_config, "fallback_to_default", False)
            if fallback:
                logger.warning("Vision model endpoint is not available, falling back to default model")
                return LLM()
            else:
                logger.error("Vision model endpoint is not available and fallback is disabled")
                return None
        
        # Initialize the vision model
        vision_model = LLM(config_name="vision")
        logger.info(f"Vision model initialized: {vision_model.model}")
        return vision_model
    except Exception as e:
        logger.error(f"Failed to initialize vision model: {e}")
        fallback = getattr(config.llm.get("vision", {}), "fallback_to_default", False)
        if fallback:
            logger.warning(f"Falling back to default model due to error: {e}")
            return LLM()
        return None

# Create a global instance that can be imported
vision_llm = initialize_vision_model()
if vision_llm is None:
    logger.warning("Vision model not available. Some vision features may not work.")
else:
    logger.info(f"Vision model ready: {vision_llm.model}")
