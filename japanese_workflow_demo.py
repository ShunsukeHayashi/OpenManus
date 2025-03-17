import asyncio
import json
import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.tool.dify_dsl_generator.dsl_generator import DifyDSLGenerator

async def generate_japanese_workflow():
    """Generate a workflow DSL from Japanese user input."""
    # Create the DifyDSLGenerator tool
    dsl_generator = DifyDSLGenerator()
    
    # Japanese user input for data analysis workflow
    user_input_ja = (
        "データ分析アシスタントのためのDifyワークフローを作成してください。"
        "このアシスタントは以下の機能を持ちます："
        "1. データ分析に関するユーザーの質問を受け付ける "
        "2. 知識ベースから関連するコード例を取得する "
        "3. Pythonコードを実行してデータを分析する "
        "4. 可視化を生成する "
        "5. 結果の説明を提供する"
    )
    
    # Generate workflow DSL directly using parameters
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Input] → " + user_input_ja)
    print("[User Intent] → データ分析アシスタントのワークフロー生成")
    print("[Intent] → 複数ノードタイプを含むワークフロー")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Generate workflow using direct parameters
    workflow = {
        "name": "データ分析アシスタント",
        "description": "データ分析に関する質問に答え、コードを実行し、結果を可視化するアシスタント",
        "graph": {
            "nodes": [
                {
                    "id": "start",
                    "position": None,
                    "data": {
                        "title": "開始",
                        "type": "start",
                        "variables": [
                            {
                                "variable": "質問",
                                "type": "string",
                                "required": True,
                                "default": ""
                            }
                        ]
                    }
                },
                {
                    "id": "knowledge-retrieval_0",
                    "position": None,
                    "data": {
                        "title": "知識検索",
                        "type": "knowledge-retrieval",
                        "query_variable_selector": [
                            "sys",
                            "query"
                        ],
                        "dataset_ids": [],
                        "retrieval_mode": "multiple",
                        "single_retrieval_config": None,
                        "multiple_retrieval_config": {
                            "top_k": 3,
                            "score_threshold": 0.5,
                            "reranking_model": None
                        }
                    }
                },
                {
                    "id": "code_1",
                    "position": None,
                    "data": {
                        "title": "Pythonコード実行",
                        "type": "code",
                        "language": "python",
                        "code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport io\nimport base64\n\n# サンプルデータの作成\ndata = {'カテゴリ': ['A', 'B', 'C', 'D'], '値': [10, 25, 15, 30]}\ndf = pd.DataFrame(data)\n\n# グラフの作成\nplt.figure(figsize=(10, 6))\nplt.bar(df['カテゴリ'], df['値'], color='skyblue')\nplt.title('データ分析結果')\nplt.xlabel('カテゴリ')\nplt.ylabel('値')\n\n# 画像をBase64エンコード\nbuffer = io.BytesIO()\nplt.savefig(buffer, format='png')\nbuffer.seek(0)\nimg_str = base64.b64encode(buffer.read()).decode('utf-8')\n\n# 結果を返す\nresult = {\n    'データフレーム': df.to_dict(),\n    'グラフ': f'data:image/png;base64,{img_str}',\n    '分析結果': 'カテゴリDが最も高い値を示しています。'\n}\n\nresult"
                    }
                },
                {
                    "id": "llm_2",
                    "position": None,
                    "data": {
                        "title": "言語モデル",
                        "type": "llm",
                        "model": {
                            "provider": "openai",
                            "name": "gpt-3.5-turbo",
                            "mode": "chat",
                            "completion_params": {
                                "temperature": 0.7,
                                "top_p": 1,
                                "presence_penalty": 0,
                                "frequency_penalty": 0,
                                "max_tokens": 1000
                            }
                        },
                        "prompt_template": [
                            {
                                "role": "user",
                                "text": "以下のデータ分析結果について、詳細な説明を日本語で提供してください。\n\n質問: {{#sys.query#}}\n\nコード実行結果: {{#code.result#}}"
                            }
                        ],
                        "memory": {
                            "role_prefix": None,
                            "window": {
                                "enabled": True,
                                "max_messages": 10
                            }
                        },
                        "context": {
                            "enabled": False,
                            "variable_selector": None
                        },
                        "vision": {
                            "enabled": False,
                            "variable_selector": None,
                            "configs": None
                        }
                    }
                },
                {
                    "id": "template-transform_3",
                    "position": None,
                    "data": {
                        "title": "テンプレート変換",
                        "type": "template-transform",
                        "template": "# データ分析結果\n\n## 質問\n{{#sys.query#}}\n\n## 分析\n{{#llm.text#}}\n\n## 可視化\n![データ分析グラフ]({{#code.result.グラフ#}})"
                    }
                },
                {
                    "id": "answer_4",
                    "position": None,
                    "data": {
                        "title": "回答",
                        "type": "answer",
                        "answer": "{{#template-transform.text#}}"
                    }
                },
                {
                    "id": "end",
                    "position": None,
                    "data": {
                        "title": "終了",
                        "type": "end",
                        "outputs": [
                            {
                                "variable": "result",
                                "value_selector": [
                                    "template-transform",
                                    "text"
                                ]
                            }
                        ]
                    }
                }
            ],
            "edges": [
                {
                    "id": "start-knowledge-retrieval_0",
                    "source": "start",
                    "target": "knowledge-retrieval_0"
                },
                {
                    "id": "knowledge-retrieval_0-code_1",
                    "source": "knowledge-retrieval_0",
                    "target": "code_1"
                },
                {
                    "id": "code_1-llm_2",
                    "source": "code_1",
                    "target": "llm_2"
                },
                {
                    "id": "llm_2-template-transform_3",
                    "source": "llm_2",
                    "target": "template-transform_3"
                },
                {
                    "id": "template-transform_3-answer_4",
                    "source": "template-transform_3",
                    "target": "answer_4"
                },
                {
                    "id": "answer_4-end",
                    "source": "answer_4",
                    "target": "end"
                }
            ]
        },
        "features": {
            "opening_statement": "こんにちは、データ分析アシスタントです。どのようなデータ分析をお手伝いしましょうか？",
            "suggested_questions": [
                "売上データの傾向分析をしてください",
                "顧客セグメントの分類方法を教えてください",
                "時系列データの予測モデルを作成してください"
            ],
            "suggested_questions_after_answer": [],
            "speech_to_text": False,
            "text_to_speech": False,
            "file_upload": True,
            "sensitive_word_avoidance": False,
            "retriever_resource": {
                "enabled": True
            }
        }
    }
    
    # Save the workflow to a file
    with open('japanese_workflow.json', 'w', encoding='utf-8') as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("ワークフロー構造")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Display workflow structure
    nodes = workflow["graph"]["nodes"]
    edges = workflow["graph"]["edges"]
    
    print(f"ワークフロー名: {workflow['name']}")
    print(f"説明: {workflow['description']}")
    print(f"ノード数: {len(nodes)}")
    print(f"エッジ数: {len(edges)}")
    print("\nノード情報:")
    
    for node in nodes:
        print(f"  - ID: {node['id']}, タイプ: {node['data']['type']}, タイトル: {node['data']['title']}")
    
    print("\nノード接続:")
    for edge in edges:
        source_node = next((n for n in nodes if n['id'] == edge['source']), None)
        target_node = next((n for n in nodes if n['id'] == edge['target']), None)
        if source_node and target_node:
            print(f"  - {source_node['data']['title']} → {target_node['data']['title']}")
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("ワークフローDSLの生成が完了しました。")
    print("ファイル: japanese_workflow.json")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    return workflow

if __name__ == "__main__":
    asyncio.run(generate_japanese_workflow())
