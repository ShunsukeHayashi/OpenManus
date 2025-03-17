"""
Test Browser Automation Scripts

This script tests the browser automation scripts for Dify UI workflow creation.
"""
import asyncio
import os
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.dify_ui_direct_workflow_creation import run_dify_ui_direct_workflow_creation
from examples.dify_ui_workflow_builder import run_dify_ui_workflow_builder_example
from examples.japanese_dify_ui_workflow_creation import run_japanese_dify_ui_workflow_creation

async def test_browser_automation():
    """Test the browser automation scripts."""
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Testing] Dify UI Browser Automation")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Ask which script to test
    print("Which browser automation script would you like to test?")
    print("1. Direct Workflow Creation (English)")
    print("2. Workflow Builder Example (English)")
    print("3. Japanese Workflow Creation")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        # Run the direct workflow creation script
        await run_dify_ui_direct_workflow_creation()
    elif choice == "2":
        # Run the workflow builder example
        await run_dify_ui_workflow_builder_example()
    elif choice == "3":
        # Run the Japanese workflow creation example
        await run_japanese_dify_ui_workflow_creation()
    else:
        print("Invalid choice. Please run the script again and select a valid option.")
        return
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("[Test Complete] Browser automation successful")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")

if __name__ == "__main__":
    asyncio.run(test_browser_automation())
