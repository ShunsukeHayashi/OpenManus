import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.manus import Manus
from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

# Constants for Dify API interaction
DIFY_API_URL = "https://api.dify.ai/v1"

async def run_dify_workflow_creation_example():
    """
    Demonstrate creating and executing Dify workflows programmatically.
    This example shows how to:
    1. Generate workflow DSL from user input
    2. Create a workflow using the Dify API
    3. Execute the workflow
    4. Visualize the results
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration] Programmatic Dify Workflow Creation")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Initialize Manus agent
    manus = Manus()
    
    # Define user inputs for testing
    user_inputs = [
        # English inputs
        "Create a workflow for a customer service bot that can answer product questions",
        "I need a workflow for data analysis with Python code execution and visualization",
        
        # Japanese inputs
        "製品の質問に答えるカスタマーサービスボットのワークフローを作成してください",
        "Pythonコード実行と可視化を含むデータ分析用のワークフローが必要です"
    ]
    
    # Process each user input
    for i, user_input in enumerate(user_inputs):
        # Determine language based on input (simple heuristic)
        language = "ja" if any(c for c in user_input if ord(c) > 127) else "en"
        
        await demonstrate_workflow_creation(manus, user_input, language, i+1)
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration Complete]")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

async def demonstrate_workflow_creation(manus: Manus, user_input: str, language: str, example_num: int):
    """
    Demonstrate creating a workflow from user input and visualizing it.
    
    Args:
        manus: The Manus agent
        user_input: The user input to generate a workflow from
        language: The language of the user input (en or ja)
        example_num: The example number for display purposes
    """
    print(f"\n\n{'='*80}")
    print(f"Example {example_num}: {user_input}")
    print(f"{'='*80}")
    
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
    
    # Simulate workflow execution
    print("\nSimulating workflow execution...")
    
    # Print workflow structure details instead of visualization
    print("\nWorkflow Structure:")
    print(f"- Name: {workflow_def.get('name', 'Unnamed workflow')}")
    print(f"- Description: {workflow_def.get('description', 'No description')}")
    
    # Print nodes
    nodes = workflow_def.get('graph', {}).get('nodes', [])
    print(f"- Nodes ({len(nodes)}):")
    for node in nodes:
        node_id = node.get('id')
        node_type = node.get('data', {}).get('type', 'unknown')
        node_title = node.get('data', {}).get('title', 'Untitled')
        print(f"  - {node_title} ({node_type}) [ID: {node_id}]")
    
    # Print edges
    edges = workflow_def.get('graph', {}).get('edges', [])
    print(f"- Connections ({len(edges)}):")
    for edge in edges:
        source = edge.get('source')
        target = edge.get('target')
        print(f"  - {source} → {target}")
    
    # Save the workflow definition to a file
    filename = f"workflow_{example_num}_{language}.json"
    save_result = await manus.available_tools.execute(
        "file_saver",
        content=json.dumps(workflow_def, indent=2, ensure_ascii=False),
        file_name=filename
    )
    print(f"Saved workflow definition to {filename}")

if __name__ == "__main__":
    asyncio.run(run_dify_workflow_creation_example())
