# ================================================================================
# FILE: enhanced_csv_agent_v2.py
# ================================================================================
"""
Enhanced CSV Agent V2 with DataFrame returns, 3-step limit, and final_answer() function.
This agent automatically includes data structure information and uses try-catch blocks.
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
import pandas as pd

# Global agent instance
_enhanced_agent_v2 = None


def final_answer(result):
    """
    Final answer function that handles the result and provides comprehensive output.
    
    Args:
        result: The result from the agent's operation (DataFrame or other)
    
    Returns:
        str: Formatted final answer
    """
    if isinstance(result, pd.DataFrame):
        if len(result) == 0:
            return "No data found matching your criteria."
        
        # Format DataFrame for display
        with pd.option_context('display.max_columns', None, 
                              'display.width', 1000,
                              'display.max_colwidth', 50):
            formatted_result = str(result)
        
        return f"Here are the results:\n\n{formatted_result}"
    else:
        return str(result)


def create_enhanced_csv_agent_v2():
    """
    Creates and returns a configured CSV manipulation agent V2 with DataFrame returns.
    This agent automatically includes df.info() and df.describe() information
    and uses try-catch blocks with final_answer() function.
    
    Returns:
        CodeAgent: Configured agent with enhanced CSV tools and DataFrame returns.
    """
    # Initialize the model
    model = LiteLLMModel(
        model_id=config.MODEL_ID,
        api_key=config.MODEL_API_KEY
    )
    
    # Create agent with enhanced tools and necessary permissions
    agent = CodeAgent(
        tools=[
            # Enhanced tools with DataFrame returns
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
    
    # Enhanced system instruction for V2
    agent.system_instruction = """
You are an enhanced CSV manipulation agent V2 with DataFrame returns and comprehensive analysis capabilities.

IMPORTANT CODING GUIDELINES:
- ALL TOOLS NOW RETURN PANDAS DATAFRAMES INSTEAD OF STRINGS
- Use try-catch blocks in EVERY step with final_answer() function
- Maximum 3 steps allowed - be efficient and comprehensive
- Always wrap your main operation in try-catch blocks

QUERY TYPE DETECTION AND RESPONSE STRATEGY:

1. COMPREHENSIVE ANALYSIS QUESTIONS (e.g., "What's the mean age of all passengers?"):
   Step 1: Data exploration using enhanced_read_csv() or enhanced_get_csv_info()
   Step 2: Perform the analysis/computation (calculate mean, provide insights)
   Step 3: Use final_answer() with comprehensive string explanation

2. DATAFRAME REQUESTS (e.g., "Show me passengers over 30", "Create a new CSV"):
   Step 1: Perform the operation and get DataFrame result
   Step 2: Use final_answer() with the DataFrame directly
   Step 3: (Optional) Additional analysis if needed

CODING PATTERN FOR EACH STEP:
try:
    # Your analysis code here
    result = your_analysis_function()
    final_answer(result)
except Exception as e:
    print(f"Error in step: {e}")
    # Continue to next step

ENHANCED CAPABILITIES:
- Automatic data structure inspection (df.info() and df.describe())
- Comprehensive data context for accurate code generation
- Error prevention through data type awareness
- Enhanced tools provide better integration and context
- All tools return DataFrames for better data handling

Remember: 
- Use enhanced tools (enhanced_read_csv, enhanced_get_csv_info, etc.) for better results
- Always use try-catch blocks with final_answer() function
- For statistical questions, provide comprehensive analysis with insights
- For data requests, return the DataFrame directly
- Be efficient within the 3-step limit
- ALL OUTPUT CSV FILES MUST BE SAVED IN THE 'answers' DIRECTORY (same folder as main.py)
- Use config.OUTPUT_DIR for all file output paths
"""
    
    return agent


def get_enhanced_agent_v2():
    """
    Returns the global enhanced agent V2 instance, creating it if necessary.
    
    Returns:
        CodeAgent: The global enhanced CSV manipulation agent V2.
    """
    global _enhanced_agent_v2
    if _enhanced_agent_v2 is None:
        _enhanced_agent_v2 = create_enhanced_csv_agent_v2()
    return _enhanced_agent_v2


def run_with_data_inspection_v2(query: str, file_paths: list = None, max_steps: int = None):
    """
    Enhanced run method V2 that automatically includes df.info() and df.describe() 
    for all CSV files mentioned in the query, with DataFrame returns and try-catch blocks.
    
    Args:
        query: The user's query
        file_paths: Optional list of CSV file paths to inspect
        max_steps: Maximum steps for the agent (default: 3)
    
    Returns:
        str: Agent response with enhanced data context and DataFrame handling
    """
    if max_steps is None:
        max_steps = 3  # Fixed to 3 steps for V2
    
    # Ensure answers directory exists
    import os
    answers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "answers")
    os.makedirs(answers_dir, exist_ok=True)
    
    agent = get_enhanced_agent_v2()
    
    # Enhanced query with automatic data inspection
    enhanced_query = _enhance_query_with_data_inspection_v2(query, file_paths)
    
    return agent.run(enhanced_query, max_steps=max_steps)


def _enhance_query_with_data_inspection_v2(query: str, file_paths: list = None):
    """
    Enhances a query by automatically adding df.info() and df.describe() 
    information for better code generation accuracy in V2.
    
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
    data_context = "\n\n=== AUTOMATIC DATA INSPECTION V2 ===\n"
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
    
    data_context += "=== END DATA INSPECTION V2 ===\n"
    data_context += "Use this information to write accurate code. Pay special attention to:\n"
    data_context += "- Column names and data types\n"
    data_context += "- Null value counts\n"
    data_context += "- Unique values in categorical columns\n"
    data_context += "- Numeric ranges and statistics\n\n"
    data_context += "IMPORTANT CODING GUIDELINES FOR V2:\n"
    data_context += "- ALL TOOLS NOW RETURN PANDAS DATAFRAMES\n"
    data_context += "- Use try-catch blocks in EVERY step with final_answer() function\n"
    data_context += "- Maximum 3 steps allowed - be efficient\n"
    data_context += "- For comprehensive questions, provide detailed analysis in step 2\n"
    data_context += "- For DataFrame requests, provide DataFrame in step 1\n"
    data_context += "- Always use enhanced tools for better results\n\n"
    
    return query + data_context
