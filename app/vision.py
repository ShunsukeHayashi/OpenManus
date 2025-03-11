"""
Vision model initialization and utilities for OpenManus.
This module initializes the qwq-32b vision model based on the configuration in config.toml.
"""

from app.llm import LLM
from app.logger import logger

def initialize_vision_model():
    """
    Initialize the qwq-32b vision model using the configuration in config.toml.
    
    Returns:
        LLM: The initialized vision model instance
    """
    try:
        # Initialize the vision model from the 'vision' section in config
        vision_model = LLM(config_name="vision")
        logger.info(f"Vision model initialized: {vision_model.model}")
        return vision_model
    except Exception as e:
        logger.error(f"Failed to initialize vision model: {e}")
        raise

# Create a global instance that can be imported
try:
    vision_llm = initialize_vision_model()
except Exception as e:
    logger.error(f"Error during vision model initialization: {e}")
    vision_llm = None
