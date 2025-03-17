import os
import json
import webbrowser
from pathlib import Path

# Load the workflow JSON
workflow_path = Path(__file__).parent / "japanese_workflow.json"
with open(workflow_path, "r", encoding="utf-8") as f:
    workflow = json.load(f)

# Create HTML visualization
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>データ分析アシスタント ワークフロー可視化</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .workflow-info {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f0f7ff;
            border-radius: 5px;
        }
        .workflow-graph {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 30px 0;
        }
        .node-row {
            display: flex;
            margin-bottom: 50px;
            position: relative;
            width: 100%;
            justify-content: center;
        }
        .node {
            width: 180px;
            height: 80px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-weight: bold;
            margin: 0 15px;
            position: relative;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .node-title {
            font-size: 14px;
            margin-bottom: 5px;
        }
        .node-type {
            font-size: 12px;
            opacity: 0.8;
        }
        .edge {
            position: absolute;
            width: 2px;
            background-color: #666;
            z-index: -1;
        }
        .edge::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: -4px;
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 10px solid #666;
        }
        .start { background-color: #4CAF50; }
        .knowledge-retrieval { background-color: #2196F3; }
        .code { background-color: #9C27B0; }
        .llm { background-color: #FF9800; }
        .template-transform { background-color: #795548; }
        .answer { background-color: #607D8B; }
        .end { background-color: #F44336; }
        
        .border-marker {
            font-family: monospace;
            color: #666;
            margin: 20px 0;
            font-size: 16px;
        }
        
        .input-section {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .node-list, .edge-list {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .node-item, .edge-item {
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }
        
        .node-item::before, .edge-item::before {
            content: "•";
            position: absolute;
            left: 5px;
            color: #2196F3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
        <h1>データ分析アシスタント ワークフロー可視化</h1>
        <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
        
        <div class="input-section">
            <h2>ユーザー入力</h2>
            <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
            <p><strong>[Input]</strong> → データ分析アシスタントのためのDifyワークフローを作成してください。このアシスタントは以下の機能を持ちます：1. データ分析に関するユーザーの質問を受け付ける 2. 知識ベースから関連するコード例を取得する 3. Pythonコードを実行してデータを分析する 4. 可視化を生成する 5. 結果の説明を提供する</p>
            <p><strong>[User Intent]</strong> → データ分析アシスタントのワークフロー生成</p>
            <p><strong>[Intent]</strong> → 複数ノードタイプを含むワークフロー</p>
            <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
        </div>
        
        <div class="workflow-info">
            <h2>ワークフロー情報</h2>
            <p><strong>名前:</strong> データ分析アシスタント</p>
            <p><strong>説明:</strong> データ分析に関する質問に答え、コードを実行し、結果を可視化するアシスタント</p>
            <p><strong>ノード数:</strong> 7</p>
            <p><strong>エッジ数:</strong> 6</p>
        </div>
        
        <h2>ワークフロー構造</h2>
        <div class="workflow-graph">
            <!-- Row 1: Start -->
            <div class="node-row">
                <div class="node start">
                    <div class="node-title">開始</div>
                    <div class="node-type">start</div>
                </div>
            </div>
            
            <!-- Edge 1 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 2: Knowledge Retrieval -->
            <div class="node-row">
                <div class="node knowledge-retrieval">
                    <div class="node-title">知識検索</div>
                    <div class="node-type">knowledge-retrieval</div>
                </div>
            </div>
            
            <!-- Edge 2 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 3: Code -->
            <div class="node-row">
                <div class="node code">
                    <div class="node-title">Pythonコード実行</div>
                    <div class="node-type">code</div>
                </div>
            </div>
            
            <!-- Edge 3 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 4: LLM -->
            <div class="node-row">
                <div class="node llm">
                    <div class="node-title">言語モデル</div>
                    <div class="node-type">llm</div>
                </div>
            </div>
            
            <!-- Edge 4 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 5: Template Transform -->
            <div class="node-row">
                <div class="node template-transform">
                    <div class="node-title">テンプレート変換</div>
                    <div class="node-type">template-transform</div>
                </div>
            </div>
            
            <!-- Edge 5 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 6: Answer -->
            <div class="node-row">
                <div class="node answer">
                    <div class="node-title">回答</div>
                    <div class="node-type">answer</div>
                </div>
            </div>
            
            <!-- Edge 6 -->
            <div class="edge" style="height: 50px;"></div>
            
            <!-- Row 7: End -->
            <div class="node-row">
                <div class="node end">
                    <div class="node-title">終了</div>
                    <div class="node-type">end</div>
                </div>
            </div>
        </div>
        
        <div class="node-list">
            <h2>ノード情報</h2>
            <div class="node-item"><strong>ID: start, タイプ: start, タイトル: 開始</strong></div>
            <div class="node-item"><strong>ID: knowledge-retrieval_0, タイプ: knowledge-retrieval, タイトル: 知識検索</strong></div>
            <div class="node-item"><strong>ID: code_1, タイプ: code, タイトル: Pythonコード実行</strong></div>
            <div class="node-item"><strong>ID: llm_2, タイプ: llm, タイトル: 言語モデル</strong></div>
            <div class="node-item"><strong>ID: template-transform_3, タイプ: template-transform, タイトル: テンプレート変換</strong></div>
            <div class="node-item"><strong>ID: answer_4, タイプ: answer, タイトル: 回答</strong></div>
            <div class="node-item"><strong>ID: end, タイプ: end, タイトル: 終了</strong></div>
        </div>
        
        <div class="edge-list">
            <h2>ノード接続</h2>
            <div class="edge-item"><strong>開始 → 知識検索</strong></div>
            <div class="edge-item"><strong>知識検索 → Pythonコード実行</strong></div>
            <div class="edge-item"><strong>Pythonコード実行 → 言語モデル</strong></div>
            <div class="edge-item"><strong>言語モデル → テンプレート変換</strong></div>
            <div class="edge-item"><strong>テンプレート変換 → 回答</strong></div>
            <div class="edge-item"><strong>回答 → 終了</strong></div>
        </div>
        
        <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
        <p>ワークフローDSLの生成が完了しました。</p>
        <p>ファイル: japanese_workflow.json</p>
        <div class="border-marker">◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢</div>
    </div>
</body>
</html>
"""

# Save HTML file
html_path = Path(__file__).parent / "workflow_visualization.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Open in browser
print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
print("ワークフロー可視化を生成しました")
print(f"ファイル: {html_path}")
print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

# Try to open in browser
try:
    webbrowser.open(f"file://{html_path.absolute()}")
    print("ブラウザでワークフロー可視化を開きました")
except Exception as e:
    print(f"ブラウザでの表示に失敗しました: {e}")
    print(f"ファイルパス: {html_path.absolute()}")

print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
print("Difyへのインポート手順:")
print("1. Difyアプリケーションを開く")
print("2. ワークフローエディタに移動")
print("3. インポートボタンをクリック")
print("4. japanese_workflow.jsonファイルをアップロード")
print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
