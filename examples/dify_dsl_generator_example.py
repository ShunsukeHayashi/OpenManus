import asyncio
import json
import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

async def run_dify_dsl_generator_example():
    """Run an example of using the DifyDSLGenerator directly."""
    # Create the DifyDSLGenerator tool
    dsl_generator = DifyDSLGenerator()
    
    # Example 1: Generate workflow using direct parameters in English
    print("\n=== Example 1: Generate workflow using direct parameters in English ===")
    result1 = await dsl_generator.execute(
        workflow_name="Customer Support Chatbot",
        description="A chatbot that can answer questions about product features, pricing, and troubleshooting",
        node_types=["knowledge-retrieval", "llm", "answer"],
        variables=[
            {"name": "query", "type": "string"},
            {"name": "product_id", "type": "string"}
        ],
        language="en"
    )
    print(json.dumps(result1.output, indent=2, ensure_ascii=False))
    
    # Example 2: Generate workflow using direct parameters in Japanese
    print("\n=== Example 2: Generate workflow using direct parameters in Japanese ===")
    result2 = await dsl_generator.execute(
        workflow_name="日本文化チャットボット",
        description="日本の文化について質問に答えるチャットボット",
        node_types=["knowledge-retrieval", "llm", "answer"],
        variables=[
            {"name": "質問", "type": "string"}
        ],
        language="ja"
    )
    print(json.dumps(result2.output, indent=2, ensure_ascii=False))
    
    # Example 3: Generate workflow using user input in English
    print("\n=== Example 3: Generate workflow using user input in English ===")
    user_input = (
        "Create a Dify workflow for a data analysis assistant that can: "
        "1. Accept user queries about data analysis "
        "2. Retrieve relevant code examples from a knowledge base "
        "3. Execute Python code to analyze data "
        "4. Generate visualizations "
        "5. Provide explanations of the results"
    )
    result3 = await dsl_generator.execute(user_input=user_input, language="en")
    print(json.dumps(result3.output, indent=2, ensure_ascii=False))
    
    # Example 4: Generate workflow using user input in Japanese
    print("\n=== Example 4: Generate workflow using user input in Japanese ===")
    user_input_ja = (
        "データ分析アシスタントのためのDifyワークフローを作成してください。"
        "このアシスタントは以下の機能を持ちます："
        "1. データ分析に関するユーザーの質問を受け付ける "
        "2. 知識ベースから関連するコード例を取得する "
        "3. Pythonコードを実行してデータを分析する "
        "4. 可視化を生成する "
        "5. 結果の説明を提供する"
    )
    result4 = await dsl_generator.execute(user_input=user_input_ja, language="ja")
    print(json.dumps(result4.output, indent=2, ensure_ascii=False))
    
    # Print visualization for the last example
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print(f"[Input] → {user_input_ja}")
    print(f"[User Intent] → データ分析アシスタントのワークフロー生成")
    print(f"[Intent] → 複数ノードタイプを含むワークフロー")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(run_dify_dsl_generator_example())
