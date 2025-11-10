# ================================================================================
# FILE 3: tools/basic_tools.py
# ================================================================================
"""
Basic CSV manipulation tools.
"""
import pandas as pd
from smolagents import tool


@tool
def read_csv(file_path: str, n: int = 5) -> str:
    """
    Reads a CSV file and returns its first few rows.

    Args:
        file_path: Path to the CSV file.
        n: Number of rows to display (default: 5).

    Returns:
        The first few rows of the dataframe as a string.
    """
    df = pd.read_csv(file_path)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    return str(df.head(n))


@tool
def get_csv_info(file_path: str) -> str:
    """
    Returns comprehensive info about the CSV file including shape, columns, dtypes, and missing values.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Detailed CSV information including row count, column count, data types, and null counts.
    """
    df = pd.read_csv(file_path)
    
    info_str = f"""
CSV File Information:
=====================
Total Rows: {len(df)}
Total Columns: {len(df.columns)}

Column Details:
---------------
"""
    for idx, col in enumerate(df.columns):
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        dtype = df[col].dtype
        info_str += f"{idx}. {col}: {non_null}/{len(df)} non-null ({null_count} missing), dtype: {dtype}\n"
    
    info_str += f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB"
    
    return info_str


@tool
def get_column_names(file_path: str) -> str:
    """
    Returns just the column names from the CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        List of column names as a comma-separated string.
    """
    df = pd.read_csv(file_path)
    return f"Columns ({len(df.columns)}): {', '.join(df.columns.tolist())}"


@tool
def append_to_csv(file_path: str, data: dict) -> str:
    """
    Appends a dictionary as a new row to a CSV file.

    Args:
        file_path: Path to the CSV file.
        data: Key-value pairs corresponding to columns and values.

    Returns:
        Confirmation message after appending.
    """
    df = pd.DataFrame([data])
    df.to_csv(file_path, mode="a", header=False, index=False)
    return f"✅ Data appended successfully to {file_path}"


@tool
def search_csv(file_path: str, column: str, value: str, n: int = 5) -> str:
    """
    Searches for rows where a given column matches a value.

    Args:
        file_path: Path to the CSV file.
        column: Column name to search in.
        value: Value to match.
        n: Number of matching rows to return.

    Returns:
        Matching rows as a string with count information.
    """
    df = pd.read_csv(file_path)
    if column not in df.columns:
        return f"❌ Column '{column}' not found in CSV. Available columns: {', '.join(df.columns)}"
    
    matches = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    
    if matches.empty:
        return "⚠️ No matching records found."
    
    result_df = matches.head(n).reset_index(drop=True)
    
    with pd.option_context('display.max_columns', None, 
                          'display.width', 1000,
                          'display.max_colwidth', 40):
        output = f"Found {len(matches)} matching rows. Showing first {len(result_df)}:\n\n{str(result_df)}"
    
    return output


@tool
def describe_csv(file_path: str) -> str:
    """
    Returns a statistical summary of numeric columns in the CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Summary statistics for all numeric columns.
    """
    df = pd.read_csv(file_path)
    with pd.option_context('display.max_columns', None,
                          'display.width', 1000):
        return str(df.describe())