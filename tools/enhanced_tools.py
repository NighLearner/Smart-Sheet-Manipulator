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
def enhanced_read_csv(file_path: str, n: int = 5) -> str:
    """
    Enhanced CSV reader that automatically includes df.info() and df.describe() information.
    This helps the AI agent understand the data structure for better code generation.

    Args:
        file_path: Path to the CSV file.
        n: Number of rows to display (default: 5).

    Returns:
        The first few rows of the dataframe plus comprehensive data structure information.
    """
    df = pd.read_csv(file_path)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    # Get basic data preview
    data_preview = str(df.head(n))
    
    # Get comprehensive data structure information
    info_section = f"""

=== AUTOMATIC DATA STRUCTURE ANALYSIS ===
📊 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns
📋 Column Information:
"""
    
    for idx, col in enumerate(df.columns):
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        dtype = df[col].dtype
        info_section += f"  {idx+1}. {col}: {non_null}/{len(df)} non-null ({null_count} missing), dtype: {dtype}\n"
    
    # Add data types summary
    info_section += f"\n📈 Data Types Summary:\n"
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        info_section += f"  - {dtype}: {count} columns\n"
    
    # Add categorical column unique values (first 5 columns)
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        info_section += f"\n🏷️ Categorical Columns Unique Values (sample):\n"
        for col in categorical_cols[:3]:  # Show first 3 categorical columns
            unique_vals = df[col].dropna().unique()[:5]  # First 5 unique values
            info_section += f"  - {col}: {list(unique_vals)}\n"
    
    # Add numeric column statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        info_section += f"\n📊 Numeric Columns Statistics:\n"
        numeric_summary = df[numeric_cols].describe()
        info_section += f"{numeric_summary}\n"
    
    info_section += "\n=== END DATA STRUCTURE ANALYSIS ===\n"
    info_section += "💡 Use this information to write accurate code that matches the actual data structure.\n"
    info_section += "🔧 CODING TIP: Avoid unnecessary imports - use the provided enhanced tools instead of direct pandas operations.\n"
    
    return data_preview + info_section


@tool
def enhanced_get_csv_info(file_path: str) -> str:
    """
    Enhanced CSV info that provides comprehensive data structure analysis.
    This includes df.info() equivalent plus df.describe() for better code generation.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Detailed CSV information with enhanced data structure analysis.
    """
    df = pd.read_csv(file_path)
    
    info_str = f"""
=== ENHANCED CSV FILE ANALYSIS ===
📊 Dataset Overview:
   Total Rows: {len(df)}
   Total Columns: {len(df.columns)}
   Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB

📋 Detailed Column Analysis:
"""
    
    for idx, col in enumerate(df.columns):
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        dtype = df[col].dtype
        info_str += f"   {idx+1}. {col}: {non_null}/{len(df)} non-null ({null_count} missing), dtype: {dtype}\n"
    
    # Add data types distribution
    info_str += f"\n📈 Data Types Distribution:\n"
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        info_str += f"   - {dtype}: {count} columns\n"
    
    # Add categorical analysis
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        info_str += f"\n🏷️ Categorical Columns Analysis:\n"
        for col in categorical_cols:
            unique_count = df[col].nunique()
            most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
            info_str += f"   - {col}: {unique_count} unique values, most common: '{most_common}'\n"
    
    # Add numeric analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        info_str += f"\n📊 Numeric Columns Statistical Summary:\n"
        numeric_summary = df[numeric_cols].describe()
        info_str += f"{numeric_summary}\n"
        
        # Add correlation information for numeric columns
        if len(numeric_cols) > 1:
            info_str += f"\n🔗 Numeric Columns Correlation Matrix:\n"
            correlation_matrix = df[numeric_cols].corr()
            info_str += f"{correlation_matrix}\n"
    
    info_str += "\n=== END ENHANCED ANALYSIS ===\n"
    info_str += "💡 This comprehensive analysis helps ensure accurate code generation.\n"
    info_str += "🔧 CODING TIP: Use the enhanced tools instead of direct pandas imports for better results.\n"
    
    return info_str


@tool
def enhanced_search_csv(file_path: str, column: str, value: str, n: int = 5) -> str:
    """
    Enhanced CSV search that includes data structure context for better filtering.
    Automatically provides df.info() and df.describe() context.

    Args:
        file_path: Path to the CSV file.
        column: Column name to search in.
        value: Value to match.
        n: Number of matching rows to return.

    Returns:
        Matching rows plus data structure context for accurate filtering.
    """
    df = pd.read_csv(file_path)
    
    # First, provide data structure context
    context_info = f"""
=== DATA STRUCTURE CONTEXT FOR SEARCH ===
📊 Dataset: {df.shape[0]} rows × {df.shape[1]} columns
📋 Available columns: {', '.join(df.columns.tolist())}
"""
    
    if column not in df.columns:
        return f"❌ Column '{column}' not found in CSV.\n{context_info}\nAvailable columns: {', '.join(df.columns)}"
    
    # Add column-specific information
    col_dtype = df[column].dtype
    col_nulls = df[column].isna().sum()
    col_unique = df[column].nunique()
    
    context_info += f"🎯 Target Column '{column}':\n"
    context_info += f"   - Data type: {col_dtype}\n"
    context_info += f"   - Null values: {col_nulls}\n"
    context_info += f"   - Unique values: {col_unique}\n"
    
    if col_dtype == 'object':
        unique_vals = df[column].dropna().unique()[:10]
        context_info += f"   - Sample values: {list(unique_vals)}\n"
    else:
        col_stats = df[column].describe()
        context_info += f"   - Statistics: {col_stats}\n"
    
    context_info += "\n=== END CONTEXT ===\n"
    
    # Perform the search
    matches = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    
    if matches.empty:
        return f"⚠️ No matching records found.\n{context_info}\n💡 Check the data type and unique values above to refine your search."
    
    result_df = matches.head(n).reset_index(drop=True)
    
    with pd.option_context('display.max_columns', None, 
                          'display.width', 1000,
                          'display.max_colwidth', 40):
        output = f"{context_info}\n🔍 Search Results:\nFound {len(matches)} matching rows. Showing first {len(result_df)}:\n\n{str(result_df)}"
    
    return output


@tool
def enhanced_describe_csv(file_path: str) -> str:
    """
    Enhanced CSV description with comprehensive statistical analysis.
    Provides df.describe() plus additional insights for better understanding.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Enhanced statistical summary with data structure insights.
    """
    df = pd.read_csv(file_path)
    
    # Basic describe() output
    with pd.option_context('display.max_columns', None,
                          'display.width', 1000):
        basic_describe = str(df.describe())
    
    # Enhanced analysis
    enhanced_info = f"""
=== ENHANCED STATISTICAL ANALYSIS ===
📊 Dataset Overview: {df.shape[0]} rows × {df.shape[1]} columns

📈 Standard Statistical Summary:
{basic_describe}

🔍 Additional Insights:
"""
    
    # Add data type specific analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    if len(numeric_cols) > 0:
        enhanced_info += f"\n📊 Numeric Columns ({len(numeric_cols)}):\n"
        for col in numeric_cols:
            col_info = df[col].describe()
            enhanced_info += f"   {col}: mean={col_info['mean']:.2f}, std={col_info['std']:.2f}, range=[{col_info['min']:.2f}, {col_info['max']:.2f}]\n"
    
    if len(categorical_cols) > 0:
        enhanced_info += f"\n🏷️ Categorical Columns ({len(categorical_cols)}):\n"
        for col in categorical_cols:
            unique_count = df[col].nunique()
            null_count = df[col].isna().sum()
            most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
            enhanced_info += f"   {col}: {unique_count} unique values, {null_count} nulls, most common: '{most_common}'\n"
    
    # Add missing data analysis
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        enhanced_info += f"\n⚠️ Missing Data Analysis:\n"
        for col, missing_count in missing_data.items():
            if missing_count > 0:
                percentage = (missing_count / len(df)) * 100
                enhanced_info += f"   {col}: {missing_count} missing ({percentage:.1f}%)\n"
    else:
        enhanced_info += f"\n✅ No missing data found in any column.\n"
    
    enhanced_info += "\n=== END ENHANCED ANALYSIS ===\n"
    enhanced_info += "💡 Use this comprehensive analysis to write accurate data manipulation code.\n"
    enhanced_info += "🔧 CODING TIP: Prefer enhanced tools over direct pandas imports for better integration.\n"
    
    return enhanced_info


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
