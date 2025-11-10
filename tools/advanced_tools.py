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
def create_csv_with_columns(source_file: str, output_file: str, columns: list) -> str:
    """
    Creates a new CSV file with only selected columns from the source file.

    Args:
        source_file: Path to the source CSV file.
        output_file: Path where the new CSV file will be saved.
        columns: List of column names to include in the new file.

    Returns:
        Confirmation message with details about the new file.
    
    Example:
        create_csv_with_columns("data.csv", "output.csv", ["Name", "Age"])
    """
    try:
        df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"❌ Columns not found in source file: {', '.join(missing_cols)}\nAvailable columns: {', '.join(df.columns)}"
        
        # Create new dataframe with selected columns
        new_df = df[columns]
        
        # Save to new file
        new_df.to_csv(output_file, index=False)
        
        return f"✅ Created new CSV file: {output_file}\n" \
               f"   Rows: {len(new_df)}\n" \
               f"   Columns: {', '.join(columns)}\n" \
               f"   File saved successfully!"
    
    except Exception as e:
        return f"❌ Error creating CSV: {str(e)}"


@tool
def join_csv_files(file1: str, file2: str, output_file: str, join_column: str, join_type: str = "inner") -> str:
    """
    Joins two CSV files on a common column and saves the result.

    Args:
        file1: Path to the first CSV file.
        file2: Path to the second CSV file.
        output_file: Path where the joined CSV will be saved.
        join_column: Column name to join on (must exist in both files).
        join_type: Type of join - "inner", "left", "right", or "outer" (default: "inner").

    Returns:
        Confirmation message with details about the joined file.
    
    Example:
        join_csv_files("customers.csv", "orders.csv", "result.csv", "customer_id", "left")
    """
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Validate join column exists in both files
        if join_column not in df1.columns:
            return f"❌ Column '{join_column}' not found in {file1}\nAvailable columns: {', '.join(df1.columns)}"
        
        if join_column not in df2.columns:
            return f"❌ Column '{join_column}' not found in {file2}\nAvailable columns: {', '.join(df2.columns)}"
        
        # Validate join type
        valid_joins = ["inner", "left", "right", "outer"]
        if join_type not in valid_joins:
            return f"❌ Invalid join type '{join_type}'. Valid options: {', '.join(valid_joins)}"
        
        # Perform the join
        joined_df = pd.merge(df1, df2, on=join_column, how=join_type, suffixes=('_file1', '_file2'))
        
        # Save to output file
        joined_df.to_csv(output_file, index=False)
        
        return f"✅ Successfully joined CSV files!\n" \
               f"   File 1: {os.path.basename(file1)} ({len(df1)} rows, {len(df1.columns)} columns)\n" \
               f"   File 2: {os.path.basename(file2)} ({len(df2)} rows, {len(df2.columns)} columns)\n" \
               f"   Join Type: {join_type}\n" \
               f"   Join Column: {join_column}\n" \
               f"   Result: {output_file} ({len(joined_df)} rows, {len(joined_df.columns)} columns)\n" \
               f"   File saved successfully!"
    
    except Exception as e:
        return f"❌ Error joining CSV files: {str(e)}"


@tool
def filter_and_save_csv(file_path: str, output_file: str, column: str, value: str, comparison: str = "contains") -> str:
    """
    Filters rows from a CSV file based on a condition and saves to a new file.

    Args:
        file_path: Path to the source CSV file.
        output_file: Path where the filtered CSV will be saved.
        column: Column name to filter on.
        value: Value to compare against.
        comparison: Type of comparison - "equals", "contains", "greater_than", "less_than" (default: "contains").

    Returns:
        Confirmation message with filter details.
    
    Example:
        filter_and_save_csv("data.csv", "filtered.csv", "Age", "30", "greater_than")
    """
    try:
        df = pd.read_csv(file_path)
        
        if column not in df.columns:
            return f"❌ Column '{column}' not found in source file.\nAvailable columns: {', '.join(df.columns)}"
        
        # Apply filter based on comparison type
        if comparison == "equals":
            filtered_df = df[df[column].astype(str) == value]
        elif comparison == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif comparison == "greater_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') > float(value)]
            except ValueError:
                return f"❌ Cannot compare '{value}' as number. Column might not be numeric."
        elif comparison == "less_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') < float(value)]
            except ValueError:
                return f"❌ Cannot compare '{value}' as number. Column might not be numeric."
        else:
            return f"❌ Invalid comparison type '{comparison}'. Valid options: equals, contains, greater_than, less_than"
        
        # Save filtered data
        filtered_df.to_csv(output_file, index=False)
        
        return f"✅ Filtered CSV created successfully!\n" \
               f"   Source: {os.path.basename(file_path)} ({len(df)} rows)\n" \
               f"   Filter: {column} {comparison} '{value}'\n" \
               f"   Result: {output_file} ({len(filtered_df)} rows)\n" \
               f"   File saved successfully!"
    
    except Exception as e:
        return f"❌ Error filtering CSV: {str(e)}"


@tool
def combine_csv_files(file_list: list, output_file: str, ignore_index: bool = True, keep_only_common: bool = True) -> str:
    """
    Combines multiple CSV files vertically (stacks them) into one file.
    By default, keeps only columns that exist in ALL files.

    Args:
        file_list: List of CSV file paths to combine.
        output_file: Path where the combined CSV will be saved.
        ignore_index: Whether to reset index in the combined file (default: True).
        keep_only_common: If True, keeps only common columns. If False, keeps all columns and fills missing with NaN (default: True).

    Returns:
        Confirmation message with combination details.
    
    Example:
        combine_csv_files(["data1.csv", "data2.csv"], "combined.csv")
    """
    try:
        if len(file_list) < 2:
            return "❌ Please provide at least 2 CSV files to combine."
        
        dfs = []
        all_columns = []
        
        for file_path in file_list:
            if not os.path.exists(file_path):
                return f"❌ File not found: {file_path}"
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
                    return "❌ No common columns found across all files. Cannot combine."
                
                # Keep only common columns in order from first file
                common_cols_ordered = [col for col in dfs[0].columns if col in common_cols]
                
                # Filter each dataframe to only keep common columns
                dfs_filtered = [df[common_cols_ordered] for df in dfs]
                
                # Combine filtered dataframes
                combined_df = pd.concat(dfs_filtered, ignore_index=ignore_index)
                
                # Build info about dropped columns
                dropped_info = []
                for i, (df, file_path) in enumerate(zip(dfs, file_list)):
                    dropped = set(df.columns) - common_cols
                    if dropped:
                        dropped_info.append(f"   File {i+1} ({os.path.basename(file_path)}): {', '.join(sorted(dropped))}")
                
                dropped_msg = ""
                if dropped_info:
                    dropped_msg = f"\n   🗑️  Dropped columns:\n" + "\n".join(dropped_info)
                
            else:
                # Keep all columns, fill missing with NaN
                combined_df = pd.concat(dfs, ignore_index=ignore_index, sort=False)
                dropped_msg = "\n   ⚠️  Note: Files had different columns. Missing values filled with NaN."
        else:
            # All files have same columns, simple concatenation
            combined_df = pd.concat(dfs, ignore_index=ignore_index)
            dropped_msg = ""
        
        # Save to output file
        combined_df.to_csv(output_file, index=False)
        
        files_info = "\n".join([f"   - {os.path.basename(f)} ({len(df)} rows, {len(df.columns)} cols)" 
                                for f, df in zip(file_list, dfs)])
        
        return f"✅ Successfully combined {len(file_list)} CSV files!\n" \
               f"   Files combined:\n{files_info}\n" \
               f"   Result: {output_file} ({len(combined_df)} rows, {len(combined_df.columns)} columns){dropped_msg}\n" \
               f"   File saved successfully!"
    
    except Exception as e:
        return f"❌ Error combining CSV files: {str(e)}"


@tool
def delete_csv_file(file_path: str) -> str:
    """
    Deletes a CSV file from the filesystem.

    Args:
        file_path: Path to the CSV file to delete.

    Returns:
        Confirmation message.
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        os.remove(file_path)
        return f"✅ Successfully deleted: {file_path}"
    
    except Exception as e:
        return f"❌ Error deleting file: {str(e)}"
