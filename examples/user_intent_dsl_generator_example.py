import asyncio
import json
import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

async def run_user_intent_example():
    """
    Run an example demonstrating dynamic workflow DSL generation from user intent.
    This example shows how to use the DifyDSLGenerator with natural language input.
    """
    # Create the DifyDSLGenerator tool
    dsl_generator = DifyDSLGenerator()
    
    # Define user inputs for testing
    user_inputs = [
        # English inputs
        "Create a workflow for a customer service bot that can answer product questions",
        "I need a workflow for data analysis with Python code execution and visualization",
        "Build a workflow for a travel recommendation system with knowledge retrieval",
        
        # Japanese inputs
        "製品の質問に答えるカスタマーサービスボットのワークフローを作成してください",
        "Pythonコード実行と可視化を含むデータ分析用のワークフローが必要です",
        "知識検索機能を持つ旅行推薦システムのワークフローを構築してください"
    ]
    
    # Process each user input
    for i, user_input in enumerate(user_inputs):
        print(f"\n\n{'='*80}")
        print(f"Example {i+1}: {user_input}")
        print(f"{'='*80}")
        
        # Determine language based on input (simple heuristic)
        language = "ja" if any(c for c in user_input if ord(c) > 127) else "en"
        
        # Generate workflow DSL from user intent
        result = await dsl_generator.execute(user_input=user_input, language=language)
        
        if result.error:
            print(f"Error: {result.error}")
            continue
            
        workflow_def = result.output
        
        # Print workflow information
        print(f"\nGenerated Workflow: {workflow_def.get('name', 'Unnamed')}")
        print(f"Description: {workflow_def.get('description', 'No description')}")
        
        # Print node information
        if 'graph' in workflow_def and 'nodes' in workflow_def['graph']:
            nodes = workflow_def['graph']['nodes']
            print(f"\nNodes ({len(nodes)}):")
            for node in nodes:
                node_type = node.get('data', {}).get('type', 'unknown')
                node_title = node.get('data', {}).get('title', 'Untitled')
                print(f"  - {node_title} ({node_type})")
        
        # Print visualization markers
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print(f"[Input] → {user_input}")
        print(f"[User Intent] → Generate a workflow for {workflow_def.get('description', 'the specified task')}")
        print(f"[Intent] → Workflow with {len(workflow_def.get('graph', {}).get('nodes', []))} nodes")
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(run_user_intent_example())
