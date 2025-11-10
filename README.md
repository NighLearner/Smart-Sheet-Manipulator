# Data Manipulation Tool

A simple AI-powered tool for manipulating CSV and Excel files using natural language. Focuses exclusively on data transformation operations - no analysis, no insights, just data manipulation.

## 🚀 Features

### Supported Operations
- ✅ **Select Columns**: Choose specific columns from files
- ✅ **Create Columns**: Create new columns from existing ones using expressions
- ✅ **Normalization**: Normalize/standardize numeric columns (min-max or z-score)
- ✅ **One-Hot Encoding**: Encode categorical columns as binary features
- ✅ **Label Encoding**: Convert categories to numeric labels
- ✅ **Filter Rows**: Filter data based on conditions
- ✅ **Combine Files**: Combine multiple files vertically or horizontally
- ✅ **Join Files**: Join two files on a common column
- ✅ **Excel Support**: Read and write both CSV and Excel (.xlsx, .xls) files

### What This Tool Does NOT Do
- ❌ Answer analytical queries (e.g., "what is the average age?")
- ❌ Provide statistical summaries for information
- ❌ Perform data analysis or generate insights
- ❌ Explore data for understanding

**Focus**: Data transformation and manipulation only.

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

### 4. Prepare Your Files
Place your CSV or Excel files in the `app/` directory. The application will automatically create a `resultant/` directory for output files.

**Note**: File paths are automatically configured. You don't need to modify `config.py` for basic usage.

## 🎯 Usage

### Interactive Mode

Run the application:

```bash
python main.py
```

Choose option 1 for interactive mode, then enter your manipulation queries.

### Example Queries

```
📝 Select Name and Age columns from data.csv and save to output.csv
📝 Create a new column Total as Price + Tax in data.csv and save to output.csv
📝 Normalize the Age column in data.csv using min_max and save to output.csv
📝 One-hot encode the Category column in data.csv and save to output.csv
📝 Label encode the Status column in data.csv and save to output.csv
📝 Filter rows where Age > 30 from data.csv and save to output.csv
📝 Combine data1.csv and data2.csv vertically and save to output.csv
📝 Join customers.csv and orders.csv on customer_id and save to output.csv
```

### Programmatic Usage

```python
from agent import get_agent
import config

# Get the agent
agent = get_agent()

# Run a manipulation query
result = agent.run(
    "Select Name and Age columns from data.csv and save to output.csv",
    max_steps=config.MAX_STEPS
)
print(result)
```

## 📁 Project Structure

```
app/
├── agent/
│   ├── __init__.py
│   └── csv_agent.py              # Data manipulation agent
├── tools/
│   ├── __init__.py
│   └── manipulation_tools.py     # Manipulation operations
├── utils/
│   ├── __init__.py
│   └── metadata.py               # Metadata injection utilities
├── student/                      # Student test datasets (auto-generated)
├── titanic/                      # Titanic test datasets
├── results/                      # Test results (auto-generated)
│   ├── student/                  # Student test results
│   └── titanic/                  # Titanic test results
├── resultant/                    # Output directory (created automatically)
├── config.py                     # Configuration settings
├── main.py                       # Main entry point
├── test_runner.py                # Test runner script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Available Operations

### Column Operations
- **Select Columns**: Choose specific columns from a file
- **Create Column**: Create new columns using expressions (e.g., `Price + Tax`, `Age * 2`)
- **Get Column Names**: View column names in a file

### Data Transformation (Basic)
- **Normalize Column**: Normalize numeric columns using min-max (0-1) or z-score standardization
- **One-Hot Encode**: Convert categorical columns to binary features
- **Label Encode**: Convert categories to numeric labels (0, 1, 2, ...)

### Advanced Scaling & Normalization (sklearn)
- **Standard Scaler**: Standardize numeric columns (mean=0, std=1) using sklearn's StandardScaler
- **Min-Max Scaler**: Scale numeric columns to a specified range using sklearn's MinMaxScaler
- **Robust Scaler**: Scale numeric columns using median and IQR (robust to outliers)

### Advanced Encoding Methods
- **Ordinal Encode**: Encode categorical columns with ordered integer labels
- **Target Encode**: Encode categories using mean of target variable (mean encoding)
- **Frequency Encode**: Encode categories with their frequency of occurrence
- **Binary Encode**: Encode high-cardinality categories using binary encoding (requires category-encoders)

### Feature Engineering
- **Polynomial Features**: Create polynomial and interaction features from numeric columns
- **Handle Outliers**: Remove outliers using IQR or Z-score methods
- **Impute Missing Values**: Fill missing values using mean, median, most_frequent, or constant strategy

### Filtering
- **Filter Rows**: Filter data based on conditions:
  - `equals`: Exact match
  - `not_equals`: Not equal to
  - `contains`: Contains substring
  - `greater_than`: Greater than value
  - `less_than`: Less than value

### File Operations
- **Combine Files**: Combine multiple files:
  - `vertical`: Stack rows (same columns)
  - `horizontal`: Merge columns (same rows)
- **Join Files**: Join two files on a common column:
  - `inner`: Only matching rows
  - `left`: All rows from first file
  - `right`: All rows from second file
  - `outer`: All rows from both files

## 📊 Example Use Cases

### 1. Select Specific Columns
```
Select Name, Age, and Salary columns from employees.csv and save to output.csv
```

### 2. Create New Columns
```
Create a new column Total as Price + Tax in sales.csv and save to output.csv
Create a new column FullName as FirstName + ' ' + LastName in data.csv and save to output.csv
```

### 3. Normalize Data
```
Normalize the Age column in data.csv using min_max and save to output.csv
Normalize the Salary column in data.csv using z_score and save to output.csv
```

### 4. Encode Categorical Data
```
One-hot encode the Category column in products.csv and save to output.csv
Label encode the Status column in orders.csv and save to output.csv
Ordinal encode the Priority column in tasks.csv and save to output.csv
Target encode the Category column using Sales as target in products.csv and save to output.csv
Frequency encode the City column in customers.csv and save to output.csv
```

### 5. Advanced Scaling
```
Standardize the Age and Salary columns in data.csv using StandardScaler and save to output.csv
Scale the Price column to range (0, 1) in data.csv using MinMaxScaler and save to output.csv
Robust scale the Income column in data.csv using RobustScaler and save to output.csv
```

### 6. Feature Engineering
```
Create polynomial features (degree=2) from Age and Income columns in data.csv and save to output.csv
Handle outliers in the Salary column using IQR method in data.csv and save to output.csv
Impute missing values in the Age column using mean strategy in data.csv and save to output.csv
```

### 7. Filter Data
```
Filter rows where Age > 30 from data.csv and save to output.csv
Filter rows where Status equals 'Active' from data.csv and save to output.csv
Filter rows where Name contains 'Smith' from data.csv and save to output.csv
```

### 8. Combine Files
```
Combine data1.csv and data2.csv vertically and save to output.csv
Combine file1.csv and file2.csv horizontally and save to output.csv
```

### 9. Join Files
```
Join customers.csv and orders.csv on customer_id and save to output.csv
Join employees.csv and departments.csv on department_id using left join and save to output.csv
```

## ⚙️ Configuration

### Automatic Configuration

The application automatically configures file paths:
- Output files are saved to `app/resultant/` directory
- Input files are read from the `app/` directory (or specify full paths)

### Manual Configuration (Advanced)

If you need to customize, edit `config.py`:

```python
# Model Configuration
MODEL_ID = "ollama/qwen2.5-coder:3b"  # LLM model to use
MODEL_API_KEY = "ollama"               # API key for the model

# Agent Configuration
MAX_STEPS = 5              # Maximum steps for agent execution
ADD_BASE_TOOLS = False     # Whether to add base tools
```

## 🧪 Testing

The project includes a comprehensive test runner with automatic metadata injection:

### Run All Tests

```bash
python test_runner.py
```

This will:
1. Create sample student datasets in `student/` folder
2. Setup titanic dataset in `titanic/` folder (if train.csv exists)
3. Run comprehensive tests on both datasets
4. Save all results to `results/` folder
5. Display test summary

### Test Cases

The test runner includes:

#### Student Dataset Tests (9 test cases):
- Select columns
- Create column from expression
- Normalize column (min-max)
- One-hot encode
- Label encode
- Filter rows
- Combine files
- Join files
- Multiple operations

#### Titanic Dataset Tests (13 test cases):
- Select columns
- Create column (family size)
- Normalize columns (min-max and z-score)
- One-hot encode (single and multiple columns)
- Label encode
- Filter rows (multiple conditions)
- Combine files
- Join files
- Complex multi-step operations

### Automatic Metadata Injection

All queries automatically include file metadata (df.info() equivalent) before execution:
- File shape and structure
- Column names and data types
- Null value counts
- Numeric statistics (min, max, mean, std)
- Categorical unique values

This ensures accurate operations by providing context about the data structure.

### Workflow Diagram

Generate an up-to-date workflow diagram (PNG) that documents the entire automation pipeline:

```bash
python workflow_diagram.py
```

The diagram is saved to `diagrams/data_manipulation_workflow.png`.

### Test Structure

```
app/
├── student/          # Student test datasets (auto-generated)
├── titanic/          # Titanic test datasets
├── results/          # Test results
│   ├── student/      # Student test results
│   └── titanic/      # Titanic test results
└── test_runner.py    # Test runner script
```

### How Metadata Injection Works

When you provide a query, the system automatically:

1. **Detects file paths** in your query (e.g., `data.csv`, `folder/file.xlsx`)
2. **Reads file metadata** for each detected file:
   - Shape (rows × columns)
   - Column names and data types
   - Null value counts
   - Numeric statistics (for numeric columns)
   - Unique values (for categorical columns)
3. **Enhances your query** with metadata before execution
4. **Executes the operation** with full context about the data structure

### Example Enhanced Query

**Your Query:**
```
Select Name and Age columns from titanic/train.csv and save to results/output.csv
```

**Enhanced Query (automatically generated):**
```
FILE METADATA INFORMATION:
======================================================================
=== FILE METADATA: train.csv ===
File Path: titanic/train.csv
Shape: 891 rows × 12 columns
Columns: PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked

Column Details:
--------------------------------------------------
Column: Name
  Data Type: object
  Non-null Count: 891/891
  Null Count: 0
  Unique Values: 891

Column: Age
  Data Type: float64
  Non-null Count: 714/891
  Null Count: 177
  Min: 0.42
  Max: 80.0
  Mean: 29.70
  Std: 14.53
...

======================================================================
USER QUERY:
======================================================================
Select Name and Age columns from titanic/train.csv and save to results/output.csv
```

This ensures the agent has full context about the data structure before performing operations.

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not running**
   - Ensure Ollama is installed and running
   - Check if the model is available: `ollama list`
   - Pull the model if missing: `ollama pull qwen2.5-coder:3b`
   - Start Ollama service: `ollama serve`

2. **File not found errors**
   - Ensure CSV/Excel files exist in the specified paths
   - Check that you're running from the `app/` directory
   - Verify file names match exactly (case-sensitive on Linux/Mac)

3. **Permission errors**
   - Ensure write permissions for the `resultant/` directory
   - The directory is created automatically, but check permissions if issues occur

4. **Excel file errors**
   - Ensure `openpyxl` is installed: `pip install openpyxl`
   - For older .xls files, you may need `xlrd`: `pip install xlrd`

6. **Advanced tool dependencies**
   - For binary encoding: `pip install category-encoders`
   - For Z-score outlier detection: `pip install scipy`
   - Most advanced tools require `scikit-learn` (already in requirements.txt)
   - If a tool reports a missing dependency, install it using the suggested pip command

5. **Model errors**
   - Verify Ollama is running: `ollama serve`
   - Check model availability: `ollama list`
   - Try pulling the model again: `ollama pull qwen2.5-coder:3b`

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

**Made with ❤️ for simple data manipulation**
