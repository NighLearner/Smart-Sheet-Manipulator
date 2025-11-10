"""
Simple CSV/Excel manipulation agent.
Focuses only on data transformation operations.
"""
from smolagents import CodeAgent, LiteLLMModel
from tools import (
    get_column_names,
    select_columns,
    create_column,
    normalize_column,
    one_hot_encode,
    label_encode,
    filter_rows,
    combine_files,
    join_files,
    # Advanced tools
    standard_scaler,
    min_max_scaler,
    robust_scaler,
    ordinal_encode,
    target_encode,
    frequency_encode,
    binary_encode,
    polynomial_features,
    impute_missing_values,
    handle_outliers
)
import config

# Global agent instance
_agent = None


def create_agent():
    """
    Creates and returns a configured data manipulation agent.
    
    Returns:
        CodeAgent: Configured agent with manipulation tools.
    """
    # Initialize the model
    model = LiteLLMModel(
        model_id=config.MODEL_ID,
        api_key=config.MODEL_API_KEY
    )
    
    # Create agent with manipulation tools
    agent = CodeAgent(
        tools=[
            # Basic manipulation tools
            get_column_names,
            select_columns,
            create_column,
            normalize_column,
            one_hot_encode,
            label_encode,
            filter_rows,
            combine_files,
            join_files,
            # Advanced tools (sklearn-based)
            standard_scaler,
            min_max_scaler,
            robust_scaler,
            ordinal_encode,
            target_encode,
            frequency_encode,
            binary_encode,
            polynomial_features,
            impute_missing_values,
            handle_outliers
        ],
        model=model,
        add_base_tools=config.ADD_BASE_TOOLS,
        # Allow necessary imports for data manipulation
        # Note: sklearn is imported inside the label_encode tool, so we don't need to authorize it here
        additional_authorized_imports=[
            'pandas', 'os', 'numpy', 'sklearn'
        ]
    )
    
    # Set system instruction for data manipulation focus
    agent.system_instruction = """
You are a data manipulation agent focused on transforming CSV and Excel files.

YOUR PURPOSE:
- Perform data transformations (select columns, create columns, normalize, encode, filter, combine, join)
- Save transformed data to new files
- Support both CSV (.csv) and Excel (.xlsx, .xls) files

WHAT YOU DO:
- Select specific columns from files
- Create new columns from existing ones using expressions
- Normalize/standardize numeric columns (multiple methods available)
- Perform various encodings: one-hot, label, ordinal, target, frequency, binary
- Scale features: StandardScaler, MinMaxScaler, RobustScaler
- Handle missing values with imputation
- Handle outliers using IQR or Z-score methods
- Create polynomial features
- Filter rows based on conditions
- Combine multiple files (vertically or horizontally)
- Join files on common columns

WHAT YOU DO NOT DO:
- Do NOT answer analytical queries (e.g., "what is the average age?")
- Do NOT provide statistical summaries for information purposes
- Do NOT perform data analysis or insights
- Focus ONLY on data manipulation and transformation

IMPORTANT:
- Always save results to output files
- Use the provided tools for all operations
- Support both CSV and Excel file formats
- Return clear confirmation messages
"""
    
    return agent


def get_agent():
    """
    Returns the global agent instance, creating it if necessary.
    
    Returns:
        CodeAgent: The global data manipulation agent.
    """
    global _agent
    if _agent is None:
        _agent = create_agent()
    return _agent
