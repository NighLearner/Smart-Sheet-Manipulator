"""
Simple data manipulation tools for CSV and Excel files.
Focuses only on data transformation operations, not analysis.
"""
import pandas as pd
import os
from smolagents import tool


@tool
def get_column_names(file_path: str) -> str:
    """
    Gets column names from a CSV or Excel file. Useful for understanding structure before manipulation.
    
    Args:
        file_path: Path to the CSV or Excel file.
    
    Returns:
        String with column names.
    """
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        return f"Columns: {', '.join(df.columns.tolist())}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def select_columns(source_file: str, output_file: str, columns: list) -> str:
    """
    Selects specific columns from a CSV or Excel file and saves to a new file.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the new file will be saved (supports .csv and .xlsx).
        columns: List of column names to select.
    
    Returns:
        Confirmation message.
    """
    try:
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Select columns
        new_df = df[columns]
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            new_df.to_excel(output_file, index=False)
        else:
            new_df.to_csv(output_file, index=False)
        
        return f"Successfully created {output_file} with columns: {', '.join(columns)}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def create_column(source_file: str, output_file: str, new_column: str, expression: str) -> str:
    """
    Creates a new column from existing columns using a pandas expression.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the new file will be saved.
        new_column: Name of the new column to create.
        expression: Pandas expression using column names (e.g., "Age * 2", "Name + '_suffix'", "Price + Tax").
                   Use column names directly in the expression (e.g., "Age * 2" not "df['Age'] * 2").
    
    Returns:
        Confirmation message.
    """
    try:
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Use pandas eval for safe expression evaluation
        # This allows expressions like "Age * 2", "Price + Tax"
        # For string operations, pandas eval works with quotes: "Name + '_suffix'"
        try:
            # Try pandas eval first (works for numeric operations)
            df[new_column] = df.eval(expression)
        except Exception:
            # If eval fails, try direct column operations for common cases
            # This handles string concatenation and other operations
            try:
                # Create a safe namespace with only the dataframe columns
                namespace = {col: df[col] for col in df.columns}
                namespace['pd'] = pd
                namespace['np'] = __import__('numpy')
                # Use eval with restricted namespace
                df[new_column] = eval(expression, {"__builtins__": {}}, namespace)
            except Exception as e:
                return f"Error evaluating expression '{expression}': {str(e)}. Please use valid expressions with column names (e.g., 'Age * 2', 'Price + Tax', 'Name + \"_suffix\"')."
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, index=False)
        
        return f"Successfully created column '{new_column}' in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def normalize_column(source_file: str, output_file: str, column: str, method: str = "min_max") -> str:
    """
    Normalizes a numeric column using min-max or z-score normalization.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the new file will be saved.
        column: Name of the column to normalize.
        method: Normalization method - "min_max" (0-1 range) or "z_score" (standardization) (default: "min_max").
    
    Returns:
        Confirmation message.
    """
    try:
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found"
        
        # Check if column is numeric
        if not pd.api.types.is_numeric_dtype(df[column]):
            return f"Error: Column '{column}' is not numeric"
        
        # Normalize
        if method == "min_max":
            min_val = df[column].min()
            max_val = df[column].max()
            if max_val == min_val:
                df[f"{column}_normalized"] = 0
            else:
                df[f"{column}_normalized"] = (df[column] - min_val) / (max_val - min_val)
        elif method == "z_score":
            mean_val = df[column].mean()
            std_val = df[column].std()
            if std_val == 0:
                df[f"{column}_normalized"] = 0
            else:
                df[f"{column}_normalized"] = (df[column] - mean_val) / std_val
        else:
            return f"Error: Invalid method '{method}'. Use 'min_max' or 'z_score'"
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, index=False)
        
        return f"Successfully normalized column '{column}' using {method} method in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def one_hot_encode(source_file: str, output_file: str, columns: list) -> str:
    """
    Performs one-hot encoding on categorical columns.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the new file will be saved.
        columns: List of column names to one-hot encode.
    
    Returns:
        Confirmation message.
    """
    try:
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Perform one-hot encoding
        df_encoded = pd.get_dummies(df, columns=columns, prefix=columns, prefix_sep='_')
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully one-hot encoded columns {', '.join(columns)} in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def label_encode(source_file: str, output_file: str, columns: list) -> str:
    """
    Performs label encoding on categorical columns (converts categories to numeric labels).
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the new file will be saved.
        columns: List of column names to label encode.
    
    Returns:
        Confirmation message.
    """
    try:
        # Try to import sklearn
        try:
            from sklearn.preprocessing import LabelEncoder
        except ImportError:
            return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Perform label encoding
        df_encoded = df.copy()
        for col in columns:
            le = LabelEncoder()
            df_encoded[f"{col}_encoded"] = le.fit_transform(df[col].astype(str))
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully label encoded columns {', '.join(columns)} in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def filter_rows(source_file: str, output_file: str, column: str, condition: str, value: str) -> str:
    """
    Filters rows based on a condition and saves to a new file.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the filtered file will be saved.
        column: Name of the column to filter on.
        condition: Condition type - "equals", "greater_than", "less_than", "contains", "not_equals".
        value: Value to compare against.
    
    Returns:
        Confirmation message.
    """
    try:
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found"
        
        # Apply filter
        if condition == "equals":
            filtered_df = df[df[column].astype(str) == value]
        elif condition == "not_equals":
            filtered_df = df[df[column].astype(str) != value]
        elif condition == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        elif condition == "greater_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') > float(value)]
            except ValueError:
                return f"Error: Cannot compare '{value}' as number for column '{column}'"
        elif condition == "less_than":
            try:
                filtered_df = df[pd.to_numeric(df[column], errors='coerce') < float(value)]
            except ValueError:
                return f"Error: Cannot compare '{value}' as number for column '{column}'"
        else:
            return f"Error: Invalid condition '{condition}'. Use: equals, not_equals, contains, greater_than, less_than"
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            filtered_df.to_excel(output_file, index=False)
        else:
            filtered_df.to_csv(output_file, index=False)
        
        return f"Successfully filtered {len(filtered_df)} rows and saved to {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def combine_files(file_list: list, output_file: str, axis: str = "vertical") -> str:
    """
    Combines multiple CSV or Excel files either vertically (stack rows) or horizontally (merge columns).
    
    Args:
        file_list: List of file paths to combine.
        output_file: Path where the combined file will be saved.
        axis: "vertical" to stack rows (default) or "horizontal" to merge columns.
    
    Returns:
        Confirmation message.
    """
    try:
        if len(file_list) < 2:
            return "Error: Please provide at least 2 files to combine"
        
        dfs = []
        for file_path in file_list:
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
            
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            dfs.append(df)
        
        # Combine dataframes
        if axis == "vertical":
            # Stack rows (must have same columns)
            combined_df = pd.concat(dfs, ignore_index=True)
        elif axis == "horizontal":
            # Merge columns (must have same number of rows)
            combined_df = pd.concat(dfs, axis=1)
        else:
            return f"Error: Invalid axis '{axis}'. Use 'vertical' or 'horizontal'"
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            combined_df.to_excel(output_file, index=False)
        else:
            combined_df.to_csv(output_file, index=False)
        
        return f"Successfully combined {len(file_list)} files and saved to {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def join_files(file1: str, file2: str, output_file: str, join_column: str, join_type: str = "inner") -> str:
    """
    Joins two CSV or Excel files on a common column.
    
    Args:
        file1: Path to the first file.
        file2: Path to the second file.
        output_file: Path where the joined file will be saved.
        join_column: Name of the column to join on (must exist in both files).
        join_type: Type of join - "inner", "left", "right", or "outer" (default: "inner").
    
    Returns:
        Confirmation message.
    """
    try:
        # Read files
        if file1.endswith('.xlsx') or file1.endswith('.xls'):
            df1 = pd.read_excel(file1)
        else:
            df1 = pd.read_csv(file1)
        
        if file2.endswith('.xlsx') or file2.endswith('.xls'):
            df2 = pd.read_excel(file2)
        else:
            df2 = pd.read_csv(file2)
        
        # Validate join column
        if join_column not in df1.columns:
            return f"Error: Column '{join_column}' not found in {file1}"
        if join_column not in df2.columns:
            return f"Error: Column '{join_column}' not found in {file2}"
        
        # Validate join type
        valid_joins = ["inner", "left", "right", "outer"]
        if join_type not in valid_joins:
            return f"Error: Invalid join type '{join_type}'. Use: {', '.join(valid_joins)}"
        
        # Perform join
        joined_df = pd.merge(df1, df2, on=join_column, how=join_type)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            joined_df.to_excel(output_file, index=False)
        else:
            joined_df.to_csv(output_file, index=False)
        
        return f"Successfully joined files and saved to {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"

