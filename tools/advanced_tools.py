# ================================================================================
# FILE 4: tools/advanced_tools.py
# ================================================================================
"""
Advanced CSV manipulation tools.
"""
import pandas as pd
import os
from smolagents import tool


@tool
def create_csv_with_columns(source_file: str, output_file: str, columns: list) -> pd.DataFrame:
    """
    Creates a new CSV file with only selected columns from the source file.

    Args:
        source_file: Path to the source CSV file.
        output_file: Path where the new CSV file will be saved.
        columns: List of column names to include in the new file.

    Returns:
        DataFrame with the selected columns.
    
    Example:
        create_csv_with_columns("data.csv", "output.csv", ["Name", "Age"])
    """
    try:
        df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            error_df = pd.DataFrame({
                'Error': [f"Columns not found: {', '.join(missing_cols)}"],
                'Available_Columns': [', '.join(df.columns)]
            })
            return error_df
        
        # Create new dataframe with selected columns
        new_df = df[columns]
        
        # Save to new file
        new_df.to_csv(output_file, index=False)
        
        return new_df
    
    except Exception as e:
        error_df = pd.DataFrame({'Error': [f"Error creating CSV: {str(e)}"]})
        return error_df


@tool
def join_csv_files(file1: str, file2: str, output_file: str, join_column: str, join_type: str = "inner") -> pd.DataFrame:
    """
    Joins two CSV files on a common column and saves the result.

    Args:
        file1: Path to the first CSV file.
        file2: Path to the second CSV file.
        output_file: Path where the joined CSV will be saved.
        join_column: Column name to join on (must exist in both files).
        join_type: Type of join - "inner", "left", "right", or "outer" (default: "inner").

    Returns:
        DataFrame with the joined data.
    
    Example:
        join_csv_files("customers.csv", "orders.csv", "result.csv", "customer_id", "left")
    """
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Validate join column exists in both files
        if join_column not in df1.columns:
            error_df = pd.DataFrame({
                'Error': [f"Column '{join_column}' not found in {file1}"],
                'Available_Columns': [', '.join(df1.columns)]
            })
            return error_df
        
        if join_column not in df2.columns:
            error_df = pd.DataFrame({
                'Error': [f"Column '{join_column}' not found in {file2}"],
                'Available_Columns': [', '.join(df2.columns)]
            })
            return error_df
        
        # Validate join type
        valid_joins = ["inner", "left", "right", "outer"]
        if join_type not in valid_joins:
            error_df = pd.DataFrame({
                'Error': [f"Invalid join type '{join_type}'"],
                'Valid_Options': [', '.join(valid_joins)]
            })
            return error_df
        
        # Perform the join
        joined_df = pd.merge(df1, df2, on=join_column, how=join_type, suffixes=('_file1', '_file2'))
        
        # Save to output file
        joined_df.to_csv(output_file, index=False)
        
        return joined_df
    
    except Exception as e:
        error_df = pd.DataFrame({'Error': [f"Error joining CSV files: {str(e)}"]})
        return error_df


@tool
def filter_and_save_csv(file_path: str, output_file: str, column: str, value: str, comparison: str = "contains") -> pd.DataFrame:
    """
    Filters rows from a CSV file based on a condition and saves to a new file.

    Args:
        file_path: Path to the source CSV file.
        output_file: Path where the filtered CSV will be saved.
        column: Column name to filter on.
        value: Value to compare against.
        comparison: Type of comparison - "equals", "contains", "greater_than", "less_than" (default: "contains").

    Returns:
        DataFrame with filtered data.
    
    Example:
        filter_and_save_csv("data.csv", "filtered.csv", "Age", "30", "greater_than")
    """
    try:
        df = pd.read_csv(file_path)
        
        if column not in df.columns:
            error_df = pd.DataFrame({
                'Error': [f"Column '{column}' not found"],
                'Available_Columns': [', '.join(df.columns)]
            })
            return error_df
        
        # Apply filter based on comparison type
        if comparison == "equals":
            filtered_df = df[df[column].astype(str) == value]
        elif comparison == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif comparison == "greater_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') > float(value)]
            except ValueError:
                error_df = pd.DataFrame({
                    'Error': [f"Cannot compare '{value}' as number"],
                    'Column_Type': [str(df[column].dtype)]
                })
                return error_df
        elif comparison == "less_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') < float(value)]
            except ValueError:
                error_df = pd.DataFrame({
                    'Error': [f"Cannot compare '{value}' as number"],
                    'Column_Type': [str(df[column].dtype)]
                })
                return error_df
        else:
            error_df = pd.DataFrame({
                'Error': [f"Invalid comparison type '{comparison}'"],
                'Valid_Options': ["equals, contains, greater_than, less_than"]
            })
            return error_df
        
        # Save filtered data
        filtered_df.to_csv(output_file, index=False)
        
        return filtered_df
    
    except Exception as e:
        error_df = pd.DataFrame({'Error': [f"Error filtering CSV: {str(e)}"]})
        return error_df


@tool
def combine_csv_files(file_list: list, output_file: str, ignore_index: bool = True, keep_only_common: bool = True) -> pd.DataFrame:
    """
    Combines multiple CSV files vertically (stacks them) into one file.
    By default, keeps only columns that exist in ALL files.

    Args:
        file_list: List of CSV file paths to combine.
        output_file: Path where the combined CSV will be saved.
        ignore_index: Whether to reset index in the combined file (default: True).
        keep_only_common: If True, keeps only common columns. If False, keeps all columns and fills missing with NaN (default: True).

    Returns:
        DataFrame with combined data.
    
    Example:
        combine_csv_files(["data1.csv", "data2.csv"], "combined.csv")
    """
    try:
        if len(file_list) < 2:
            error_df = pd.DataFrame({'Error': ["Please provide at least 2 CSV files to combine"]})
            return error_df
        
        dfs = []
        all_columns = []
        
        for file_path in file_list:
            if not os.path.exists(file_path):
                error_df = pd.DataFrame({'Error': [f"File not found: {file_path}"]})
                return error_df
            df = pd.read_csv(file_path)
            dfs.append(df)
            all_columns.append(set(df.columns))
        
        # Check if all dataframes have the same columns
        columns_match = all(cols == all_columns[0] for cols in all_columns[1:])
        
        if not columns_match:
            if keep_only_common:
                # Find common columns across all files
                common_cols = set.intersection(*all_columns)
                
                if not common_cols:
                    error_df = pd.DataFrame({'Error': ["No common columns found across all files"]})
                    return error_df
                
                # Keep only common columns in order from first file
                common_cols_ordered = [col for col in dfs[0].columns if col in common_cols]
                
                # Filter each dataframe to only keep common columns
                dfs_filtered = [df[common_cols_ordered] for df in dfs]
                
                # Combine filtered dataframes
                combined_df = pd.concat(dfs_filtered, ignore_index=ignore_index)
                
            else:
                # Keep all columns, fill missing with NaN
                combined_df = pd.concat(dfs, ignore_index=ignore_index, sort=False)
        else:
            # All files have same columns, simple concatenation
            combined_df = pd.concat(dfs, ignore_index=ignore_index)
        
        # Save to output file
        combined_df.to_csv(output_file, index=False)
        
        return combined_df
    
    except Exception as e:
        error_df = pd.DataFrame({'Error': [f"Error combining CSV files: {str(e)}"]})
        return error_df


@tool
def delete_csv_file(file_path: str) -> pd.DataFrame:
    """
    Deletes a CSV file from the filesystem.

    Args:
        file_path: Path to the CSV file to delete.

    Returns:
        DataFrame with deletion status.
    """
    try:
        if not os.path.exists(file_path):
            error_df = pd.DataFrame({'Error': [f"File not found: {file_path}"]})
            return error_df
        
        os.remove(file_path)
        success_df = pd.DataFrame({'Status': ["Successfully deleted"], 'File': [file_path]})
        return success_df
    
    except Exception as e:
        error_df = pd.DataFrame({'Error': [f"Error deleting file: {str(e)}"]})
        return error_df
