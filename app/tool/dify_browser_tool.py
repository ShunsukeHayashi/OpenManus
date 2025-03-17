import asyncio
from typing import Optional

from app.tool.browser_use_tool import BrowserUseTool
from app.tool.base import ToolResult


class DifyBrowserTool(BrowserUseTool):
    """Specialized browser tool for Dify application automation."""
    
    name: str = "dify_browser"
    description: str = "Browser automation tool specialized for Dify application creation."
    
    async def create_dify_app(
        self,
        app_name: str,
        app_description: str,
        app_mode: str = "chat",
        chat_type: str = "basic"
    ) -> ToolResult:
        """
        Create a Dify application using browser automation.
        
        Args:
            app_name: Name of the application
            app_description: Description of the application
            app_mode: Application mode (chat, completion, agent-chat, workflow)
            chat_type: For chat mode, the type (basic or advanced)
        """
        try:
            # Navigate to Dify apps page
            await self.execute(action="navigate", url="http://localhost/apps")
            
            # Take screenshot of initial state
            screenshot_result = await self.execute(action="screenshot")
            
            # Click "Create from Blank" button (devinid="20")
            await self.execute(action="execute_js", script="""
                const elements = Array.from(document.querySelectorAll('[devinid="20"]'));
                if (elements.length > 0) {
                    elements[0].click();
                    return true;
                }
                return false;
            """)
            
            # Wait for modal to appear
            await asyncio.sleep(1)
            
            # Take screenshot after clicking create button
            screenshot_result = await self.execute(action="screenshot")
            
            # Select app mode
            mode_index_map = {
                "chat": 0,
                "completion": 1,
                "agent-chat": 2,
                "workflow": 3
            }
            
            mode_index = mode_index_map.get(app_mode, 0)
            
            # Click on the app mode option
            await self.execute(action="execute_js", script=f"""
                const modeElements = Array.from(document.querySelectorAll('.flex > div[class*="relative grow box-border"]'));
                if (modeElements.length > {mode_index}) {{
                    modeElements[{mode_index}].click();
                    return true;
                }}
                return false;
            """)
            
            # If chat mode, select chat type
            if app_mode == "chat":
                type_index = 0 if chat_type == "basic" else 1
                
                # Click on the chat type option
                await self.execute(action="execute_js", script=f"""
                    const typeElements = Array.from(document.querySelectorAll('.flex.gap-2 > div[class*="relative grow"]'));
                    if (typeElements.length > {type_index}) {{
                        typeElements[{type_index}].click();
                        return true;
                    }}
                    return false;
                """)
            
            # Take screenshot after selecting app type
            screenshot_result = await self.execute(action="screenshot")
            
            # Click on app icon to open emoji picker
            await self.execute(action="execute_js", script="""
                const iconElement = document.querySelector('.flex.items-center.justify-between.space-x-2 > div');
                if (iconElement) {
                    iconElement.click();
                    return true;
                }
                return false;
            """)
            
            # Wait for emoji picker to appear
            await asyncio.sleep(1)
            
            # Select first emoji (default)
            await self.execute(action="execute_js", script="""
                const emojiElement = document.querySelector('.emoji-mart-emoji');
                if (emojiElement) {
                    emojiElement.click();
                    return true;
                }
                return false;
            """)
            
            # Enter app name
            await self.execute(action="execute_js", script=f"""
                const nameInput = document.querySelector('input[placeholder*="app name"]');
                if (nameInput) {{
                    nameInput.value = "{app_name}";
                    nameInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            """)
            
            # Enter app description
            await self.execute(action="execute_js", script=f"""
                const descInput = document.querySelector('textarea[placeholder*="description"]');
                if (descInput) {{
                    descInput.value = "{app_description}";
                    descInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            """)
            
            # Take screenshot after entering app details
            screenshot_result = await self.execute(action="screenshot")
            
            # Click Create button
            await self.execute(action="execute_js", script="""
                const createButton = Array.from(document.querySelectorAll('button')).find(
                    button => button.textContent.includes('Create')
                );
                if (createButton) {
                    createButton.click();
                    return true;
                }
                return false;
            """)
            
            # Wait for app creation to complete
            await asyncio.sleep(3)
            
            # Take final screenshot
            screenshot_result = await self.execute(action="screenshot")
            
            return ToolResult(output=f"Successfully created Dify application: {app_name}")
            
        except Exception as e:
            return ToolResult(error=f"Failed to create Dify application: {str(e)}")
