"""
Utility functions for metadata injection in queries.
"""
import pandas as pd
import os
import re
from pathlib import Path


def get_file_metadata(file_path: str) -> str:
    """
    Gets comprehensive metadata (df.info() equivalent) for a CSV or Excel file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        String with file metadata including shape, columns, types, and statistics
    """
    try:
        # Read file
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        # Build metadata string
        metadata = f"\n=== FILE METADATA: {os.path.basename(file_path)} ===\n"
        metadata += f"File Path: {file_path}\n"
        metadata += f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
        metadata += f"Columns: {', '.join(df.columns.tolist())}\n\n"
        metadata += "Column Details:\n"
        metadata += "-" * 50 + "\n"
        
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isna().sum()
            non_null = df[col].count()
            total_rows = len(df)
            
            metadata += f"Column: {col}\n"
            metadata += f"  Data Type: {dtype}\n"
            metadata += f"  Non-null Count: {non_null}/{total_rows}\n"
            metadata += f"  Null Count: {null_count}\n"
            
            # Add type-specific information
            if pd.api.types.is_numeric_dtype(df[col]):
                metadata += f"  Min: {df[col].min()}\n"
                metadata += f"  Max: {df[col].max()}\n"
                metadata += f"  Mean: {df[col].mean():.2f}\n"
                metadata += f"  Std: {df[col].std():.2f}\n"
            elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
                unique_count = df[col].nunique()
                metadata += f"  Unique Values: {unique_count}\n"
                if unique_count <= 20:
                    unique_vals = df[col].dropna().unique()[:20]
                    metadata += f"  Sample Values: {list(unique_vals)}\n"
                else:
                    unique_vals = df[col].dropna().unique()[:10]
                    metadata += f"  Sample Values (first 10): {list(unique_vals)}\n"
            
            metadata += "\n"
        
        metadata += "=" * 50 + "\n"
        return metadata
    
    except Exception as e:
        return f"Error reading metadata for {file_path}: {str(e)}\n"


def extract_file_paths_from_query(query: str) -> list:
    """
    Extracts file paths from a query string.
    
    Args:
        query: Query string that may contain file paths
        
    Returns:
        List of file paths found in the query
    """
    file_paths = []
    
    # Patterns to match file paths (handles both Windows and Unix paths)
    # Match paths like: file.csv, folder/file.csv, folder\file.csv, C:\path\file.csv, /path/file.csv
    patterns = [
        r'[^\s"\']+\.csv',
        r'[^\s"\']+\.xlsx',
        r'[^\s"\']+\.xls'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        file_paths.extend(matches)
    
    # Remove duplicates and clean paths
    file_paths = list(set(file_paths))
    
    # Filter and resolve paths
    existing_paths = []
    for path in file_paths:
        # Clean the path (remove quotes if present)
        path = path.strip('"\'').strip()
        
        # Skip if it's not a valid file path
        if not (path.endswith('.csv') or path.endswith('.xlsx') or path.endswith('.xls')):
            continue
        
        # Try different path resolutions
        resolved_path = None
        
        # Try as-is (absolute path or relative to current directory)
        if os.path.exists(path):
            resolved_path = os.path.abspath(path)
        else:
            # Try relative to current directory
            current_dir = os.getcwd()
            full_path = os.path.join(current_dir, path)
            if os.path.exists(full_path):
                resolved_path = os.path.abspath(full_path)
            else:
                # Try relative to app directory
                app_dir = Path(__file__).resolve().parent.parent
                full_path = app_dir / path
                if full_path.exists():
                    resolved_path = str(full_path.resolve())
                else:
                    # Try with path normalization (handle Windows/Unix path separators)
                    normalized_path = os.path.normpath(path)
                    if os.path.exists(normalized_path):
                        resolved_path = os.path.abspath(normalized_path)
        
        if resolved_path and resolved_path not in existing_paths:
            existing_paths.append(resolved_path)
    
    return existing_paths


def enhance_query_with_metadata(query: str, file_paths: list = None, auto_detect: bool = True) -> str:
    """
    Enhances a query by adding file metadata before the actual query.
    
    Args:
        query: Original user query
        file_paths: List of file paths to include metadata for (optional)
        auto_detect: Whether to auto-detect file paths from query (default: True)
        
    Returns:
        Enhanced query with metadata
    """
    # Auto-detect file paths if not provided and auto_detect is True
    if file_paths is None and auto_detect:
        file_paths = extract_file_paths_from_query(query)
    
    # If no file paths found, return original query
    if not file_paths:
        return query
    
    # Build enhanced query with metadata
    enhanced_query = "FILE METADATA INFORMATION:\n"
    enhanced_query += "=" * 70 + "\n"
    enhanced_query += "The following metadata is provided to help you understand the data structure:\n\n"
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            enhanced_query += get_file_metadata(file_path)
            enhanced_query += "\n"
    
    enhanced_query += "=" * 70 + "\n"
    enhanced_query += "USER QUERY:\n"
    enhanced_query += "=" * 70 + "\n"
    enhanced_query += query
    enhanced_query += "\n\n"
    enhanced_query += "INSTRUCTIONS:\n"
    enhanced_query += "- Use the metadata information above to perform the operation accurately.\n"
    enhanced_query += "- Pay attention to column names (case-sensitive), data types, and null values.\n"
    enhanced_query += "- Ensure output file paths are correct and directories exist.\n"
    enhanced_query += "-" * 70 + "\n"
    
    return enhanced_query

