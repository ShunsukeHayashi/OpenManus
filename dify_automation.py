from typing import Dict
import asyncio
import time

from app.agent.base import BaseAgent
from app.agent.manus import Manus
from app.flow.base import FlowType
from app.flow.flow_factory import FlowFactory
from app.logger import logger


async def create_dify_app(app_name="OpenManus Demo App", 
                         app_description="Created by OpenManus automation", 
                         app_mode="chat", 
                         chat_type="basic"):
    """
    Automate the creation of a Dify application using browser automation.
    
    Args:
        app_name: Name of the application to create
        app_description: Description of the application
        app_mode: Application mode (chat, completion, agent-chat, workflow)
        chat_type: For chat mode, the type (basic or advanced)
    """
    # Create Manus agent with browser automation capabilities
    agents: Dict[str, BaseAgent] = {
        "manus": Manus(),
    }
    
    # Create a planning flow for structured task execution
    flow = FlowFactory.create_flow(
        flow_type=FlowType.PLANNING,
        agents=agents,
        plan_id=f"dify_app_creation_{int(time.time())}",
    )
    
    # Define the automation steps based on app_mode
    steps = [
        "Navigate to Dify application creation page",
        "Click 'Create from Blank' button",
        f"Select app mode: {app_mode}",
    ]
    
    # Add chat type selection step if app_mode is chat
    if app_mode == "chat":
        steps.append(f"Select chat type: {chat_type}")
    
    # Add remaining steps
    steps.extend([
        "Set app icon, name, and description",
        "Click 'Create' button",
        "Verify app creation success"
    ])
    
    # Create the initial plan with the defined steps
    await flow.planning_tool.execute(
        command="create",
        plan_id=flow.active_plan_id,
        title=f"Create Dify App: {app_name}",
        steps=steps
    )
    
    # Define the automation prompt with app details
    prompt = f"""
    Create a new Dify application with the following details:
    - Name: {app_name}
    - Description: {app_description}
    - Mode: {app_mode}
    - Chat Type (if applicable): {chat_type}
    
    Follow these steps:
    1. Navigate to http://localhost/apps
    2. Click the 'Create from Blank' button (devinid="20")
    3. Select the app mode: {app_mode}
    4. If chat mode, select type: {chat_type}
    5. Set app icon, name, and description
    6. Click 'Create' button
    7. Verify the app was created successfully
    
    Use browser automation to complete these steps and capture screenshots at each stage.
    """
    
    # Execute the flow with the defined prompt
    try:
        logger.warning("Starting Dify application creation automation...")
        result = await flow.execute(prompt)
        logger.info("Automation completed successfully")
        logger.info(result)
        return True
    except Exception as e:
        logger.error(f"Error during automation: {str(e)}")
        return False


async def main():
    """Main function to run the Dify automation demo."""
    try:
        # Get user input for app details
        print("\n=== Dify Application Creation Automation ===")
        app_name = input("Enter app name (default: OpenManus Demo App): ") or "OpenManus Demo App"
        app_description = input("Enter app description (default: Created by OpenManus automation): ") or "Created by OpenManus automation"
        
        # App mode selection
        print("\nSelect app mode:")
        print("1. Chat (default)")
        print("2. Completion")
        print("3. Agent-chat")
        print("4. Workflow")
        mode_choice = input("Enter choice (1-4): ") or "1"
        
        app_mode_map = {
            "1": "chat",
            "2": "completion",
            "3": "agent-chat",
            "4": "workflow"
        }
        
        app_mode = app_mode_map.get(mode_choice, "chat")
        
        # Chat type selection if app_mode is chat
        chat_type = "basic"
        if app_mode == "chat":
            print("\nSelect chat type:")
            print("1. Basic (default)")
            print("2. Advanced")
            type_choice = input("Enter choice (1-2): ") or "1"
            
            chat_type_map = {
                "1": "basic",
                "2": "advanced-chat"
            }
            
            chat_type = chat_type_map.get(type_choice, "basic")
        
        # Run the automation
        print(f"\nCreating Dify app: {app_name} ({app_mode})")
        success = await create_dify_app(app_name, app_description, app_mode, chat_type)
        
        if success:
            print("\n✅ Dify application created successfully!")
        else:
            print("\n❌ Failed to create Dify application.")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
