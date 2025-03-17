"""
Dify UI Direct Workflow Creation Example

This script demonstrates how to create a workflow directly in the Dify UI
using browser automation with OpenManus.
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional, List

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.manus import Manus
from app.tool.browser_use_tool import BrowserUseTool

# Constants for Dify UI interaction
DIFY_URL = "https://cloud.dify.ai"
SIGNIN_URL = f"{DIFY_URL}/signin"
WORKFLOW_URL_TEMPLATE = f"{DIFY_URL}/apps/{{app_id}}/workflows"

async def run_dify_ui_direct_workflow_creation():
    """
    Demonstrate direct Dify UI workflow creation using browser automation.
    This example shows how to:
    1. Navigate to Dify
    2. Sign in (handled by user)
    3. Navigate to a workflow
    4. Create a workflow directly in the UI
    5. Configure node properties
    6. Connect nodes
    7. Save and publish the workflow
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration] Direct Dify UI Workflow Creation")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Initialize Manus agent
    manus = Manus()
    
    # Initialize the browser
    print("Initializing browser...")
    # Initialize browser directly without requiring LLM calls
    await manus.available_tools.execute(
        "browser_use",
        action="initialize"
    )
    print("Browser initialized successfully")
    
    # Navigate to Dify signin page
    print(f"Navigating to Dify signin page: {SIGNIN_URL}")
    result = await manus.available_tools.execute(
        "browser_use",
        action="navigate",
        url=SIGNIN_URL
    )
    print(f"Navigation result: {result.output}")
    
    # Take a screenshot to show the signin page
    screenshot_result = await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("Captured screenshot of signin page")
    
    # Wait for user to sign in
    print("\nPlease sign in to Dify manually. Press Enter when signed in...")
    input()
    
    # Create a data analysis workflow
    app_id = input("Enter the app ID from the URL (e.g., 12345-abcd-67890): ")
    await create_data_analysis_workflow(manus, app_id)
    
    # Clean up browser resources
    await manus.available_tools.get_tool("browser_use").cleanup()
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration Complete]")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

async def create_data_analysis_workflow(manus: Manus, app_id: str):
    """
    Create a data analysis workflow directly in the Dify UI.
    
    Args:
        manus: The Manus agent
        app_id: The app ID for the workflow
    """
    # Navigate to the workflow page
    workflow_url = WORKFLOW_URL_TEMPLATE.format(app_id=app_id)
    print(f"Navigating to workflow page: {workflow_url}")
    await manus.available_tools.execute(
        "browser_use",
        action="navigate",
        url=workflow_url
    )
    
    # Wait for page to load
    await asyncio.sleep(2)
    
    # Take a screenshot to show the workflow page
    screenshot_result = await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("Captured screenshot of workflow page")
    
    # Create workflow nodes using JavaScript execution for more reliable interaction
    print("Creating workflow nodes...")
    
    # Find the start node and add an LLM node
    js_add_llm_node = """
    // Find the start node
    const startNode = document.querySelector('[data-type="start"]');
    if (!startNode) {
        return "Start node not found";
    }
    
    // Find the plus button on the start node
    const plusButton = startNode.querySelector('.plus-button') || 
                       startNode.querySelector('[class*="plus"]') ||
                       startNode.querySelector('[class*="add"]');
    if (!plusButton) {
        return "Plus button not found on start node";
    }
    
    // Click the plus button
    plusButton.click();
    
    return "Clicked plus button on start node";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_add_llm_node
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for block selector to appear
    await asyncio.sleep(1)
    
    # Select LLM node from block selector
    js_select_llm = """
    // Find the LLM option in the block selector
    const llmOption = Array.from(document.querySelectorAll('[class*="block-item"]')).find(
        el => el.textContent.includes('LLM') || el.textContent.includes('Language Model')
    );
    
    if (!llmOption) {
        return "LLM option not found";
    }
    
    // Click the LLM option
    llmOption.click();
    
    return "Selected LLM node";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_select_llm
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for LLM node to be added
    await asyncio.sleep(1)
    
    # Configure LLM node
    js_configure_llm = """
    // Find the LLM node
    const llmNode = document.querySelector('[data-type="llm"]');
    if (!llmNode) {
        return "LLM node not found";
    }
    
    // Click the LLM node to open configuration panel
    llmNode.click();
    
    return "Clicked LLM node for configuration";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_configure_llm
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for configuration panel to open
    await asyncio.sleep(1)
    
    # Add a prompt to the LLM node
    js_add_prompt = """
    // Find the prompt textarea
    const promptTextarea = document.querySelector('textarea[placeholder*="prompt"]') || 
                          document.querySelector('textarea[class*="prompt"]');
    
    if (!promptTextarea) {
        return "Prompt textarea not found";
    }
    
    // Set the prompt text
    promptTextarea.value = "You are a data analysis assistant. Help the user analyze their data and provide insights.";
    
    // Trigger input event to ensure the value is registered
    promptTextarea.dispatchEvent(new Event('input', { bubbles: true }));
    
    return "Added prompt to LLM node";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_add_prompt
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Add an Answer node
    js_add_answer_node = """
    // Find the LLM node
    const llmNode = document.querySelector('[data-type="llm"]');
    if (!llmNode) {
        return "LLM node not found";
    }
    
    // Find the plus button on the LLM node
    const plusButton = llmNode.querySelector('.plus-button') || 
                       llmNode.querySelector('[class*="plus"]') ||
                       llmNode.querySelector('[class*="add"]');
    if (!plusButton) {
        return "Plus button not found on LLM node";
    }
    
    // Click the plus button
    plusButton.click();
    
    return "Clicked plus button on LLM node";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_add_answer_node
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for block selector to appear
    await asyncio.sleep(1)
    
    # Select Answer node from block selector
    js_select_answer = """
    // Find the Answer option in the block selector
    const answerOption = Array.from(document.querySelectorAll('[class*="block-item"]')).find(
        el => el.textContent.includes('Answer')
    );
    
    if (!answerOption) {
        return "Answer option not found";
    }
    
    // Click the Answer option
    answerOption.click();
    
    return "Selected Answer node";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_select_answer
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for Answer node to be added
    await asyncio.sleep(1)
    
    # Save the workflow
    js_save_workflow = """
    // Find the save button
    const saveButton = Array.from(document.querySelectorAll('button')).find(
        el => el.textContent.includes('Save') && !el.textContent.includes('Publish')
    );
    
    if (!saveButton) {
        return "Save button not found";
    }
    
    // Click the save button
    saveButton.click();
    
    return "Clicked save button";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_save_workflow
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Wait for save to complete
    await asyncio.sleep(2)
    
    # Take a screenshot of the completed workflow
    screenshot_result = await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("Captured screenshot of completed workflow")
    
    # Print workflow information
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Workflow Created] Data Analysis Assistant")
    print("Nodes: Start → LLM → Answer")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(run_dify_ui_direct_workflow_creation())
