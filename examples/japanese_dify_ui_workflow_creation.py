"""
Japanese Dify UI Workflow Creation Example

This script demonstrates how to create a Japanese data analysis workflow
directly in the Dify UI using browser automation with OpenManus.
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional, List

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.manus import Manus
from examples.dify_ui_workflow_builder import DifyUIWorkflowBuilder

async def create_japanese_data_analysis_workflow(manus: Manus, app_id: str):
    """
    Create a Japanese data analysis workflow directly in the Dify UI.
    
    Args:
        manus: The Manus agent
        app_id: The app ID for the workflow
    """
    builder = DifyUIWorkflowBuilder(manus)
    
    # Navigate to workflow page
    print("ワークフローページに移動しています...")
    if not await builder.navigate_to_workflow(app_id):
        print("ワークフローページへの移動に失敗しました")
        return
    
    # Add LLM node after Start node
    print("LLMノードを追加しています...")
    if not await builder.add_node("start", "LLM"):
        print("LLMノードの追加に失敗しました")
        return
    
    # Configure LLM node with Japanese prompt
    print("LLMノードを設定しています...")
    llm_config = {
        "prompt": """あなたはデータ分析アシスタントです。
ユーザーのデータを分析し、洞察を提供してください。
以下の点に注意してください：
1. データの傾向や特徴を明確に説明する
2. 視覚化の提案を行う
3. 統計的な分析結果を日本語で分かりやすく説明する
4. 必要に応じてPythonコードを提供する"""
    }
    if not await builder.configure_node("llm", llm_config):
        print("LLMノードの設定に失敗しました")
        return
    
    # Add Code node after LLM node
    print("Codeノードを追加しています...")
    if not await builder.add_node("llm", "Code"):
        print("Codeノードの追加に失敗しました")
        return
    
    # Configure Code node with Python code for data analysis
    print("Codeノードを設定しています...")
    code_config = {
        "code": """# データ分析用のPythonコード
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from typing import Dict, Any

def analyze_data(data_str: str) -> Dict[str, Any]:
    # データを分析し、結果を返す関数
    # データをDataFrameに変換
    try:
        # CSVデータの場合
        df = pd.read_csv(io.StringIO(data_str))
    except:
        try:
            # JSON形式の場合
            df = pd.read_json(io.StringIO(data_str))
        except:
            return {"error": "データの形式が認識できませんでした。CSV形式またはJSON形式のデータを提供してください。"}
    
    # 基本的な統計情報
    stats = df.describe().to_dict()
    
    # 欠損値の確認
    missing_values = df.isnull().sum().to_dict()
    
    # 相関関係の計算（数値データのみ）
    numeric_df = df.select_dtypes(include=[np.number])
    correlation = {}
    if not numeric_df.empty:
        correlation = numeric_df.corr().to_dict()
    
    # データの可視化（ヒストグラム）
    visualizations = {}
    for col in numeric_df.columns[:3]:  # 最初の3つの数値列のみ可視化
        plt.figure(figsize=(8, 6))
        plt.hist(df[col].dropna(), bins=20)
        plt.title(f"{col}のヒストグラム")
        plt.xlabel(col)
        plt.ylabel("頻度")
        
        # 画像をBase64エンコード
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        visualizations[col] = img_str
        plt.close()
    
    return {
        "statistics": stats,
        "missing_values": missing_values,
        "correlation": correlation,
        "visualizations": visualizations
    }

# 入力データを分析
input_data = input_data if 'input_data' in locals() else ""
result = analyze_data(input_data)

# 結果を返す
return result
"""
    }
    if not await builder.configure_node("code", code_config):
        print("Codeノードの設定に失敗しました")
        return
    
    # Add Answer node after Code node
    print("Answerノードを追加しています...")
    if not await builder.add_node("code", "Answer"):
        print("Answerノードの追加に失敗しました")
        return
    
    # Save the workflow
    print("ワークフローを保存しています...")
    if not await builder.save_workflow():
        print("ワークフローの保存に失敗しました")
        return
    
    # Take a screenshot of the completed workflow
    await builder.take_screenshot()
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[ワークフロー作成完了] データ分析アシスタント")
    print("ノード: Start → LLM → Code → Answer")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

async def run_japanese_dify_ui_workflow_creation():
    """
    Demonstrate the creation of a Japanese data analysis workflow in Dify UI.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[デモンストレーション] 日本語Dify UIワークフロー作成")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Initialize Manus agent
    manus = Manus()
    
    # Initialize the browser
    print("ブラウザを初期化しています...")
    # Initialize browser directly without requiring LLM calls
    await manus.available_tools.execute(
        "browser_use",
        action="initialize"
    )
    print("ブラウザが正常に初期化されました")
    
    # Navigate to Dify signin page
    signin_url = "https://cloud.dify.ai/signin"
    print(f"Difyサインインページに移動しています: {signin_url}")
    result = await manus.available_tools.execute(
        "browser_use",
        action="navigate",
        url=signin_url
    )
    print(f"ナビゲーション結果: {result.output}")
    
    # Take a screenshot to show the signin page
    await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("サインインページのスクリーンショットを撮影しました")
    
    # Wait for user to sign in
    print("\nDifyに手動でサインインしてください。サインイン完了後にEnterキーを押してください...")
    input()
    
    # Create a Japanese data analysis workflow
    app_id = input("URL内のアプリIDを入力してください (例: 12345-abcd-67890): ")
    await create_japanese_data_analysis_workflow(manus, app_id)
    
    # Clean up browser resources
    await manus.available_tools.get_tool("browser_use").cleanup()
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[デモンストレーション完了]")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(run_japanese_dify_ui_workflow_creation())
