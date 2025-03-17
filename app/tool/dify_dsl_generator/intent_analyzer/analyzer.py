"""Intent analyzer for Dify DSL Generator."""
import json
from typing import Dict, List, Any, Optional

from app.llm import LLM


class IntentAnalyzer:
    """Analyzes user intent to determine appropriate workflow configuration."""

    def __init__(self):
        """Initialize the intent analyzer."""
        self.llm = LLM()

    async def analyze(
        self, user_input: str, language: str = "en"
    ) -> Dict[str, Any]:
        """
        Analyze user input to determine workflow configuration.

        Args:
            user_input: The user input to analyze
            language: The language to use for the analysis (en or ja)

        Returns:
            A dictionary containing the workflow configuration
        """
        # Prepare the system prompt
        system_prompt = self._get_system_prompt(language)
        
        # Prepare the user prompt
        user_prompt = self._get_user_prompt(user_input, language)
        
        # Call the LLM
        response = await self.llm.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        
        # Parse the response
        try:
            content = response.choices[0].message.content
            # Extract the JSON part
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback to default configuration
                return self._get_default_config(language)
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return self._get_default_config(language)

    def _get_system_prompt(self, language: str) -> str:
        """
        Get the system prompt for the intent analyzer.

        Args:
            language: The language to use for the prompt

        Returns:
            The system prompt
        """
        if language == "ja":
            return """
あなたはDifyワークフローDSLジェネレーターのインテント分析エキスパートです。
ユーザーの入力を分析し、適切なワークフロー設定を決定します。
以下の情報を含むJSONオブジェクトを返してください：

1. workflow_name: ワークフローの名前
2. description: ワークフローの説明
3. node_types: ワークフローに含めるノードタイプのリスト（以下から選択）
   - start（必須）
   - end（必須）
   - llm（言語モデル）
   - knowledge-retrieval（知識検索）
   - http-request（HTTPリクエスト）
   - code（コード実行）
   - template-transform（テンプレート変換）
   - answer（回答）
   - if-else（条件分岐）
   - iteration（繰り返し）
4. variables: ワークフローの変数のリスト（各変数は名前、タイプ、必須かどうかを含む）

ユーザーの意図を分析し、最も適切なワークフロー設定を決定してください。
回答は必ずJSON形式で返してください。
"""
        else:
            return """
You are an intent analysis expert for the Dify Workflow DSL Generator.
Analyze the user input to determine the appropriate workflow configuration.
Return a JSON object with the following information:

1. workflow_name: The name of the workflow
2. description: A description of the workflow
3. node_types: A list of node types to include in the workflow (select from the following)
   - start (required)
   - end (required)
   - llm (language model)
   - knowledge-retrieval (knowledge retrieval)
   - http-request (HTTP request)
   - code (code execution)
   - template-transform (template transformation)
   - answer (answer)
   - if-else (conditional)
   - iteration (loop)
4. variables: A list of variables for the workflow (each with a name, type, and whether it's required)

Analyze the user's intent and determine the most appropriate workflow configuration.
Always return your response in JSON format.
"""

    def _get_user_prompt(self, user_input: str, language: str) -> str:
        """
        Get the user prompt for the intent analyzer.

        Args:
            user_input: The user input to analyze
            language: The language to use for the prompt

        Returns:
            The user prompt
        """
        if language == "ja":
            return f"""
以下のユーザー入力を分析し、適切なDifyワークフロー設定を決定してください：

ユーザー入力: {user_input}

以下の形式でJSON応答を返してください：

{{
  "workflow_name": "ワークフロー名",
  "description": "ワークフローの説明",
  "node_types": ["必要なノードタイプのリスト"],
  "variables": [
    {{
      "name": "変数名",
      "type": "string/number/boolean/file",
      "required": true/false
    }}
  ]
}}

ユーザーの意図に最も適したワークフロー設定を提供してください。
"""
        else:
            return f"""
Analyze the following user input and determine the appropriate Dify workflow configuration:

User Input: {user_input}

Return your response in the following JSON format:

{{
  "workflow_name": "Workflow Name",
  "description": "Workflow Description",
  "node_types": ["List of required node types"],
  "variables": [
    {{
      "name": "Variable Name",
      "type": "string/number/boolean/file",
      "required": true/false
    }}
  ]
}}

Provide the workflow configuration that best matches the user's intent.
"""

    def _get_default_config(self, language: str) -> Dict[str, Any]:
        """
        Get the default workflow configuration.

        Args:
            language: The language to use for the configuration

        Returns:
            The default workflow configuration
        """
        if language == "ja":
            return {
                "workflow_name": "基本ワークフロー",
                "description": "基本的な質問応答ワークフロー",
                "node_types": ["llm", "answer"],
                "variables": [
                    {
                        "name": "質問",
                        "type": "string",
                        "required": True
                    }
                ]
            }
        else:
            return {
                "workflow_name": "Basic Workflow",
                "description": "A basic question-answering workflow",
                "node_types": ["llm", "answer"],
                "variables": [
                    {
                        "name": "query",
                        "type": "string",
                        "required": True
                    }
                ]
            }
