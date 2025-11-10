# App2 - Enhanced CSV Manipulator V2

## Overview
App2 is an enhanced version of the original CSV manipulator with significant improvements in data handling, efficiency, and user experience.

## Key Differences from App (Original)

### 1. **DataFrame Returns Instead of Strings**
- **App**: All tools returned formatted strings
- **App2**: All tools now return pandas DataFrames for better data manipulation
- **Benefit**: Enables direct data operations and better integration with pandas

### 2. **Reduced Step Limit**
- **App**: Maximum 5 steps
- **App2**: Maximum 3 steps for improved efficiency
- **Benefit**: Faster processing and more focused responses

### 3. **Enhanced Error Handling**
- **App**: Basic error handling
- **App2**: Try-catch blocks in every step with `final_answer()` function
- **Benefit**: Robust error handling and graceful failure recovery

### 4. **Intelligent Query Processing**
- **App**: Generic processing for all queries
- **App2**: Different strategies for different query types:
  - **Comprehensive Analysis Questions** (e.g., "What's the mean age?"): Detailed analysis in step 2
  - **DataFrame Requests** (e.g., "Show me passengers over 30"): Direct DataFrame return in step 1

### 7. **Dynamic Prompt Template**
- **App**: Generic prompts without dataset awareness
- **App2**: Dynamic prompts with automatic df.info() and df.describe() inclusion
- **Benefit**: Agent knows actual data structure, prevents parameter errors

## File Structure
```
app2/
├── agent/
│   ├── enhanced_csv_agent_v2.py    # New V2 agent with DataFrame returns
│   ├── csv_agent.py                 # Original agent (unchanged)
│   └── enhanced_csv_agent.py        # Original enhanced agent (unchanged)
├── tools/
│   ├── basic_tools.py               # Modified to return DataFrames
│   ├── advanced_tools.py            # Modified to return DataFrames
│   └── enhanced_tools.py            # Modified to return DataFrames
├── answers/                         # NEW: Directory for all CSV output files
├── config.py                        # Modified (MAX_STEPS = 3, OUTPUT_DIR = answers)
├── main.py                          # Modified to use V2 agent with dynamic prompts
├── dynamic_prompt_template.py        # NEW: Dynamic prompt template with df.info()/df.describe()
├── test_app2_differences.py         # Test script for V2 features
├── test_answers_directory.py         # Test script for answers directory
├── test_dynamic_prompt.py           # Test script for dynamic prompt template
└── README.md                        # This documentation
```

## Key Features

### 1. **final_answer() Function**
```python
def final_answer(result):
    """
    Handles different result types and formats them appropriately.
    - DataFrames: Formatted display with proper options
    - Strings: Direct output
    - Empty DataFrames: Informative message
    """
```

### 2. **Enhanced Tool Returns**
All tools now return DataFrames:
- `read_csv()` → DataFrame with first n rows
- `get_csv_info()` → DataFrame with column information
- `search_csv()` → DataFrame with matching rows
- `describe_csv()` → DataFrame with statistical summary
- And more...

### 3. **Query Type Detection**
The agent automatically detects query types:
- **Statistical Questions**: "What's the mean age?", "How many passengers survived?"
- **Data Requests**: "Show me passengers over 30", "Create a filtered CSV"

### 4. **Try-Catch Pattern**
Every step follows this pattern:
```python
try:
    # Analysis code
    result = analysis_function()
    final_answer(result)
except Exception as e:
    print(f"Error in step: {e}")
    # Continue to next step
```

## Usage Examples

### Comprehensive Analysis Question
```python
query = "What's the mean age of all passengers?"
result = run_with_data_inspection_v2(query)
# Returns: Detailed analysis with insights
```

### DataFrame Request
```python
query = "Show me passengers over 30"
result = run_with_data_inspection_v2(query)
# Returns: DataFrame with filtered data
```

## Testing
Run the test scripts to see the differences:
```bash
cd app2
python test_app2_differences.py
python test_answers_directory.py
python test_dynamic_prompt.py
```

## Dynamic Prompt Template
The dynamic prompt template automatically provides comprehensive dataset information:

### **Features:**
- **Automatic df.info()**: Column names, data types, null counts
- **Automatic df.describe()**: Statistical summary for numeric columns  
- **Categorical analysis**: Unique values and distributions
- **Sample data**: First few rows for context
- **Tool signatures**: Available functions and parameters
- **Smart detection**: Automatically detects relevant datasets

### **Example:**
```python
# Original query
query = "Find female passengers"

# Automatically enhanced with:
# - Dataset shape: 891 rows × 12 columns
# - Column info: Sex (object, 2 unique values: ['male', 'female'])
# - Data types: int64, object, float64
# - Tool signatures: search_csv(file_path, column, value, n=5)
# - Guidelines: Use exact column names, check data types
```

## Answers Directory
All CSV output files generated by app2 are automatically saved in the `app2/answers/` directory:
- **Location**: Same directory as `main.py`
- **Auto-creation**: Directory is created automatically if it doesn't exist
- **Organization**: All results are centralized in one location
- **Access**: Easy to find and manage all generated CSV files

## Benefits of App2

1. **Better Data Handling**: DataFrame returns enable more sophisticated data operations
2. **Improved Efficiency**: 3-step limit forces more focused and efficient processing
3. **Robust Error Handling**: Try-catch blocks prevent crashes and enable recovery
4. **Context-Aware Responses**: Different strategies for different query types
5. **Enhanced User Experience**: More accurate and comprehensive responses

## Migration from App to App2

To use App2 instead of App:
1. Import from `agent.enhanced_csv_agent_v2` instead of `agent.enhanced_csv_agent`
2. Use `run_with_data_inspection_v2()` instead of `run_with_data_inspection()`
3. Expect DataFrame returns instead of string returns
4. Benefit from improved error handling and efficiency
