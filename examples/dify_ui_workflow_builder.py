"""
Dify UI Workflow Builder

This module provides a class for building workflows directly in the Dify UI
using browser automation with OpenManus.
"""
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional, List

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent.manus import Manus

class DifyUIWorkflowBuilder:
    """
    A class for building workflows directly in the Dify UI using browser automation.
    """
    
    def __init__(self, manus: Manus):
        """
        Initialize the workflow builder.
        
        Args:
            manus: The Manus agent
        """
        self.manus = manus
        
    async def navigate_to_workflow(self, app_id: str) -> bool:
        """
        Navigate to the workflow page for the specified app.
        
        Args:
            app_id: The app ID
            
        Returns:
            True if navigation was successful, False otherwise
        """
        workflow_url = f"https://cloud.dify.ai/apps/{app_id}/workflows"
        result = await self.manus.available_tools.execute(
            "browser_use",
            action="navigate",
            url=workflow_url
        )
        
        # Wait for page to load
        await asyncio.sleep(2)
        
        # Take a screenshot
        await self.manus.available_tools.execute(
            "browser_use",
            action="screenshot"
        )
        
        return "error" not in result.output.lower()
        
    async def add_node(self, source_node_type: str, target_node_type: str) -> bool:
        """
        Add a node to the workflow.
        
        Args:
            source_node_type: The type of the source node
            target_node_type: The type of the node to add
            
        Returns:
            True if the node was added successfully, False otherwise
        """
        # Find the source node and click its plus button
        js_click_plus = f"""
        // Find the source node
        const sourceNode = document.querySelector('[data-type="{source_node_type}"]');
        if (!sourceNode) {{
            return "Source node not found";
        }}
        
        // Find the plus button on the source node
        const plusButton = sourceNode.querySelector('.plus-button') || 
                           sourceNode.querySelector('[class*="plus"]') ||
                           sourceNode.querySelector('[class*="add"]');
        if (!plusButton) {{
            return "Plus button not found on source node";
        }}
        
        // Click the plus button
        plusButton.click();
        
        return "Clicked plus button on source node";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_click_plus
        )
        
        if "not found" in js_result.output:
            return False
            
        # Wait for block selector to appear
        await asyncio.sleep(1)
        
        # Select the target node type from block selector
        js_select_node = f"""
        // Find the node option in the block selector
        const nodeOption = Array.from(document.querySelectorAll('[class*="block-item"]')).find(
            el => el.textContent.includes('{target_node_type}')
        );
        
        if (!nodeOption) {{
            return "{target_node_type} option not found";
        }}
        
        // Click the node option
        nodeOption.click();
        
        return "Selected {target_node_type} node";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_select_node
        )
        
        # Wait for node to be added
        await asyncio.sleep(1)
        
        return "not found" not in js_result.output
        
    async def configure_node(self, node_type: str, config: Dict[str, Any]) -> bool:
        """
        Configure a node in the workflow.
        
        Args:
            node_type: The type of the node to configure
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Click the node to open configuration panel
        js_click_node = f"""
        // Find the node
        const node = document.querySelector('[data-type="{node_type}"]');
        if (!node) {{
            return "{node_type} node not found";
        }}
        
        // Click the node
        node.click();
        
        return "Clicked {node_type} node for configuration";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_click_node
        )
        
        if "not found" in js_result.output:
            return False
            
        # Wait for configuration panel to open
        await asyncio.sleep(1)
        
        # Apply configuration based on node type
        if node_type == "llm":
            return await self._configure_llm_node(config)
        elif node_type == "knowledge-retrieval":
            return await self._configure_knowledge_retrieval_node(config)
        elif node_type == "answer":
            return await self._configure_answer_node(config)
        elif node_type == "code":
            return await self._configure_code_node(config)
        elif node_type == "if-else":
            return await self._configure_if_else_node(config)
        elif node_type == "template-transform":
            return await self._configure_template_transform_node(config)
        else:
            # Generic configuration for other node types
            return await self._configure_generic_node(node_type, config)
            
    async def _configure_llm_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure an LLM node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        if "prompt" in config:
            js_set_prompt = f"""
            // Find the prompt textarea
            const promptTextarea = document.querySelector('textarea[placeholder*="prompt"]') || 
                                  document.querySelector('textarea[class*="prompt"]');
            
            if (!promptTextarea) {{
                return "Prompt textarea not found";
            }}
            
            // Set the prompt text
            promptTextarea.value = `{config["prompt"]}`;
            
            // Trigger input event to ensure the value is registered
            promptTextarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Added prompt to LLM node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_prompt
            )
            
            if "not found" in js_result.output:
                return False
        
        # Configure model if specified
        if "model" in config:
            js_set_model = f"""
            // Find the model selector
            const modelSelector = document.querySelector('select[name*="model"]') || 
                                 document.querySelector('[class*="model-selector"]');
            
            if (!modelSelector) {{
                return "Model selector not found";
            }}
            
            // Set the model
            modelSelector.value = "{config["model"]}";
            modelSelector.dispatchEvent(new Event('change', {{ bubbles: true }}));
            
            return "Set model for LLM node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_model
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_knowledge_retrieval_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure a Knowledge Retrieval node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Set knowledge base if specified
        if "knowledge_base" in config:
            js_set_kb = f"""
            // Find the knowledge base selector
            const kbSelector = document.querySelector('select[name*="knowledge_base"]') || 
                              document.querySelector('[class*="kb-selector"]');
            
            if (!kbSelector) {{
                return "Knowledge base selector not found";
            }}
            
            // Set the knowledge base
            kbSelector.value = "{config["knowledge_base"]}";
            kbSelector.dispatchEvent(new Event('change', {{ bubbles: true }}));
            
            return "Set knowledge base for Knowledge Retrieval node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_kb
            )
            
            if "not found" in js_result.output:
                return False
        
        # Set top k if specified
        if "top_k" in config:
            js_set_top_k = f"""
            // Find the top k input
            const topKInput = document.querySelector('input[name*="top_k"]') || 
                             document.querySelector('[class*="top-k"]');
            
            if (!topKInput) {{
                return "Top k input not found";
            }}
            
            // Set the top k
            topKInput.value = "{config["top_k"]}";
            topKInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Set top k for Knowledge Retrieval node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_top_k
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_answer_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure an Answer node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Set answer variable if specified
        if "variable" in config:
            js_set_variable = f"""
            // Find the variable input
            const variableInput = document.querySelector('input[name*="variable"]') || 
                                 document.querySelector('[class*="variable-input"]');
            
            if (!variableInput) {{
                return "Variable input not found";
            }}
            
            // Set the variable
            variableInput.value = "{config["variable"]}";
            variableInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Set variable for Answer node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_variable
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_code_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure a Code node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Set code if specified
        if "code" in config:
            js_set_code = f"""
            // Find the code editor
            const codeEditor = document.querySelector('[class*="code-editor"]') || 
                              document.querySelector('textarea[class*="code"]');
            
            if (!codeEditor) {{
                return "Code editor not found";
            }}
            
            // Set the code
            codeEditor.value = `{config["code"]}`;
            codeEditor.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Set code for Code node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_code
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_if_else_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure an If-Else node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Set condition if specified
        if "condition" in config:
            js_set_condition = f"""
            // Find the condition input
            const conditionInput = document.querySelector('input[name*="condition"]') || 
                                  document.querySelector('[class*="condition-input"]');
            
            if (!conditionInput) {{
                return "Condition input not found";
            }}
            
            // Set the condition
            conditionInput.value = "{config["condition"]}";
            conditionInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Set condition for If-Else node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_condition
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_template_transform_node(self, config: Dict[str, Any]) -> bool:
        """
        Configure a Template Transform node.
        
        Args:
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # Set template if specified
        if "template" in config:
            js_set_template = f"""
            // Find the template textarea
            const templateTextarea = document.querySelector('textarea[name*="template"]') || 
                                    document.querySelector('[class*="template-input"]');
            
            if (!templateTextarea) {{
                return "Template textarea not found";
            }}
            
            // Set the template
            templateTextarea.value = `{config["template"]}`;
            templateTextarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            return "Set template for Template Transform node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_template
            )
            
            if "not found" in js_result.output:
                return False
        
        return True
        
    async def _configure_generic_node(self, node_type: str, config: Dict[str, Any]) -> bool:
        """
        Generic configuration for node types without specific configuration methods.
        
        Args:
            node_type: The type of the node to configure
            config: The configuration to apply
            
        Returns:
            True if the node was configured successfully, False otherwise
        """
        # For each key-value pair in config, try to find a matching input and set its value
        for key, value in config.items():
            js_set_value = f"""
            // Find an input with a name or class containing the key
            const input = document.querySelector(`input[name*="{key}"]`) || 
                         document.querySelector(`textarea[name*="{key}"]`) || 
                         document.querySelector(`select[name*="{key}"]`) || 
                         document.querySelector(`[class*="{key}-input"]`);
            
            if (!input) {{
                return "{key} input not found for {node_type} node";
            }}
            
            // Set the value based on input type
            if (input.tagName === 'SELECT') {{
                input.value = "{value}";
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else if (input.tagName === 'TEXTAREA') {{
                input.value = `{value}`;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }} else {{
                input.value = "{value}";
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
            
            return "Set {key} for {node_type} node";
            """
            
            js_result = await self.manus.available_tools.execute(
                "browser_use",
                action="execute_js",
                script=js_set_value
            )
            
            if "not found" in js_result.output:
                print(f"Warning: Could not set {key} for {node_type} node")
        
        return True
        
    async def save_workflow(self) -> bool:
        """
        Save the workflow.
        
        Returns:
            True if the workflow was saved successfully, False otherwise
        """
        js_save_workflow = """
        // Find the save button
        const saveButton = Array.from(document.querySelectorAll('button')).find(
            el => el.textContent.includes('Save') && !el.textContent.includes('Publish')
        );
        
        if (!saveButton) {
            return "Save button not found";
        }
        
        // Click the save button
        saveButton.click();
        
        return "Clicked save button";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_save_workflow
        )
        
        # Wait for save to complete
        await asyncio.sleep(2)
        
        return "not found" not in js_result.output
        
    async def publish_workflow(self) -> bool:
        """
        Publish the workflow.
        
        Returns:
            True if the workflow was published successfully, False otherwise
        """
        js_publish_workflow = """
        // Find the publish button
        const publishButton = Array.from(document.querySelectorAll('button')).find(
            el => el.textContent.includes('Publish')
        );
        
        if (!publishButton) {
            return "Publish button not found";
        }
        
        // Click the publish button
        publishButton.click();
        
        return "Clicked publish button";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_publish_workflow
        )
        
        if "not found" in js_result.output:
            return False
            
        # Wait for confirmation dialog
        await asyncio.sleep(1)
        
        # Confirm publish
        js_confirm_publish = """
        // Find the confirm button in the dialog
        const confirmButton = Array.from(document.querySelectorAll('button')).find(
            el => el.textContent.includes('Confirm') || el.textContent.includes('Yes')
        );
        
        if (!confirmButton) {
            return "Confirm button not found";
        }
        
        // Click the confirm button
        confirmButton.click();
        
        return "Clicked confirm button";
        """
        
        js_result = await self.manus.available_tools.execute(
            "browser_use",
            action="execute_js",
            script=js_confirm_publish
        )
        
        # Wait for publish to complete
        await asyncio.sleep(2)
        
        return "not found" not in js_result.output
        
    async def take_screenshot(self) -> None:
        """
        Take a screenshot of the current state.
        """
        await self.manus.available_tools.execute(
            "browser_use",
            action="screenshot"
        )
        
    async def retry_operation(self, operation, max_retries: int = 3, **kwargs) -> bool:
        """
        Retry an operation multiple times.
        
        Args:
            operation: The async function to retry
            max_retries: Maximum number of retry attempts
            **kwargs: Arguments to pass to the operation
            
        Returns:
            True if the operation succeeded, False otherwise
        """
        for attempt in range(max_retries):
            try:
                result = await operation(**kwargs)
                if result:
                    return True
                print(f"Operation failed, attempt {attempt + 1}/{max_retries}")
                await asyncio.sleep(1)  # Wait before retrying
            except Exception as e:
                print(f"Error during operation: {str(e)}, attempt {attempt + 1}/{max_retries}")
                await asyncio.sleep(1)  # Wait before retrying
        
        return False


async def create_customer_support_workflow(manus: Manus, app_id: str):
    """
    Create a customer support workflow directly in the Dify UI.
    
    Args:
        manus: The Manus agent
        app_id: The app ID for the workflow
    """
    builder = DifyUIWorkflowBuilder(manus)
    
    # Navigate to workflow page
    print("Navigating to workflow page...")
    if not await builder.navigate_to_workflow(app_id):
        print("Failed to navigate to workflow page")
        return
    
    # Add LLM node after Start node
    print("Adding LLM node...")
    if not await builder.add_node("start", "LLM"):
        print("Failed to add LLM node")
        return
    
    # Configure LLM node
    print("Configuring LLM node...")
    llm_config = {
        "prompt": "You are a customer support assistant. Help the user with their product questions and issues."
    }
    if not await builder.configure_node("llm", llm_config):
        print("Failed to configure LLM node")
        return
    
    # Add Knowledge Retrieval node after Start node
    print("Adding Knowledge Retrieval node...")
    if not await builder.add_node("start", "Knowledge Retrieval"):
        print("Failed to add Knowledge Retrieval node")
        return
    
    # Add Answer node after LLM node
    print("Adding Answer node...")
    if not await builder.add_node("llm", "Answer"):
        print("Failed to add Answer node")
        return
    
    # Save the workflow
    print("Saving workflow...")
    if not await builder.save_workflow():
        print("Failed to save workflow")
        return
    
    # Take a screenshot of the completed workflow
    await builder.take_screenshot()
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Workflow Created] Customer Support Assistant")
    print("Nodes: Start → Knowledge Retrieval → LLM → Answer")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

async def run_dify_ui_workflow_builder_example():
    """
    Demonstrate the DifyUIWorkflowBuilder by creating a customer support workflow.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration] Dify UI Workflow Builder")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Initialize Manus agent
    manus = Manus()
    
    # Initialize the browser
    print("Initializing browser...")
    # Initialize browser directly without requiring LLM calls
    await manus.available_tools.execute(
        "browser_use",
        action="initialize"
    )
    print("Browser initialized successfully")
    
    # Navigate to Dify signin page
    signin_url = "https://cloud.dify.ai/signin"
    print(f"Navigating to Dify signin page: {signin_url}")
    result = await manus.available_tools.execute(
        "browser_use",
        action="navigate",
        url=signin_url
    )
    print(f"Navigation result: {result.output}")
    
    # Take a screenshot to show the signin page
    await manus.available_tools.execute(
        "browser_use",
        action="screenshot"
    )
    print("Captured screenshot of signin page")
    
    # Wait for user to sign in
    print("\nPlease sign in to Dify manually. Press Enter when signed in...")
    input()
    
    # Create a customer support workflow
    app_id = input("Enter the app ID from the URL (e.g., 12345-abcd-67890): ")
    await create_customer_support_workflow(manus, app_id)
    
    # Clean up browser resources
    await manus.available_tools.get_tool("browser_use").cleanup()
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Demonstration Complete]")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(run_dify_ui_workflow_builder_example())
