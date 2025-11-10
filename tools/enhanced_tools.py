# ================================================================================
# FILE: enhanced_tools.py
# ================================================================================
"""
Enhanced CSV manipulation tools with automatic df.info() and df.describe() integration.
These tools automatically provide data structure information to improve code generation accuracy.
"""
import pandas as pd
import os
from smolagents import tool


@tool
def enhanced_read_csv(file_path: str, n: int = 5) -> pd.DataFrame:
    """
    Enhanced CSV reader that automatically includes df.info() and df.describe() information.
    This helps the AI agent understand the data structure for better code generation.

    Args:
        file_path: Path to the CSV file.
        n: Number of rows to display (default: 5).

    Returns:
        DataFrame with first few rows plus comprehensive data structure information.
    """
    df = pd.read_csv(file_path)
    
    # Get basic data preview
    data_preview = df.head(n)
    
    # Add metadata as additional columns
    metadata_df = pd.DataFrame({
        'Dataset_Shape': [f"{df.shape[0]} rows × {df.shape[1]} columns"],
        'Memory_Usage_KB': [df.memory_usage(deep=True).sum() / 1024],
        'Data_Types': [str(dict(df.dtypes))],
        'Null_Counts': [str(dict(df.isnull().sum()))]
    })
    
    # Combine preview with metadata
    result_df = pd.concat([data_preview, metadata_df], axis=1)
    
    return result_df


@tool
def enhanced_get_csv_info(file_path: str) -> pd.DataFrame:
    """
    Enhanced CSV info that provides comprehensive data structure analysis.
    This includes df.info() equivalent plus df.describe() for better code generation.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame with detailed CSV information and enhanced data structure analysis.
    """
    df = pd.read_csv(file_path)
    
    # Create comprehensive info DataFrame
    info_data = []
    for idx, col in enumerate(df.columns):
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        dtype = df[col].dtype
        unique_count = df[col].nunique()
        
        # Get most common value for categorical columns
        most_common = "N/A"
        if df[col].dtype == 'object' and not df[col].mode().empty:
            most_common = df[col].mode().iloc[0]
        
        info_data.append({
            'Column': col,
            'Non_Null': non_null,
            'Total_Rows': len(df),
            'Missing': null_count,
            'Data_Type': str(dtype),
            'Unique_Values': unique_count,
            'Most_Common': str(most_common)
        })
    
    info_df = pd.DataFrame(info_data)
    
    # Add dataset-level metadata
    metadata_df = pd.DataFrame({
        'Metric': ['Total_Rows', 'Total_Columns', 'Memory_Usage_KB', 'Numeric_Columns', 'Categorical_Columns'],
        'Value': [
            len(df),
            len(df.columns),
            df.memory_usage(deep=True).sum() / 1024,
            len(df.select_dtypes(include=['number']).columns),
            len(df.select_dtypes(include=['object']).columns)
        ]
    })
    
    return info_df


@tool
def enhanced_search_csv(file_path: str, column: str, value: str, n: int = 5) -> pd.DataFrame:
    """
    Enhanced CSV search that includes data structure context for better filtering.
    Automatically provides df.info() and df.describe() context.

    Args:
        file_path: Path to the CSV file.
        column: Column name to search in.
        value: Value to match.
        n: Number of matching rows to return.

    Returns:
        DataFrame with matching rows plus data structure context.
    """
    df = pd.read_csv(file_path)
    
    if column not in df.columns:
        error_df = pd.DataFrame({
            'Error': [f"Column '{column}' not found"],
            'Available_Columns': [', '.join(df.columns.tolist())],
            'Dataset_Shape': [f"{df.shape[0]} rows × {df.shape[1]} columns"]
        })
        return error_df
    
    # Add column-specific information
    col_dtype = df[column].dtype
    col_nulls = df[column].isna().sum()
    col_unique = df[column].nunique()
    
    # Perform the search
    matches = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    
    if matches.empty:
        empty_df = pd.DataFrame({
            'Message': ['No matching records found'],
            'Column_Type': [str(col_dtype)],
            'Unique_Values': [col_unique],
            'Null_Count': [col_nulls]
        })
        return empty_df
    
    result_df = matches.head(n).reset_index(drop=True)
    
    # Add metadata about the search
    metadata_df = pd.DataFrame({
        'Search_Column': [column],
        'Search_Value': [value],
        'Total_Matches': [len(matches)],
        'Column_Type': [str(col_dtype)],
        'Column_Unique_Values': [col_unique]
    })
    
    # Combine results with metadata
    combined_df = pd.concat([result_df, metadata_df], axis=1)
    
    return combined_df


@tool
def enhanced_describe_csv(file_path: str) -> pd.DataFrame:
    """
    Enhanced CSV description with comprehensive statistical analysis.
    Provides df.describe() plus additional insights for better understanding.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame with enhanced statistical summary and data structure insights.
    """
    df = pd.read_csv(file_path)
    
    # Basic describe() output
    basic_describe = df.describe()
    
    # Enhanced analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Create enhanced summary DataFrame
    enhanced_data = []
    
    # Add numeric column analysis
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            col_info = df[col].describe()
            enhanced_data.append({
                'Column': col,
                'Type': 'Numeric',
                'Mean': col_info['mean'],
                'Std': col_info['std'],
                'Min': col_info['min'],
                'Max': col_info['max'],
                'Count': col_info['count']
            })
    
    # Add categorical column analysis
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            unique_count = df[col].nunique()
            null_count = df[col].isna().sum()
            most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
            enhanced_data.append({
                'Column': col,
                'Type': 'Categorical',
                'Unique_Values': unique_count,
                'Null_Count': null_count,
                'Most_Common': most_common,
                'Count': df[col].count()
            })
    
    enhanced_df = pd.DataFrame(enhanced_data)
    
    # Add missing data analysis
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percentage': [(count / len(df)) * 100 for count in missing_data.values]
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0]
        
        # Combine with enhanced data
        enhanced_df = pd.concat([enhanced_df, missing_df], ignore_index=True)
    
    return enhanced_df


@tool
def enhanced_create_csv_with_columns(source_file: str, output_file: str, columns: list) -> str:
    """
    Enhanced CSV column selection with automatic data structure validation.
    Provides df.info() context to ensure accurate column selection.

    Args:
        source_file: Path to the source CSV file.
        output_file: Path where the new CSV file will be saved.
        columns: List of column names to include in the new file.

    Returns:
        Confirmation message with enhanced data structure validation.
    """
    try:
        df = pd.read_csv(source_file)
        
        # Provide data structure context
        context_info = f"""
=== DATA STRUCTURE VALIDATION ===
📊 Source Dataset: {df.shape[0]} rows × {df.shape[1]} columns
📋 Available columns: {', '.join(df.columns.tolist())}
"""
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"❌ Columns not found in source file: {', '.join(missing_cols)}\n{context_info}"
        
        # Create new dataframe with selected columns
        new_df = df[columns]
        
        # Save to new file
        new_df.to_csv(output_file, index=False)
        
        # Enhanced confirmation with data structure info
        result_info = f"✅ Enhanced CSV file created successfully!\n{context_info}\n"
        result_info += f"📁 Output Details:\n"
        result_info += f"   - File: {output_file}\n"
        result_info += f"   - Rows: {len(new_df)}\n"
        result_info += f"   - Columns: {', '.join(columns)}\n"
        result_info += f"   - Data types: {dict(new_df.dtypes)}\n"
        result_info += f"   - Memory usage: {new_df.memory_usage(deep=True).sum() / 1024:.1f} KB\n"
        result_info += f"   - File saved successfully!"
        
        return result_info
    
    except Exception as e:
        return f"❌ Error creating CSV: {str(e)}"


@tool
def enhanced_join_csv_files(file1: str, file2: str, output_file: str, join_column: str, join_type: str = "inner") -> str:
    """
    Enhanced CSV join with automatic data structure analysis.
    Provides df.info() and df.describe() context for both files.

    Args:
        file1: Path to the first CSV file.
        file2: Path to the second CSV file.
        output_file: Path where the joined CSV will be saved.
        join_column: Column name to join on (must exist in both files).
        join_type: Type of join - "inner", "left", "right", or "outer" (default: "inner").

    Returns:
        Enhanced confirmation with comprehensive data structure analysis.
    """
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Enhanced data structure context
        context_info = f"""
=== ENHANCED JOIN DATA STRUCTURE ANALYSIS ===
📊 File 1 ({file1}): {df1.shape[0]} rows × {df1.shape[1]} columns
   Columns: {', '.join(df1.columns.tolist())}
   Data types: {dict(df1.dtypes)}

📊 File 2 ({file2}): {df2.shape[0]} rows × {df2.shape[1]} columns
   Columns: {', '.join(df2.columns.tolist())}
   Data types: {dict(df2.dtypes)}
"""
        
        # Validate join column exists in both files
        if join_column not in df1.columns:
            return f"❌ Column '{join_column}' not found in {file1}\n{context_info}"
        
        if join_column not in df2.columns:
            return f"❌ Column '{join_column}' not found in {file2}\n{context_info}"
        
        # Validate join type
        valid_joins = ["inner", "left", "right", "outer"]
        if join_type not in valid_joins:
            return f"❌ Invalid join type '{join_type}'. Valid options: {', '.join(valid_joins)}"
        
        # Analyze join column data
        join_analysis = f"\n🔗 Join Column Analysis:\n"
        join_analysis += f"   Column '{join_column}' in File 1: {df1[join_column].dtype}, {df1[join_column].nunique()} unique values\n"
        join_analysis += f"   Column '{join_column}' in File 2: {df2[join_column].dtype}, {df2[join_column].nunique()} unique values\n"
        
        # Perform the join
        joined_df = pd.merge(df1, df2, on=join_column, how=join_type, suffixes=('_file1', '_file2'))
        
        # Save to output file
        joined_df.to_csv(output_file, index=False)
        
        # Enhanced result with comprehensive analysis
        result_info = f"✅ Enhanced CSV join completed successfully!\n{context_info}{join_analysis}\n"
        result_info += f"📁 Join Results:\n"
        result_info += f"   - Join Type: {join_type}\n"
        result_info += f"   - Join Column: {join_column}\n"
        result_info += f"   - Result File: {output_file}\n"
        result_info += f"   - Result Shape: {joined_df.shape[0]} rows × {joined_df.shape[1]} columns\n"
        result_info += f"   - Result Data Types: {dict(joined_df.dtypes)}\n"
        result_info += f"   - Memory Usage: {joined_df.memory_usage(deep=True).sum() / 1024:.1f} KB\n"
        result_info += f"   - File saved successfully!"
        
        return result_info
    
    except Exception as e:
        return f"❌ Error joining CSV files: {str(e)}"


@tool
def enhanced_filter_and_save_csv(file_path: str, output_file: str, column: str, value: str, comparison: str = "contains") -> str:
    """
    Enhanced CSV filtering with automatic data structure validation.
    Provides df.info() and df.describe() context for accurate filtering.

    Args:
        file_path: Path to the source CSV file.
        output_file: Path where the filtered CSV will be saved.
        column: Column name to filter on.
        value: Value to compare against.
        comparison: Type of comparison - "equals", "contains", "greater_than", "less_than" (default: "contains").

    Returns:
        Enhanced confirmation with data structure validation.
    """
    try:
        df = pd.read_csv(file_path)
        
        # Enhanced data structure context
        context_info = f"""
=== ENHANCED FILTER DATA STRUCTURE ANALYSIS ===
📊 Source Dataset: {df.shape[0]} rows × {df.shape[1]} columns
📋 Available columns: {', '.join(df.columns.tolist())}
"""
        
        if column not in df.columns:
            return f"❌ Column '{column}' not found in source file.\n{context_info}"
        
        # Add column-specific analysis
        col_analysis = f"\n🎯 Filter Column Analysis:\n"
        col_analysis += f"   Column '{column}': {df[column].dtype}\n"
        col_analysis += f"   Unique values: {df[column].nunique()}\n"
        col_analysis += f"   Null values: {df[column].isna().sum()}\n"
        
        if df[column].dtype == 'object':
            unique_vals = df[column].dropna().unique()[:10]
            col_analysis += f"   Sample values: {list(unique_vals)}\n"
        else:
            col_stats = df[column].describe()
            col_analysis += f"   Statistics: {col_stats}\n"
        
        # Apply filter based on comparison type
        if comparison == "equals":
            filtered_df = df[df[column].astype(str) == value]
        elif comparison == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif comparison == "greater_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') > float(value)]
            except ValueError:
                return f"❌ Cannot compare '{value}' as number. Column might not be numeric.\n{context_info}{col_analysis}"
        elif comparison == "less_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') < float(value)]
            except ValueError:
                return f"❌ Cannot compare '{value}' as number. Column might not be numeric.\n{context_info}{col_analysis}"
        else:
            return f"❌ Invalid comparison type '{comparison}'. Valid options: equals, contains, greater_than, less_than"
        
        # Save filtered data
        filtered_df.to_csv(output_file, index=False)
        
        # Enhanced result with comprehensive analysis
        result_info = f"✅ Enhanced CSV filter completed successfully!\n{context_info}{col_analysis}\n"
        result_info += f"📁 Filter Results:\n"
        result_info += f"   - Filter: {column} {comparison} '{value}'\n"
        result_info += f"   - Source: {df.shape[0]} rows → {len(filtered_df)} rows\n"
        result_info += f"   - Filtered data types: {dict(filtered_df.dtypes)}\n"
        result_info += f"   - Memory usage: {filtered_df.memory_usage(deep=True).sum() / 1024:.1f} KB\n"
        result_info += f"   - File saved successfully!"
        
        return result_info
    
    except Exception as e:
        return f"❌ Error filtering CSV: {str(e)}"


@tool
def enhanced_combine_csv_files(file_list: list, output_file: str, ignore_index: bool = True, keep_only_common: bool = True) -> str:
    """
    Enhanced CSV combination with automatic data structure analysis.
    Provides df.info() and df.describe() context for all files.

    Args:
        file_list: List of CSV file paths to combine.
        output_file: Path where the combined CSV will be saved.
        ignore_index: Whether to reset index in the combined file (default: True).
        keep_only_common: If True, keeps only common columns. If False, keeps all columns and fills missing with NaN (default: True).

    Returns:
        Enhanced confirmation with comprehensive data structure analysis.
    """
    try:
        if len(file_list) < 2:
            return "❌ Please provide at least 2 CSV files to combine."
        
        dfs = []
        all_columns = []
        
        # Enhanced data structure analysis for all files
        context_info = f"""
=== ENHANCED COMBINE DATA STRUCTURE ANALYSIS ===
📊 Files to combine: {len(file_list)}
"""
        
        for i, file_path in enumerate(file_list):
            if not os.path.exists(file_path):
                return f"❌ File not found: {file_path}"
            df = pd.read_csv(file_path)
            dfs.append(df)
            all_columns.append(set(df.columns))
            
            context_info += f"\n📁 File {i+1} ({os.path.basename(file_path)}):\n"
            context_info += f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            context_info += f"   Columns: {', '.join(df.columns.tolist())}\n"
            context_info += f"   Data types: {dict(df.dtypes)}\n"
        
        # Check if all dataframes have the same columns
        columns_match = all(cols == all_columns[0] for cols in all_columns[1:])
        
        if not columns_match:
            if keep_only_common:
                # Find common columns across all files
                common_cols = set.intersection(*all_columns)
                
                if not common_cols:
                    return "❌ No common columns found across all files. Cannot combine.\n" + context_info
                
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
        
        # Enhanced result with comprehensive analysis
        result_info = f"✅ Enhanced CSV combination completed successfully!\n{context_info}\n"
        result_info += f"📁 Combination Results:\n"
        result_info += f"   - Files combined: {len(file_list)}\n"
        result_info += f"   - Result shape: {combined_df.shape[0]} rows × {combined_df.shape[1]} columns\n"
        result_info += f"   - Result data types: {dict(combined_df.dtypes)}\n"
        result_info += f"   - Memory usage: {combined_df.memory_usage(deep=True).sum() / 1024:.1f} KB\n"
        result_info += f"   - File saved successfully!{dropped_msg}"
        
        return result_info
    
    except Exception as e:
        return f"❌ Error combining CSV files: {str(e)}"
