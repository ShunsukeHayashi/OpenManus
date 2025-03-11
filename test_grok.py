"""
Test script for using the Grok-2 model.
"""
import os
import asyncio
from app.llm import LLM

# Set API key directly
os.environ["XAI_API_KEY"] = "xai-zMKUqIpcBmT52Tl4NJcVLZsGmQCe97ES5dGWWUaawDQo0ArQc0a2TAQXHxOBoEuuXr1xtVrZN7Zt0rtm"

async def test_grok():
    """Test Grok-2 model by sending a simple query."""
    # Initialize the Grok LLM instance
    llm = LLM("grok")
    
    # Print model info
    print(f"Using model: {llm.model}")
    print(f"Client type: {llm.client_type}")
    
    # Test simple query
    response = await llm.ask(
        [{"role": "user", "content": "Explain quantum computing in simple terms."}],
        stream=False  # Disable streaming for cleaner output
    )
    
    print("\nGrok response:")
    print("-" * 40)
    print(response)
    print("-" * 40)
    
    # Test with system message
    system_msg = [{"role": "system", "content": "You are a helpful assistant that specializes in explaining complex topics in simple terms."}]
    
    response2 = await llm.ask(
        [{"role": "user", "content": "What is the significance of neural networks in AI?"}],
        system_msgs=system_msg,
        stream=False
    )
    
    print("\nGrok response with system message:")
    print("-" * 40)
    print(response2)
    print("-" * 40)
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    # Check if API key is set
    if "XAI_API_KEY" not in os.environ:
        print("Warning: XAI_API_KEY environment variable not found.")
        print("Please set your xAI API key in the environment or in this script.")
        print("Attempting to proceed anyway in case the key is configured in config.toml...")
    
    # Run the test
    asyncio.run(test_grok())
