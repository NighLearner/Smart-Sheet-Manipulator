# CSV Manipulator AI Agent - Test Examples

This directory contains comprehensive test examples for the CSV Manipulator AI Agent, demonstrating all its capabilities for manipulating, analyzing, and performing CRUD operations on CSV files.

## Test Files

### 1. `test_examples.py` - Basic Test Examples
Contains 4 basic test cases demonstrating core functionality:
- **Test 1**: Create CSV with selected columns
- **Test 2**: Join two CSV files
- **Test 3**: Filter and save data
- **Test 4**: Combine multiple CSV files

### 2. `detailed_test_examples.py` - Comprehensive Test Suite
Contains 11 comprehensive test categories with 50+ individual test cases:

#### Test 1: Basic CSV Operations
- Read CSV files (first N rows)
- Get comprehensive CSV information
- Get column names
- Statistical description of numeric columns

#### Test 2: Search and Filter Operations
- Search for specific values in columns
- Search for patterns in text data
- Search for numeric conditions
- Multiple search criteria

#### Test 3: Data Creation and Column Selection
- Create CSV with selected columns
- Create demographic information datasets
- Create family information datasets
- Create specialized analysis datasets

#### Test 4: Join Operations
- Inner join between CSV files
- Left join operations
- Right join operations
- Outer join operations

#### Test 5: Filter and Save Operations
- Filter by gender
- Filter by passenger class
- Filter by age ranges
- Filter by survival status
- Filter by fare amounts

#### Test 6: Combine Multiple CSV Files
- Combine with common columns only
- Combine with all columns (fill missing with NaN)
- Handle different column structures
- Preserve data integrity

#### Test 7: Data Insights and Analysis
- Analyze survival rates by gender
- Analyze passenger class distribution
- Analyze age distribution
- Analyze fare distribution

#### Test 8: CRUD Operations
- Create new CSV files with sample data
- Append data to existing CSV files
- Read and verify data
- Delete CSV files

#### Test 9: Error Handling and Edge Cases
- Handle non-existent files
- Handle non-existent columns
- Handle invalid operations
- Graceful error reporting

#### Test 10: Complex Data Manipulation
- Create comprehensive analysis datasets
- Create demographic analysis datasets
- Create family analysis datasets
- Create survival analysis datasets

#### Test 11: Performance and Large Dataset Operations
- Combine multiple datasets
- Create multiple filtered datasets
- Handle large datasets efficiently
- Performance optimization

## Running the Tests

### From Main Application
```bash
python app/main.py
```

Choose from the menu:
1. **Basic test examples** - Run the original 4 basic tests
2. **Comprehensive detailed tests** - Run all 11 test categories
3. **Specific test category** - Run a specific category of tests
4. **Interactive mode** - Use the agent interactively

### Direct Execution
```bash
# Run all detailed tests
python app/examples/detailed_test_examples.py

# Run specific test category
python app/examples/detailed_test_examples.py basic
python app/examples/detailed_test_examples.py search
python app/examples/detailed_test_examples.py insights
```

## Available Test Categories

| Category | Description | Test Cases |
|----------|-------------|------------|
| `basic` | Basic CSV operations (read, info, search, describe) | 4 tests |
| `search` | Search and filter operations | 3 tests |
| `create` | Data creation and column selection | 3 tests |
| `join` | Join operations between CSV files | 3 tests |
| `filter` | Filter and save operations | 5 tests |
| `combine` | Combine multiple CSV files | 2 tests |
| `insights` | Data insights and analysis | 4 tests |
| `crud` | CRUD operations (create, read, update, delete) | 4 tests |
| `error` | Error handling and edge cases | 4 tests |
| `complex` | Complex data manipulation scenarios | 4 tests |
| `performance` | Performance and large dataset operations | 2 tests |

## Test Data

The tests use the following CSV files:
- `train.csv` - Titanic passenger data (891 rows, 12 columns)
- `test.csv` - Additional Titanic passenger data (418 rows, 11 columns)

## Output Files

The tests generate various output files in the configured output directory:
- `passenger_basic_info.csv` - Basic passenger information
- `passenger_demographics.csv` - Demographic data
- `passenger_family_info.csv` - Family information
- `female_passengers.csv` - Female passengers only
- `first_class_passengers.csv` - First class passengers
- `survivors.csv` - Survivors only
- `combined_data.csv` - Combined datasets
- And many more...

## Features Demonstrated

### Basic Operations
- ✅ Read CSV files
- ✅ Get file information
- ✅ Get column names
- ✅ Statistical descriptions

### Advanced Operations
- ✅ Create new CSV files
- ✅ Join multiple CSV files
- ✅ Filter and save data
- ✅ Combine multiple files

### Data Analysis
- ✅ Search and filter data
- ✅ Generate insights
- ✅ Statistical analysis
- ✅ Pattern recognition

### CRUD Operations
- ✅ Create new datasets
- ✅ Read existing data
- ✅ Update/append data
- ✅ Delete files

### Error Handling
- ✅ Handle missing files
- ✅ Handle invalid columns
- ✅ Handle invalid operations
- ✅ Graceful error reporting

## Configuration

The tests use configuration from `app/config.py`:
- `TRAIN_CSV` - Path to training data
- `TEST_CSV` - Path to test data
- `OUTPUT_DIR` - Output directory for generated files
- `MAX_STEPS` - Maximum steps for agent execution

## Requirements

- Python 3.8+
- pandas
- smolagents
- LiteLLM
- Ollama (for local model)

## Usage Examples

### Interactive Mode
```python
# Start interactive mode
python app/main.py
# Choose option 4: Interactive mode
# Enter queries like:
# "Read the first 10 rows of train.csv"
# "Create a new CSV with only Name and Age columns"
# "Filter train.csv for female passengers"
```

### Programmatic Usage
```python
from agent import get_agent
import config

agent = get_agent()
result = agent.run("Read the first 5 rows of train.csv", max_steps=3)
print(result)
```

## Troubleshooting

### Common Issues
1. **File not found errors**: Ensure CSV files exist in the configured paths
2. **Permission errors**: Ensure write permissions for output directory
3. **Model errors**: Ensure Ollama is running and model is available
4. **Memory issues**: For large datasets, consider filtering data first

### Debug Mode
Set `MAX_STEPS` to a higher value in `config.py` for complex operations.

## Contributing

To add new test cases:
1. Add new test functions to `detailed_test_examples.py`
2. Update the test categories in `run_specific_test_category()`
3. Update this README with new test descriptions
4. Test your additions thoroughly

## License

This project is part of the CSV Manipulator AI Agent system.
