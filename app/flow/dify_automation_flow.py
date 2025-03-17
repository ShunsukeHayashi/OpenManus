from typing import Dict, List, Optional, Union

from pydantic import Field

from app.agent.base import BaseAgent
from app.flow.planning import PlanningFlow
from app.logger import logger


class DifyAutomationFlow(PlanningFlow):
    """A flow specialized for automating Dify application creation."""
    
    dify_url: str = Field(default="http://localhost/apps")
    app_name: str = Field(default="OpenManus Demo App")
    app_description: str = Field(default="Created by OpenManus automation")
    app_mode: str = Field(default="chat")
    chat_type: str = Field(default="basic")
    
    def __init__(
        self, 
        agents: Union[BaseAgent, List[BaseAgent], Dict[str, BaseAgent]], 
        **data
    ):
        super().__init__(agents, **data)
    
    async def _create_initial_plan(self, request: str) -> None:
        """Create an initial plan for Dify automation."""
        logger.info(f"Creating Dify automation plan with ID: {self.active_plan_id}")
        
        # Define steps based on app_mode
        steps = [
            "[BROWSER] Navigate to Dify application page",
            "[BROWSER] Click 'Create from Blank' button",
            f"[BROWSER] Select app mode: {self.app_mode}",
        ]
        
        # Add chat type selection step if app_mode is chat
        if self.app_mode == "chat":
            steps.append(f"[BROWSER] Select chat type: {self.chat_type}")
        
        # Add remaining steps
        steps.extend([
            "[BROWSER] Set app icon",
            "[BROWSER] Enter app name and description",
            "[BROWSER] Click 'Create' button",
            "[BROWSER] Verify app creation success"
        ])
        
        # Create the plan using the planning tool
        await self.planning_tool.execute(
            command="create",
            plan_id=self.active_plan_id,
            title=f"Create Dify App: {self.app_name}",
            steps=steps
        )
