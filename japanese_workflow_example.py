import asyncio
import json
import sys
import os

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

async def main():
    # Create the DSL generator
    dsl_generator = DifyDSLGenerator()
    
    # Generate a Japanese workflow for a customer support chatbot
    result = await dsl_generator.execute(
        workflow_name="カスタマーサポートボット",
        node_types=["knowledge-retrieval", "llm", "if-else", "template-transform", "answer"],
        description="製品に関する質問に答え、問題解決をサポートするワークフロー",
        variables=[
            {"name": "ユーザー質問", "type": "string"},
            {"name": "製品カテゴリ", "type": "string", "required": False}
        ],
        language="ja"
    )
    
    # Print the result
    print("# 日本語ワークフローDSL例: カスタマーサポートボット")
    print(json.dumps(result.output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
