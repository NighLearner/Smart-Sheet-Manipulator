# Smart Sheet Manipulator

An AI-powered CSV manipulation tool that uses natural language queries to perform complex data operations on CSV files. Built with Python, pandas, and smolagents, this tool allows you to interact with CSV data using plain English commands.

## 🚀 Features

### Core Capabilities
- **Natural Language Processing**: Interact with CSV files using plain English queries
- **Comprehensive CSV Operations**: Read, search, filter, join, combine, and analyze CSV files
- **Enhanced Data Inspection**: Automatic data structure analysis with `df.info()` and `df.describe()` integration
- **Interactive Mode**: Real-time interaction with your data through a command-line interface
- **Test Suite**: Comprehensive test examples demonstrating all capabilities

### Operations Supported
- ✅ Read and display CSV data
- ✅ Get file information and column details
- ✅ Search and filter data
- ✅ Statistical analysis and descriptions
- ✅ Create new CSV files with selected columns
- ✅ Join multiple CSV files (inner, left, right, outer joins)
- ✅ Filter and save data based on conditions
- ✅ Combine multiple CSV files
- ✅ Append data to existing files
- ✅ Delete CSV files
- ✅ CRUD operations (Create, Read, Update, Delete)

## 📋 Requirements

- Python 3.8 or higher
- Ollama (for local LLM model)
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/NighLearner/Smart-Sheet-Manipulator.git
cd Smart-Sheet-Manipulator/app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Ollama
Make sure Ollama is installed and running on your system. The project uses the `qwen2.5-coder:3b` model by default.

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/

# Pull the required model
ollama pull qwen2.5-coder:3b
```

### 4. Configure Settings
Update `config.py` with your file paths and settings:

```python
# File Paths
DATA_DIR = r"D:\sheet_manipulator"  # Update to your data directory
TRAIN_CSV = os.path.join(DATA_DIR, "train.csv")
TEST_CSV = os.path.join(DATA_DIR, "test.csv")
OUTPUT_DIR = DATA_DIR  # Update to your output directory

# Model Configuration
MODEL_ID = "ollama/qwen2.5-coder:3b"
MODEL_API_KEY = "ollama"

# Agent Configuration
MAX_STEPS = 5  # Maximum steps for agent execution
```

## 🎯 Usage

### Interactive Mode

Run the application and choose from the menu:

```bash
python main.py
```

**Menu Options:**
1. Run basic tests with tracking
2. Run comprehensive tests with tracking
3. Run Titanic dataset comprehensive tests
4. Interactive mode
5. Enhanced Interactive mode (with automatic data inspection)
6. Exit

### Enhanced Interactive Mode (Recommended)

The enhanced mode automatically includes data structure information (`df.info()` and `df.describe()`) to improve code generation accuracy:

```bash
python main.py
# Choose option 5: Enhanced Interactive mode
```

**Example Queries:**
```
📝 Enter your query: Read the first 10 rows of train.csv
📝 Enter your query: Create a new CSV with only Name and Age columns from train.csv
📝 Enter your query: Filter train.csv for female passengers and save to female_passengers.csv
📝 Enter your query: Join train.csv and test.csv on PassengerId
📝 Enter your query: Search for passengers with Age greater than 30
```

### Programmatic Usage

```python
from agent import get_agent
import config

# Get the agent
agent = get_agent()

# Run a query
result = agent.run("Read the first 5 rows of train.csv", max_steps=config.MAX_STEPS)
print(result)
```

### Enhanced Agent with Data Inspection

```python
from agent.enhanced_csv_agent import run_with_data_inspection
import config

# Run with automatic data inspection
result = run_with_data_inspection(
    "Create a new CSV with Name, Age, and Survived columns",
    file_paths=[config.TRAIN_CSV],
    max_steps=config.MAX_STEPS
)
print(result)
```

## 📁 Project Structure

```
app/
├── agent/
│   ├── __init__.py
│   ├── csv_agent.py              # Basic CSV agent
│   └── enhanced_csv_agent.py     # Enhanced agent with data inspection
├── tools/
│   ├── __init__.py
│   ├── basic_tools.py            # Basic CSV manipulation tools
│   ├── advanced_tools.py         # Advanced operations (join, combine, etc.)
│   └── enhanced_tools.py         # Enhanced tools with data inspection
├── examples/
│   ├── README.md                 # Detailed test documentation
│   ├── test_tracker.py           # Test execution with tracking
│   └── titanic_test_suite.py     # Comprehensive Titanic dataset tests
├── config.py                     # Configuration settings
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🔧 Available Tools

### Basic Tools
- `read_csv(file_path, n=5)` - Read and display first N rows
- `get_csv_info(file_path)` - Get comprehensive file information
- `get_column_names(file_path)` - Get column names
- `describe_csv(file_path)` - Statistical summary of numeric columns
- `search_csv(file_path, column, value, n=5)` - Search for specific values
- `append_to_csv(file_path, data)` - Append data to CSV file

### Advanced Tools
- `create_csv_with_columns(file_path, columns, source_file)` - Create CSV with selected columns
- `join_csv_files(file1, file2, on, how='inner')` - Join two CSV files
- `filter_and_save_csv(file_path, condition, output_path)` - Filter and save data
- `combine_csv_files(file_paths, output_path)` - Combine multiple CSV files
- `delete_csv_file(file_path)` - Delete a CSV file

### Enhanced Tools
Enhanced versions of the above tools that automatically include data structure information for better accuracy.

## 📊 Example Use Cases

### 1. Data Exploration
```python
# Get file information
query = "Get information about train.csv"
result = agent.run(query)

# Get column names
query = "What columns are in train.csv?"
result = agent.run(query)

# Statistical summary
query = "Describe the numeric columns in train.csv"
result = agent.run(query)
```

### 2. Data Filtering
```python
# Filter by condition
query = "Filter train.csv for passengers with Age > 30 and save to adults.csv"
result = agent.run(query)

# Filter by category
query = "Filter train.csv for female passengers and save to female_passengers.csv"
result = agent.run(query)
```

### 3. Data Transformation
```python
# Create new CSV with selected columns
query = "Create a new CSV with Name, Age, and Survived columns from train.csv"
result = agent.run(query)

# Join CSV files
query = "Join train.csv and test.csv on PassengerId using inner join"
result = agent.run(query)
```

### 4. Data Analysis
```python
# Search for patterns
query = "Search for passengers with Name containing 'Smith'"
result = agent.run(query)

# Combine datasets
query = "Combine train.csv and test.csv into combined_data.csv"
result = agent.run(query)
```

## 🧪 Testing

The project includes comprehensive test suites:

### Run Basic Tests
```bash
python main.py
# Choose option 1: Run basic tests with tracking
```

### Run Comprehensive Tests
```bash
python main.py
# Choose option 2: Run comprehensive tests with tracking
```

### Run Titanic Dataset Tests
```bash
python main.py
# Choose option 3: Run Titanic dataset comprehensive tests
```

### Direct Test Execution
```bash
# Run test tracker
python examples/test_tracker.py

# Run Titanic test suite
python examples/titanic_test_suite.py
```

## ⚙️ Configuration

### Model Configuration
```python
MODEL_ID = "ollama/qwen2.5-coder:3b"  # LLM model to use
MODEL_API_KEY = "ollama"               # API key for the model
```

### File Paths
```python
DATA_DIR = r"D:\sheet_manipulator"     # Data directory
TRAIN_CSV = "path/to/train.csv"        # Training CSV file
TEST_CSV = "path/to/test.csv"          # Test CSV file
OUTPUT_DIR = "path/to/output"          # Output directory
```

### Agent Configuration
```python
MAX_STEPS = 5              # Maximum steps for agent execution
ADD_BASE_TOOLS = False     # Whether to add base tools
```

### Display Settings
```python
DISPLAY_MAX_COLUMNS = None      # Maximum columns to display
DISPLAY_WIDTH = None            # Display width
DISPLAY_MAX_COLWIDTH = 50       # Maximum column width
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not running**
   - Ensure Ollama is installed and running
   - Check if the model is available: `ollama list`
   - Pull the model if missing: `ollama pull qwen2.5-coder:3b`

2. **File not found errors**
   - Verify CSV files exist in the configured paths
   - Update paths in `config.py` if needed

3. **Permission errors**
   - Ensure write permissions for the output directory
   - Check file permissions for CSV files

4. **Memory issues**
   - For large datasets, consider filtering data first
   - Reduce `MAX_STEPS` in config for simpler operations

5. **Model errors**
   - Verify Ollama is running: `ollama serve`
   - Check model availability: `ollama list`
   - Try a different model if issues persist

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents)
- Uses [LiteLLM](https://github.com/BerriAI/litellm) for LLM integration
- Powered by [Ollama](https://ollama.ai/) for local model execution
- Data manipulation powered by [pandas](https://pandas.pydata.org/)

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for efficient CSV data manipulation**

#   S m a r t - S h e e t - M a n i p u l a t o r  
 