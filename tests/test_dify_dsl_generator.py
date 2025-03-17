import asyncio
import json
import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

async def test_dify_dsl_generator():
    """Test the DifyDSLGenerator tool."""
    # Create the tool
    dsl_generator = DifyDSLGenerator()
    
    # Test with English
    result_en = await dsl_generator.execute(
        workflow_name="Test Workflow",
        node_types=["llm", "answer"],
        description="A test workflow",
        variables=[{"name": "input", "type": "string"}],
        language="en"
    )
    
    # Test with Japanese
    result_ja = await dsl_generator.execute(
        workflow_name="テストワークフロー",
        node_types=["llm", "answer"],
        description="テストワークフロー",
        variables=[{"name": "入力", "type": "string"}],
        language="ja"
    )
    
    # Print the results
    print("English Workflow:")
    print(json.dumps(result_en.output, indent=2, ensure_ascii=False))
    print("\nJapanese Workflow:")
    print(json.dumps(result_ja.output, indent=2, ensure_ascii=False))
    
    # Test with more complex workflow
    result_complex = await dsl_generator.execute(
        workflow_name="Complex Workflow",
        node_types=["knowledge-retrieval", "llm", "template-transform", "code", "answer"],
        description="A complex workflow with multiple node types",
        variables=[
            {"name": "query", "type": "string"},
            {"name": "file", "type": "file"}
        ],
        language="en"
    )
    
    print("\nComplex Workflow:")
    print(json.dumps(result_complex.output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_dify_dsl_generator())
