# ================================================================================
# FILE: dynamic_prompt_template.py
# ================================================================================
"""
Dynamic prompt template that automatically includes df.info() and df.describe()
for the dataset being used, making the agent aware of the actual data structure.
"""
import pandas as pd
import os
from typing import List, Dict, Any

def create_dynamic_prompt_template(user_query: str, dataset_paths: List[str] = None) -> str:
    """
    Creates a dynamic prompt template that includes comprehensive dataset information.
    
    Args:
        user_query: The user's original query
        dataset_paths: List of CSV file paths to analyze (default: train.csv and test.csv)
    
    Returns:
        str: Enhanced prompt with dataset metadata
    """
    if dataset_paths is None:
        # Default to train.csv and test.csv in the parent directory
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_paths = [
            os.path.join(parent_dir, "train.csv"),
            os.path.join(parent_dir, "test.csv")
        ]
    
    # Filter to only existing files
    existing_files = [f for f in dataset_paths if os.path.exists(f)]
    
    if not existing_files:
        return user_query
    
    # Build comprehensive dataset information
    dataset_info = "\n\n" + "="*80 + "\n"
    dataset_info += "DYNAMIC DATASET INFORMATION TEMPLATE\n"
    dataset_info += "="*80 + "\n"
    dataset_info += "The following information is automatically provided to ensure accurate data manipulation:\n\n"
    
    for file_path in existing_files:
        try:
            df = pd.read_csv(file_path)
            filename = os.path.basename(file_path)
            
            dataset_info += f"DATASET: {filename}\n"
            dataset_info += f"{'='*50}\n"
            
            # Basic information
            dataset_info += f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            dataset_info += f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB\n\n"
            
            # df.info() equivalent
            dataset_info += "COLUMN INFORMATION (df.info() equivalent):\n"
            dataset_info += f"{'Index':<5} {'Column':<15} {'Non-Null Count':<15} {'Dtype':<10} {'Null Count':<10}\n"
            dataset_info += "-" * 70 + "\n"
            
            for idx, col in enumerate(df.columns):
                non_null = df[col].count()
                null_count = df[col].isna().sum()
                dtype = df[col].dtype
                dataset_info += f"{idx:<5} {col:<15} {non_null:<15} {str(dtype):<10} {null_count:<10}\n"
            
            dataset_info += "\n"
            
            # df.describe() for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                dataset_info += "STATISTICAL SUMMARY (df.describe() for numeric columns):\n"
                describe_df = df[numeric_cols].describe()
                dataset_info += str(describe_df) + "\n\n"
            
            # Categorical columns analysis
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                dataset_info += "CATEGORICAL COLUMNS ANALYSIS:\n"
                for col in categorical_cols:
                    unique_count = df[col].nunique()
                    null_count = df[col].isna().sum()
                    most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                    dataset_info += f"  {col}: {unique_count} unique values, {null_count} nulls, most common: '{most_common}'\n"
                    if unique_count <= 10:  # Show all values if 10 or fewer
                        unique_vals = df[col].dropna().unique()
                        dataset_info += f"    Values: {list(unique_vals)}\n"
                dataset_info += "\n"
            
            # Data type summary
            dataset_info += "DATA TYPES SUMMARY:\n"
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                dataset_info += f"  {dtype}: {count} columns\n"
            
            # Sample data preview
            dataset_info += f"\nSAMPLE DATA (first 3 rows):\n"
            sample_df = df.head(3)
            dataset_info += str(sample_df) + "\n"
            
            dataset_info += "\n" + "="*50 + "\n\n"
            
        except Exception as e:
            dataset_info += f"WARNING: Error analyzing {file_path}: {str(e)}\n\n"
    
    # Add important guidelines
    dataset_info += "IMPORTANT GUIDELINES BASED ON ACTUAL DATA:\n"
    dataset_info += "- Use the exact column names as shown above\n"
    dataset_info += "- Pay attention to data types (numeric vs object)\n"
    dataset_info += "- Check for null values before operations\n"
    dataset_info += "- Use appropriate comparison methods based on data types\n"
    dataset_info += "- For numeric columns, use numeric comparisons\n"
    dataset_info += "- For object columns, use string comparisons\n"
    dataset_info += "- All CSV output files must be saved in the 'answers' directory\n"
    dataset_info += "- Use config.OUTPUT_DIR for all file output paths\n\n"
    
    dataset_info += "OPERATIONAL GUIDELINES:\n"
    dataset_info += "- Use the available CSV manipulation tools as needed\n"
    dataset_info += "- Focus on the task requirements rather than specific tool names\n"
    dataset_info += "- Let the system choose the most appropriate tools\n"
    dataset_info += "- All operations should be data-driven based on the structure above\n\n"
    
    dataset_info += "="*80 + "\n"
    dataset_info += "END DYNAMIC DATASET INFORMATION\n"
    dataset_info += "="*80 + "\n"
    
    return user_query + dataset_info


def create_simple_dataset_info(user_query: str, dataset_path: str) -> str:
    """
    Creates a simpler dataset info template for a single dataset.
    
    Args:
        user_query: The user's original query
        dataset_path: Path to the CSV file to analyze
    
    Returns:
        str: Enhanced prompt with dataset metadata
    """
    if not os.path.exists(dataset_path):
        return user_query
    
    try:
        df = pd.read_csv(dataset_path)
        filename = os.path.basename(dataset_path)
        
        dataset_info = f"\n\nDATASET INFO FOR {filename}:\n"
        dataset_info += f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
        dataset_info += f"Columns: {', '.join(df.columns.tolist())}\n"
        dataset_info += f"Data Types: {dict(df.dtypes)}\n"
        dataset_info += f"Null Counts: {dict(df.isnull().sum())}\n"
        
        # Add describe for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            dataset_info += f"\nNumeric Columns Statistics:\n{df[numeric_cols].describe()}\n"
        
        # Add categorical info
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            dataset_info += f"\nCategorical Columns:\n"
            for col in categorical_cols:
                unique_vals = df[col].dropna().unique()[:5]  # First 5 unique values
                dataset_info += f"  {col}: {list(unique_vals)}\n"
        
        dataset_info += f"\nSample Data:\n{df.head(2)}\n"
        
        return user_query + dataset_info
        
    except Exception as e:
        return user_query + f"\n\nWARNING: Error analyzing dataset: {str(e)}\n"


def detect_datasets_in_query(query: str) -> List[str]:
    """
    Detect which datasets are mentioned in the query.
    
    Args:
        query: The user's query
    
    Returns:
        List[str]: List of dataset file paths mentioned in the query
    """
    import re
    
    # Common dataset patterns
    dataset_patterns = [
        r'train\.csv',
        r'test\.csv', 
        r'\.csv',
        r'train',
        r'test'
    ]
    
    detected_files = []
    query_lower = query.lower()
    
    # Check for specific file mentions
    for pattern in dataset_patterns:
        if re.search(pattern, query_lower):
            # Get parent directory
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            if 'train' in pattern or 'train' in query_lower:
                train_path = os.path.join(parent_dir, "train.csv")
                if os.path.exists(train_path) and train_path not in detected_files:
                    detected_files.append(train_path)
            
            if 'test' in pattern or 'test' in query_lower:
                test_path = os.path.join(parent_dir, "test.csv")
                if os.path.exists(test_path) and test_path not in detected_files:
                    detected_files.append(test_path)
    
    # If no specific datasets detected, use defaults
    if not detected_files:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_files = [
            os.path.join(parent_dir, "train.csv"),
            os.path.join(parent_dir, "test.csv")
        ]
        detected_files = [f for f in default_files if os.path.exists(f)]
    
    return detected_files


def create_smart_prompt_template(user_query: str) -> str:
    """
    Creates a smart prompt template that automatically detects relevant datasets.
    
    Args:
        user_query: The user's original query
    
    Returns:
        str: Enhanced prompt with relevant dataset information
    """
    # Detect which datasets are relevant
    relevant_datasets = detect_datasets_in_query(user_query)
    
    if not relevant_datasets:
        return user_query
    
    # Create template with relevant datasets
    return create_dynamic_prompt_template(user_query, relevant_datasets)
