# ================================================================================
# FILE 6: agent/csv_agent.py
# ================================================================================
"""
CSV Agent setup and configuration.
"""
from smolagents import CodeAgent, LiteLLMModel
from tools import (
    read_csv, get_csv_info, get_column_names, append_to_csv, 
    search_csv, describe_csv, create_csv_with_columns, 
    join_csv_files, filter_and_save_csv, combine_csv_files, 
    delete_csv_file
)
import config

# Global agent instance
_agent = None


def create_csv_agent():
    """
    Creates and returns a configured CSV manipulation agent.
    
    Returns:
        CodeAgent: Configured agent with all CSV tools.
    """
    # Initialize the model
    model = LiteLLMModel(
        model_id=config.MODEL_ID,
        api_key=config.MODEL_API_KEY
    )
    
    # Create agent with all tools and necessary permissions
    agent = CodeAgent(
        tools=[
            # Basic tools
            read_csv, get_csv_info, get_column_names, 
            append_to_csv, search_csv, describe_csv,
            # Advanced tools
            create_csv_with_columns, join_csv_files, 
            filter_and_save_csv, combine_csv_files, delete_csv_file
        ],
        model=model,
        add_base_tools=config.ADD_BASE_TOOLS,
        # Allow necessary imports for CSV operations
        additional_authorized_imports=[
            'pandas', 'os', 'csv', 'json', 'pathlib', 'shutil', 'glob'
        ]
    )
    
    return agent


def get_agent():
    """
    Returns the global agent instance, creating it if necessary.
    
    Returns:
        CodeAgent: The global CSV manipulation agent.
    """
    global _agent
    if _agent is None:
        _agent = create_csv_agent()
    return _agent