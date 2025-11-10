# ================================================================================
# FILE 3: tools/basic_tools.py
# ================================================================================
"""
Basic CSV manipulation tools.
"""
import pandas as pd
from smolagents import tool


@tool
def read_csv(file_path: str, n: int = 5) -> pd.DataFrame:
    """
    Reads a CSV file and returns its first few rows.

    Args:
        file_path: Path to the CSV file.
        n: Number of rows to display (default: 5).

    Returns:
        The first few rows of the dataframe as a pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df.head(n)


@tool
def get_csv_info(file_path: str) -> pd.DataFrame:
    """
    Returns comprehensive info about the CSV file including shape, columns, dtypes, and missing values.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Detailed CSV information as a DataFrame with column details.
    """
    df = pd.read_csv(file_path)
    
    # Create info DataFrame
    info_data = []
    for idx, col in enumerate(df.columns):
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        dtype = df[col].dtype
        info_data.append({
            'Column': col,
            'Non_Null': non_null,
            'Total_Rows': len(df),
            'Missing': null_count,
            'Data_Type': str(dtype)
        })
    
    info_df = pd.DataFrame(info_data)
    info_df['Memory_Usage_KB'] = df.memory_usage(deep=True).sum() / 1024
    
    return info_df


@tool
def get_column_names(file_path: str) -> pd.DataFrame:
    """
    Returns just the column names from the CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame with column names and their indices.
    """
    df = pd.read_csv(file_path)
    columns_df = pd.DataFrame({
        'Index': range(len(df.columns)),
        'Column_Name': df.columns.tolist()
    })
    return columns_df


@tool
def append_to_csv(file_path: str, data: dict) -> pd.DataFrame:
    """
    Appends a dictionary as a new row to a CSV file.

    Args:
        file_path: Path to the CSV file.
        data: Key-value pairs corresponding to columns and values.

    Returns:
        DataFrame showing the appended data.
    """
    df = pd.DataFrame([data])
    df.to_csv(file_path, mode="a", header=False, index=False)
    return df


@tool
def search_csv(file_path: str, column: str, value: str, n: int = 5) -> pd.DataFrame:
    """
    Searches for rows where a given column matches a value.

    Args:
        file_path: Path to the CSV file.
        column: Column name to search in.
        value: Value to match.
        n: Number of matching rows to return.

    Returns:
        DataFrame with matching rows.
    """
    df = pd.read_csv(file_path)
    if column not in df.columns:
        # Return error info as DataFrame
        error_df = pd.DataFrame({
            'Error': [f"Column '{column}' not found"],
            'Available_Columns': [', '.join(df.columns)]
        })
        return error_df
    
    matches = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    
    if matches.empty:
        # Return empty DataFrame with info
        empty_df = pd.DataFrame({'Message': ['No matching records found']})
        return empty_df
    
    return matches.head(n).reset_index(drop=True)


@tool
def describe_csv(file_path: str) -> pd.DataFrame:
    """
    Returns a statistical summary of numeric columns in the CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Summary statistics DataFrame for all numeric columns.
    """
    df = pd.read_csv(file_path)
    return df.describe()