from typing import Dict, List, Optional, Any

from pydantic import Field

from app.tool.base import BaseTool, ToolResult
from app.tool.dify_dsl_generator.intent_analyzer import IntentAnalyzer


class DifyDSLGenerator(BaseTool):
    """
    A tool for generating Dify workflow DSL based on user input.
    Supports Japanese language and can create various node types.
    """
    name: str = "dify_dsl_generator"
    description: str = """
    Generate Dify workflow DSL based on user input. This tool can create workflow definitions
    with various node types including START, END, LLM, HTTP_REQUEST, and more. Supports Japanese language.
    """
    parameters: dict = {
        "type": "object",
        "properties": {
            "user_input": {
                "type": "string",
                "description": "Natural language description of the workflow to generate. If provided, other parameters are optional.",
            },
            "workflow_name": {
                "type": "string",
                "description": "Name of the workflow to generate",
            },
            "description": {
                "type": "string",
                "description": "Description of the workflow",
            },
            "node_types": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["start", "end", "llm", "knowledge-retrieval", "http-request", 
                             "code", "template-transform", "answer", "if-else", "iteration"]
                },
                "description": "Types of nodes to include in the workflow",
            },
            "variables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["string", "number", "boolean", "file"]}
                    }
                },
                "description": "Variables to include in the workflow",
            },
            "language": {
                "type": "string",
                "enum": ["en", "ja"],
                "description": "Language for the workflow (English or Japanese)",
                "default": "en"
            }
        },
        "required": []
    }
    
    # Define intent_analyzer as a Pydantic field
    intent_analyzer: IntentAnalyzer = Field(default_factory=IntentAnalyzer)
    
    def __init__(self):
        """Initialize the DSL generator with an intent analyzer."""
        super().__init__()
        
    async def execute(
        self,
        user_input: Optional[str] = None,
        workflow_name: Optional[str] = None,
        node_types: Optional[List[str]] = None,
        description: Optional[str] = "",
        variables: Optional[List[Dict]] = None,
        language: str = "en",
    ) -> ToolResult:
        """
        Generate a Dify workflow DSL based on the provided parameters or user input.
        
        Args:
            user_input: Natural language description of the workflow to generate
            workflow_name: Name of the workflow
            node_types: Types of nodes to include
            description: Description of the workflow
            variables: Variables to include
            language: Language for the workflow (en or ja)
            
        Returns:
            ToolResult containing the generated workflow DSL
        """
        try:
            # If user_input is provided, analyze it to determine workflow configuration
            if user_input:
                try:
                    # Analyze user input to determine workflow configuration
                    config = await self.intent_analyzer.analyze(user_input, language)
                    
                    # Extract configuration values
                    workflow_name = config.get("workflow_name", workflow_name or "Generated Workflow")
                    description = config.get("description", description or "")
                    node_types = config.get("node_types", node_types or ["llm", "answer"])
                    variables = config.get("variables", variables or [])
                except Exception as e:
                    return ToolResult(error=f"Failed to analyze user input: {str(e)}")
            
            # Ensure required parameters are set
            if workflow_name is None:
                workflow_name = "Default Workflow"
            
            if node_types is None:
                node_types = ["llm", "answer"]
                
            # Initialize variables if not provided
            if variables is None:
                variables = []
                
            # Generate the workflow graph
            graph = self._generate_workflow_graph(node_types, variables, language)
            
            # Generate features based on node types
            features = self._generate_features(node_types, language)
            
            # Create the complete workflow definition
            workflow_definition = {
                "name": workflow_name,
                "description": description,
                "graph": graph,
                "features": features
            }
            
            return ToolResult(output=workflow_definition)
        except Exception as e:
            return ToolResult(error=f"Failed to generate workflow DSL: {str(e)}")
    
    def _generate_workflow_graph(self, node_types: List[str], variables: List[Dict], language: str) -> Dict:
        """
        Generate the workflow graph with nodes and edges.
        
        Args:
            node_types: Types of nodes to include
            variables: Variables to include
            language: Language for the workflow
            
        Returns:
            Dictionary containing the workflow graph
        """
        nodes = []
        edges = []
        
        # Always include start node
        start_node = self._create_start_node(variables, language)
        nodes.append(start_node)
        
        # Create nodes based on node_types
        previous_node_id = start_node["id"]
        for i, node_type in enumerate(node_types):
            if node_type == "start":
                continue  # Skip start node as it's already added
                
            node_id = f"{node_type}_{i}"
            node = self._create_node(node_type, node_id, language)
            nodes.append(node)
            
            # Create edge from previous node to current node
            edge = {
                "id": f"{previous_node_id}-{node_id}",
                "source": previous_node_id,
                "target": node_id
            }
            edges.append(edge)
            
            previous_node_id = node_id
        
        # Always include end node if not already included
        if "end" not in node_types:
            end_node = self._create_end_node(language)
            nodes.append(end_node)
            
            # Create edge from last node to end node
            edge = {
                "id": f"{previous_node_id}-{end_node['id']}",
                "source": previous_node_id,
                "target": end_node["id"]
            }
            edges.append(edge)
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def _create_start_node(self, variables: List[Dict], language: str) -> Dict:
        """Create a start node with the given variables."""
        title = "START" if language == "en" else "開始"
        
        # Convert variables to the format expected by Dify
        formatted_variables = []
        for var in variables:
            formatted_variables.append({
                "variable": var["name"],
                "type": var["type"],
                "required": True,
                "default": ""
            })
        
        return {
            "id": "start",
            "position": None,
            "data": {
                "title": title,
                "type": "start",
                "variables": formatted_variables
            }
        }
    
    def _create_end_node(self, language: str) -> Dict:
        """Create an end node."""
        title = "END" if language == "en" else "終了"
        
        return {
            "id": "end",
            "position": None,
            "data": {
                "title": title,
                "type": "end",
                "outputs": [{
                    "variable": "result",
                    "value_selector": ["llm", "text"]
                }]
            }
        }
    
    def _create_node(self, node_type: str, node_id: str, language: str) -> Dict:
        """Create a node of the specified type."""
        # Define node titles in English and Japanese
        titles = {
            "llm": {"en": "LLM", "ja": "言語モデル"},
            "knowledge-retrieval": {"en": "KNOWLEDGE RETRIEVAL", "ja": "知識検索"},
            "http-request": {"en": "HTTP REQUEST", "ja": "HTTPリクエスト"},
            "code": {"en": "CODE", "ja": "コード"},
            "template-transform": {"en": "TEMPLATE TRANSFORM", "ja": "テンプレート変換"},
            "answer": {"en": "ANSWER", "ja": "回答"},
            "if-else": {"en": "IF-ELSE", "ja": "条件分岐"},
            "iteration": {"en": "ITERATION", "ja": "繰り返し"}
        }
        
        title = titles.get(node_type, {}).get(language, node_type.upper())
        
        # Create node based on type
        if node_type == "llm":
            return self._create_llm_node(node_id, title)
        elif node_type == "knowledge-retrieval":
            return self._create_knowledge_retrieval_node(node_id, title)
        elif node_type == "http-request":
            return self._create_http_request_node(node_id, title)
        elif node_type == "code":
            return self._create_code_node(node_id, title)
        elif node_type == "template-transform":
            return self._create_template_transform_node(node_id, title)
        elif node_type == "answer":
            return self._create_answer_node(node_id, title)
        elif node_type == "if-else":
            return self._create_if_else_node(node_id, title)
        elif node_type == "iteration":
            return self._create_iteration_node(node_id, title)
        else:
            # Default node
            return {
                "id": node_id,
                "position": None,
                "data": {
                    "title": title,
                    "type": node_type
                }
            }
    
    def _create_llm_node(self, node_id: str, title: str) -> Dict:
        """Create an LLM node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
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
                        "text": "{{#sys.query#}}"
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
        }
    
    def _create_knowledge_retrieval_node(self, node_id: str, title: str) -> Dict:
        """Create a knowledge retrieval node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "knowledge-retrieval",
                "query_variable_selector": ["sys", "query"],
                "dataset_ids": [],
                "retrieval_mode": "multiple",
                "single_retrieval_config": None,
                "multiple_retrieval_config": {
                    "top_k": 3,
                    "score_threshold": 0.5,
                    "reranking_model": None
                }
            }
        }
    
    def _create_http_request_node(self, node_id: str, title: str) -> Dict:
        """Create an HTTP request node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "http-request",
                "method": "get",
                "url": "https://api.example.com",
                "authorization": {
                    "type": "none",
                    "config": {}
                },
                "headers": "",
                "params": "",
                "body": {
                    "type": "none",
                    "data": ""
                }
            }
        }
    
    def _create_code_node(self, node_id: str, title: str) -> Dict:
        """Create a code node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "code",
                "variables": [],
                "code_language": "python3",
                "code": "def main():\n    return {'result': 'Hello, World!'}\n",
                "outputs": {
                    "result": {
                        "type": "string"
                    }
                }
            }
        }
    
    def _create_template_transform_node(self, node_id: str, title: str) -> Dict:
        """Create a template transform node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "template-transform",
                "variables": [
                    {
                        "variable": "input",
                        "value_selector": ["sys", "query"]
                    }
                ],
                "template": "{{ input }}"
            }
        }
    
    def _create_answer_node(self, node_id: str, title: str) -> Dict:
        """Create an answer node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "answer",
                "answer": "{{#llm.text#}}"
            }
        }
    
    def _create_if_else_node(self, node_id: str, title: str) -> Dict:
        """Create an if-else node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "if-else",
                "condition": {
                    "operator": "==",
                    "left": {
                        "type": "variable",
                        "value_selector": ["sys", "query"]
                    },
                    "right": {
                        "type": "value",
                        "value": ""
                    }
                }
            }
        }
    
    def _create_iteration_node(self, node_id: str, title: str) -> Dict:
        """Create an iteration node."""
        return {
            "id": node_id,
            "position": None,
            "data": {
                "title": title,
                "type": "iteration",
                "iteration_type": "for-each",
                "for_each_config": {
                    "items_variable_selector": ["sys", "query"],
                    "item_variable": "item"
                }
            }
        }
    
    def _generate_features(self, node_types: List[str], language: str) -> Dict:
        """Generate features based on node types."""
        features = {
            "opening_statement": "",
            "suggested_questions": [],
            "suggested_questions_after_answer": [],
            "speech_to_text": False,
            "text_to_speech": False,
            "file_upload": False,
            "sensitive_word_avoidance": False,
            "retriever_resource": {}
        }
        
        # Set features based on node types
        if "knowledge-retrieval" in node_types:
            features["retriever_resource"] = {
                "enabled": True
            }
            
        # Set language-specific features
        if language == "ja":
            features["opening_statement"] = "こんにちは、どのようにお手伝いできますか？"
            features["suggested_questions"] = ["質問例1", "質問例2"]
        else:
            features["opening_statement"] = "Hello, how can I help you today?"
            features["suggested_questions"] = ["Example question 1", "Example question 2"]
            
        return features
