"""
Advanced data manipulation tools requiring external libraries (sklearn, etc.).
Includes various encoding methods, scaling, and preprocessing operations.
"""
import pandas as pd
import os
from smolagents import tool


@tool
def standard_scaler(source_file: str, output_file: str, columns: list) -> str:
    """
    Standardizes numeric columns using sklearn's StandardScaler (z-score normalization).
    Scales features to have mean=0 and std=1.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the scaled file will be saved.
        columns: List of column names to standardize.
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.preprocessing import StandardScaler
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Perform scaling
        df_scaled = df.copy()
        scaler = StandardScaler()
        df_scaled[columns] = scaler.fit_transform(df[columns])
        
        # Add suffix to column names
        column_mapping = {col: f"{col}_scaled" for col in columns}
        df_scaled = df_scaled.rename(columns=column_mapping)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_scaled.to_excel(output_file, index=False)
        else:
            df_scaled.to_csv(output_file, index=False)
        
        return f"Successfully standardized columns {', '.join(columns)} using StandardScaler in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def min_max_scaler(source_file: str, output_file: str, columns: list, feature_range: tuple = (0, 1)) -> str:
    """
    Scales numeric columns to a specified range using sklearn's MinMaxScaler.
    Default range is (0, 1).
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the scaled file will be saved.
        columns: List of column names to scale.
        feature_range: Tuple (min, max) for the scaling range (default: (0, 1)).
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.preprocessing import MinMaxScaler
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Perform scaling
        df_scaled = df.copy()
        scaler = MinMaxScaler(feature_range=feature_range)
        df_scaled[columns] = scaler.fit_transform(df[columns])
        
        # Add suffix to column names
        column_mapping = {col: f"{col}_scaled" for col in columns}
        df_scaled = df_scaled.rename(columns=column_mapping)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_scaled.to_excel(output_file, index=False)
        else:
            df_scaled.to_csv(output_file, index=False)
        
        return f"Successfully scaled columns {', '.join(columns)} to range {feature_range} using MinMaxScaler in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def robust_scaler(source_file: str, output_file: str, columns: list) -> str:
    """
    Scales numeric columns using sklearn's RobustScaler (robust to outliers).
    Uses median and IQR (Interquartile Range) for scaling.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the scaled file will be saved.
        columns: List of column names to scale.
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.preprocessing import RobustScaler
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Perform scaling
        df_scaled = df.copy()
        scaler = RobustScaler()
        df_scaled[columns] = scaler.fit_transform(df[columns])
        
        # Add suffix to column names
        column_mapping = {col: f"{col}_robust_scaled" for col in columns}
        df_scaled = df_scaled.rename(columns=column_mapping)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_scaled.to_excel(output_file, index=False)
        else:
            df_scaled.to_csv(output_file, index=False)
        
        return f"Successfully scaled columns {', '.join(columns)} using RobustScaler in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def ordinal_encode(source_file: str, output_file: str, columns: list, categories: dict = None) -> str:
    """
    Performs ordinal encoding on categorical columns using sklearn's OrdinalEncoder.
    Converts categories to integers based on order.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the encoded file will be saved.
        columns: List of column names to encode.
        categories: Optional dict mapping column names to ordered category lists.
                   If None, categories are determined automatically.
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.preprocessing import OrdinalEncoder
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Perform encoding
        df_encoded = df.copy()
        
        if categories:
            # Use provided categories
            categories_list = [categories.get(col, 'auto') for col in columns]
            encoder = OrdinalEncoder(categories=categories_list)
        else:
            # Auto-detect categories
            encoder = OrdinalEncoder()
        
        df_encoded[columns] = encoder.fit_transform(df[columns].astype(str))
        
        # Add suffix to column names
        column_mapping = {col: f"{col}_ordinal" for col in columns}
        df_encoded = df_encoded.rename(columns=column_mapping)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully ordinal encoded columns {', '.join(columns)} in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def target_encode(source_file: str, output_file: str, column: str, target_column: str) -> str:
    """
    Performs target encoding (mean encoding) on a categorical column.
    Replaces categories with the mean of the target variable for each category.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the encoded file will be saved.
        column: Name of the categorical column to encode.
        target_column: Name of the target column (must be numeric).
    
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
        if column not in df.columns:
            return f"Error: Column '{column}' not found"
        if target_column not in df.columns:
            return f"Error: Target column '{target_column}' not found"
        
        # Check if target is numeric
        if not pd.api.types.is_numeric_dtype(df[target_column]):
            return f"Error: Target column '{target_column}' must be numeric"
        
        # Perform target encoding
        df_encoded = df.copy()
        target_mean = df.groupby(column)[target_column].mean()
        df_encoded[f"{column}_target_encoded"] = df[column].map(target_mean)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully target encoded column '{column}' using target '{target_column}' in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def frequency_encode(source_file: str, output_file: str, columns: list) -> str:
    """
    Performs frequency encoding on categorical columns.
    Replaces categories with their frequency of occurrence in the dataset.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the encoded file will be saved.
        columns: List of column names to encode.
    
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
        
        # Perform frequency encoding
        df_encoded = df.copy()
        for col in columns:
            freq_map = df[col].value_counts().to_dict()
            df_encoded[f"{col}_freq_encoded"] = df[col].map(freq_map)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully frequency encoded columns {', '.join(columns)} in {output_file}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def binary_encode(source_file: str, output_file: str, columns: list) -> str:
    """
    Performs binary encoding on categorical columns.
    Combines hash encoding with one-hot encoding for high cardinality categories.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the encoded file will be saved.
        columns: List of column names to encode.
    
    Returns:
        Confirmation message.
    """
    try:
        import category_encoders as ce
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Perform binary encoding
        df_encoded = df.copy()
        encoder = ce.BinaryEncoder(cols=columns)
        df_encoded = encoder.fit_transform(df_encoded)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_encoded.to_excel(output_file, index=False)
        else:
            df_encoded.to_csv(output_file, index=False)
        
        return f"Successfully binary encoded columns {', '.join(columns)} in {output_file}"
    
    except ImportError:
        return "Error: category_encoders is not installed. Please install it using: pip install category-encoders"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def polynomial_features(source_file: str, output_file: str, columns: list, degree: int = 2) -> str:
    """
    Creates polynomial features from numeric columns using sklearn.
    Generates polynomial and interaction features.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the file with polynomial features will be saved.
        columns: List of numeric column names to create polynomial features from.
        degree: Degree of the polynomial features (default: 2).
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.preprocessing import PolynomialFeatures
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Create polynomial features
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        poly_features = poly.fit_transform(df[columns])
        
        # Create feature names
        feature_names = poly.get_feature_names_out(columns)
        
        # Create new dataframe with polynomial features
        df_poly = df.drop(columns=columns).copy()
        df_poly = pd.concat([df_poly, pd.DataFrame(poly_features, columns=feature_names)], axis=1)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_poly.to_excel(output_file, index=False)
        else:
            df_poly.to_csv(output_file, index=False)
        
        return f"Successfully created polynomial features (degree={degree}) from columns {', '.join(columns)} in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def impute_missing_values(source_file: str, output_file: str, strategy: str = "mean", columns: list = None) -> str:
    """
    Imputes missing values in numeric columns using sklearn's SimpleImputer.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the imputed file will be saved.
        strategy: Imputation strategy - "mean", "median", "most_frequent", or "constant" (default: "mean").
        columns: List of column names to impute. If None, all numeric columns are imputed.
    
    Returns:
        Confirmation message.
    """
    try:
        from sklearn.impute import SimpleImputer
        
        # Read source file
        if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
            df = pd.read_excel(source_file)
        else:
            df = pd.read_csv(source_file)
        
        # Determine columns to impute
        if columns is None:
            columns = df.select_dtypes(include=['number']).columns.tolist()
        
        # Validate columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns not found: {', '.join(missing_cols)}"
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Perform imputation
        df_imputed = df.copy()
        imputer = SimpleImputer(strategy=strategy)
        df_imputed[columns] = imputer.fit_transform(df[columns])
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_imputed.to_excel(output_file, index=False)
        else:
            df_imputed.to_csv(output_file, index=False)
        
        return f"Successfully imputed missing values using '{strategy}' strategy for columns {', '.join(columns)} in {output_file}"
    
    except ImportError:
        return "Error: sklearn is not installed. Please install it using: pip install scikit-learn"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def handle_outliers(source_file: str, output_file: str, columns: list, method: str = "iqr") -> str:
    """
    Handles outliers in numeric columns using IQR (Interquartile Range) or Z-score method.
    
    Args:
        source_file: Path to the source CSV or Excel file.
        output_file: Path where the file with handled outliers will be saved.
        columns: List of column names to handle outliers for.
        method: Method to use - "iqr" (default) or "zscore".
    
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
        
        # Check if columns are numeric
        non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
        if non_numeric:
            return f"Error: Columns must be numeric: {', '.join(non_numeric)}"
        
        # Handle outliers - apply mask across all columns
        outliers_removed = 0
        
        if method == "iqr":
            # Calculate IQR bounds for all columns and combine masks
            mask = pd.Series([True] * len(df), index=df.index)
            
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                col_mask = (df[col] >= lower_bound) & (df[col] <= upper_bound)
                outliers_removed += (~col_mask).sum()
                mask = mask & col_mask
            
            df_clean = df[mask].copy()
        elif method == "zscore":
            try:
                from scipy import stats
                mask = pd.Series([True] * len(df), index=df.index)
                
                for col in columns:
                    z_scores = stats.zscore(df[col])
                    col_mask = (z_scores < 3) & (z_scores > -3)
                    outliers_removed += (~col_mask).sum()
                    mask = mask & col_mask
                
                df_clean = df[mask].copy()
            except ImportError:
                return "Error: scipy is not installed. Please install it using: pip install scipy"
        else:
            return f"Error: Invalid method '{method}'. Use 'iqr' or 'zscore'"
        
        # Reset index
        df_clean = df_clean.reset_index(drop=True)
        
        # Save to output file
        if output_file.endswith('.xlsx'):
            df_clean.to_excel(output_file, index=False)
        else:
            df_clean.to_csv(output_file, index=False)
        
        return f"Successfully handled outliers using '{method}' method. Removed {outliers_removed} outlier rows. Saved to {output_file}"
    
    except ImportError as e:
        if "scipy" in str(e):
            return "Error: scipy is not installed. Please install it using: pip install scipy"
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

