import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.manus import Manus
from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

# Constants for Dify UI interaction
DIFY_URL = "https://cloud.dify.ai"
SIGNIN_URL = f"{DIFY_URL}/signin"
WORKFLOW_URL_TEMPLATE = f"{DIFY_URL}/apps/{{app_id}}/workflows"

async def run_dify_ui_automation_example():
    """
    Demonstrate OpenManus controlling Dify UI to create workflows from user input.
    This example shows how to:
    1. Navigate to Dify
    2. Sign in
    3. Navigate to a workflow
    4. Generate a workflow DSL from user input
    5. Import the DSL into Dify
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration] OpenManus controlling Dify UI")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Initialize Manus agent
    manus = Manus()
    
    # Initialize the browser
    print("Initializing browser...")
    await manus.run("I need to control a browser to automate Dify UI.")
    
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
    
    # Demonstrate workflow DSL generation
    await demonstrate_workflow_generation(manus, "Create a customer support chatbot that can answer product questions", "en")
    await demonstrate_workflow_generation(manus, "製品の質問に答えるカスタマーサービスボットを作成する", "ja")
    
    # Clean up browser resources
    await manus.available_tools.get_tool("browser_use").cleanup()
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration Complete]")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

async def demonstrate_workflow_generation(manus: Manus, user_input: str, language: str):
    """
    Demonstrate generating a workflow DSL from user input and visualizing it.
    
    Args:
        manus: The Manus agent
        user_input: The user input to generate a workflow from
        language: The language of the user input (en or ja)
    """
    print(f"\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print(f"[Input] → {user_input}")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Create the DifyDSLGenerator tool
    dsl_generator = DifyDSLGenerator()
    
    # Generate workflow DSL from user input
    print(f"Generating workflow DSL from user input in {language}...")
    result = await dsl_generator.execute(user_input=user_input, language=language)
    
    if result.error:
        print(f"Error generating workflow DSL: {result.error}")
        return
    
    workflow_def = result.output
    
    # Print workflow information
    print(f"\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print(f"[User Intent] → Generate a workflow for {workflow_def.get('description', 'the specified task')}")
    print(f"[Intent] → Workflow with {len(workflow_def.get('graph', {}).get('nodes', []))} nodes")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Print node information
    if 'graph' in workflow_def and 'nodes' in workflow_def['graph']:
        nodes = workflow_def['graph']['nodes']
        print(f"\nNodes ({len(nodes)}):")
        for node in nodes:
            node_type = node.get('data', {}).get('type', 'unknown')
            node_title = node.get('data', {}).get('title', 'Untitled')
            print(f"  - {node_title} ({node_type})")
    
    # Demonstrate programmatic DSL import (without actual login)
    print("\nDemonstrating programmatic DSL import...")
    
    # Execute JavaScript to show how we would import the DSL
    js_code = f"""
    console.log("Programmatically importing workflow DSL:");
    console.log(`Workflow name: {workflow_def.get('name', 'Unnamed')}`);
    console.log(`Description: {workflow_def.get('description', 'No description')}`);
    console.log(`Node count: {len(workflow_def.get('graph', {}).get('nodes', []))}`);
    
    // This is a demonstration of how we would import the DSL
    // In a real implementation with authentication, we would use:
    // fetch(`apps/${{appId}}/workflows/draft/import`, {{
    //   method: 'POST',
    //   headers: {{ 'Content-Type': 'application/json' }},
    //   body: JSON.stringify({{ data: `{json.dumps(workflow_def)}` }})
    // }})
    
    return "DSL import demonstration complete";
    """
    
    js_result = await manus.available_tools.execute(
        "browser_use",
        action="execute_js",
        script=js_code
    )
    print(f"JavaScript execution result: {js_result.output}")
    
    # Take a screenshot to show the current state
    screenshot_result = await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("Captured screenshot of demonstration")

if __name__ == "__main__":
    asyncio.run(run_dify_ui_automation_example())
