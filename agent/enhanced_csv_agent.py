# ================================================================================
# FILE: enhanced_csv_agent.py
# ================================================================================
"""
Enhanced CSV Agent with automatic df.info() and df.describe() placeholders.
This agent automatically includes data structure information to improve code generation accuracy.
"""
from smolagents import CodeAgent, LiteLLMModel
from tools import (
    read_csv, get_csv_info, get_column_names, append_to_csv, 
    search_csv, describe_csv, create_csv_with_columns, 
    join_csv_files, filter_and_save_csv, combine_csv_files, 
    delete_csv_file
)
from tools.enhanced_tools import (
    enhanced_read_csv, enhanced_get_csv_info, enhanced_search_csv,
    enhanced_describe_csv, enhanced_create_csv_with_columns,
    enhanced_join_csv_files, enhanced_filter_and_save_csv,
    enhanced_combine_csv_files
)
import config

# Global agent instance
_enhanced_agent = None


def create_enhanced_csv_agent():
    """
    Creates and returns a configured CSV manipulation agent with enhanced prompts.
    This agent automatically includes df.info() and df.describe() information
    to improve code generation accuracy.
    
    Returns:
        CodeAgent: Configured agent with enhanced CSV tools and automatic data inspection.
    """
    # Initialize the model
    model = LiteLLMModel(
        model_id=config.MODEL_ID,
        api_key=config.MODEL_API_KEY
    )
    
    # Create agent with enhanced tools and necessary permissions
    agent = CodeAgent(
        tools=[
            # Enhanced tools with automatic df.info() and df.describe()
            enhanced_read_csv, enhanced_get_csv_info, get_column_names, 
            append_to_csv, enhanced_search_csv, enhanced_describe_csv,
            # Enhanced advanced tools
            enhanced_create_csv_with_columns, enhanced_join_csv_files, 
            enhanced_filter_and_save_csv, enhanced_combine_csv_files, delete_csv_file
        ],
        model=model,
        add_base_tools=config.ADD_BASE_TOOLS,
        # Allow necessary imports for CSV operations
        additional_authorized_imports=[
            'pandas', 'os', 'csv', 'json', 'pathlib', 'shutil', 'glob'
        ]
    )
    
    # Add system instruction to minimize imports
    agent.system_instruction = """
You are an enhanced CSV manipulation agent with automatic data structure inspection capabilities.

IMPORTANT CODING GUIDELINES:
- AVOID UNNECESSARY IMPORTS - Use the provided enhanced tools instead of direct pandas operations
- Prefer enhanced tools (enhanced_read_csv, enhanced_get_csv_info, etc.) over direct pandas imports
- Only import modules when absolutely necessary for the specific task
- The enhanced tools automatically provide df.info() and df.describe() context
- Use the available CSV manipulation tools rather than writing custom pandas code
- Focus on using the tool functions rather than importing pandas directly

ENHANCED CAPABILITIES:
- Automatic data structure inspection (df.info() and df.describe())
- Comprehensive data context for accurate code generation
- Error prevention through data type awareness
- Enhanced tools provide better integration and context

Remember: The enhanced tools are designed to provide all necessary functionality without requiring additional imports.
"""
    
    return agent


def get_enhanced_agent():
    """
    Returns the global enhanced agent instance, creating it if necessary.
    
    Returns:
        CodeAgent: The global enhanced CSV manipulation agent.
    """
    global _enhanced_agent
    if _enhanced_agent is None:
        _enhanced_agent = create_enhanced_csv_agent()
    return _enhanced_agent


def run_with_data_inspection(query: str, file_paths: list = None, max_steps: int = None):
    """
    Enhanced run method that automatically includes df.info() and df.describe() 
    for all CSV files mentioned in the query.
    
    Args:
        query: The user's query
        file_paths: Optional list of CSV file paths to inspect
        max_steps: Maximum steps for the agent
    
    Returns:
        str: Agent response with enhanced data context
    """
    if max_steps is None:
        max_steps = config.MAX_STEPS
    
    agent = get_enhanced_agent()
    
    # Enhanced query with automatic data inspection
    enhanced_query = _enhance_query_with_data_inspection(query, file_paths)
    
    return agent.run(enhanced_query, max_steps=max_steps)


def _enhance_query_with_data_inspection(query: str, file_paths: list = None):
    """
    Enhances a query by automatically adding df.info() and df.describe() 
    information for better code generation accuracy.
    
    Args:
        query: Original user query
        file_paths: List of CSV file paths to inspect
    
    Returns:
        str: Enhanced query with data inspection information
    """
    import pandas as pd
    import os
    
    # Default file paths if none provided
    if file_paths is None:
        file_paths = [config.TRAIN_CSV, config.TEST_CSV]
    
    # Filter to only existing CSV files
    existing_files = [f for f in file_paths if os.path.exists(f)]
    
    if not existing_files:
        return query
    
    # Build data inspection information
    data_context = "\n\n=== AUTOMATIC DATA INSPECTION ===\n"
    data_context += "The following information is automatically provided to improve code generation accuracy:\n\n"
    
    for file_path in existing_files:
        try:
            df = pd.read_csv(file_path)
            filename = os.path.basename(file_path)
            
            data_context += f"📊 DATA STRUCTURE FOR {filename}:\n"
            data_context += f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            data_context += f"Columns: {', '.join(df.columns.tolist())}\n"
            data_context += f"Data types:\n"
            
            for col in df.columns:
                dtype = df[col].dtype
                null_count = df[col].isna().sum()
                data_context += f"  - {col}: {dtype} ({null_count} null values)\n"
            
            # Add unique values for categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                data_context += f"\nCategorical column unique values:\n"
                for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                    unique_vals = df[col].dropna().unique()[:10]  # First 10 unique values
                    data_context += f"  - {col}: {list(unique_vals)}\n"
            
            # Add statistical summary for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                data_context += f"\nNumeric column statistics:\n"
                numeric_summary = df[numeric_cols].describe()
                data_context += f"{numeric_summary}\n"
            
            data_context += "\n" + "="*50 + "\n\n"
            
        except Exception as e:
            data_context += f"⚠️ Could not inspect {file_path}: {str(e)}\n\n"
    
    data_context += "=== END DATA INSPECTION ===\n"
    data_context += "Use this information to write accurate code. Pay special attention to:\n"
    data_context += "- Column names and data types\n"
    data_context += "- Null value counts\n"
    data_context += "- Unique values in categorical columns\n"
    data_context += "- Numeric ranges and statistics\n\n"
    data_context += "IMPORTANT CODING GUIDELINES:\n"
    data_context += "- Avoid unnecessary imports - use the provided tools instead\n"
    data_context += "- Prefer using the available CSV manipulation tools over direct pandas operations\n"
    data_context += "- Only import modules when absolutely necessary for the specific task\n"
    data_context += "- Use the enhanced tools (enhanced_read_csv, enhanced_get_csv_info, etc.) for better results\n\n"
    
    return query + data_context
