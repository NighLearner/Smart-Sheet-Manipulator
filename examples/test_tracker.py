g# ================================================================================
# FILE: test_tracker.py
# ================================================================================
"""
Test tracker for CSV manipulator AI agent.
Tracks test execution, results, and output file creation.
"""
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import get_agent
import config


class TestTracker:
    """Tracks test execution and results."""
    
    def __init__(self):
        self.tests_run = []
        self.start_time = None
        self.end_time = None
        
    def start_test(self, test_name: str, test_description: str):
        """Start tracking a test."""
        test_info = {
            'name': test_name,
            'description': test_description,
            'start_time': time.time(),
            'end_time': None,
            'result': None,
            'success': False,
            'output_files': [],
            'error_message': None,
            'agent_response': None
        }
        self.tests_run.append(test_info)
        return len(self.tests_run) - 1
    
    def end_test(self, test_index: int, result: str, success: bool = None, output_files: List[str] = None, error_message: str = None):
        """End tracking a test."""
        if test_index < len(self.tests_run):
            test_info = self.tests_run[test_index]
            test_info['end_time'] = time.time()
            test_info['result'] = result
            test_info['agent_response'] = result
            
            # Check for output files if not provided
            if output_files is None:
                output_files = []
            
            # Check if output files were actually created
            verified_files = []
            for file_path in output_files:
                if os.path.exists(file_path):
                    verified_files.append(file_path)
            
            test_info['output_files'] = verified_files
            
            # Determine success based on multiple factors
            if success is None:
                # Auto-determine success based on:
                # 1. No error message
                # 2. Output files were created (if expected)
                # 3. Agent response contains success indicators OR operation completed without errors
                success = (
                    error_message is None and
                    (not output_files or len(verified_files) > 0) and
                    (
                        '✅' in result or 
                        'successfully' in result.lower() or 
                        'created' in result.lower() or
                        'completed' in result.lower() or
                        'saved' in result.lower() or
                        'found' in result.lower() or
                        'showing' in result.lower() or
                        'total rows' in result.lower() or
                        'count' in result.lower() or
                        'file saved successfully' in result.lower() or
                        'new csv file' in result.lower() or
                        # If no error and output files were created, consider it successful
                        (not output_files and len(verified_files) > 0) or
                        # If it's a read/search operation and we got data back, consider it successful
                        (not output_files and result and len(result.strip()) > 50)
                    )
                )
            
            test_info['success'] = success
            test_info['error_message'] = error_message
    
    def start_testing(self):
        """Start the overall testing process."""
        self.start_time = time.time()
        print(f"\n🧪 Starting CSV Manipulator Test Suite at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def end_testing(self):
        """End the overall testing process."""
        self.end_time = time.time()
        self.print_summary()
    
    def print_summary(self):
        """Print a comprehensive test summary."""
        if not self.tests_run:
            print("\n❌ No tests were run.")
            return
        
        total_tests = len(self.tests_run)
        successful_tests = sum(1 for test in self.tests_run if test['success'])
        failed_tests = total_tests - successful_tests
        
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        print("\n" + "="*80)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*80)
        print(f"Total Tests Run: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print(f"Total Duration: {duration:.2f} seconds")
        print(f"Average Test Duration: {duration/total_tests:.2f} seconds")
        
        print("\n" + "="*80)
        print("📋 DETAILED TEST RESULTS")
        print("="*80)
        
        for i, test in enumerate(self.tests_run, 1):
            status = "✅ PASS" if test['success'] else "❌ FAIL"
            duration = test['end_time'] - test['start_time'] if test['end_time'] and test['start_time'] else 0
            
            print(f"\n{i}. {test['name']} - {status}")
            print(f"   Description: {test['description']}")
            print(f"   Duration: {duration:.2f} seconds")
            
            if test['output_files']:
                print(f"   Output Files Created: {len(test['output_files'])}")
                for file_path in test['output_files']:
                    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                    print(f"     - {os.path.basename(file_path)} ({file_size} bytes)")
            
            if test['error_message']:
                print(f"   Error: {test['error_message']}")
            
            if not test['success'] and test['agent_response']:
                print(f"   Agent Response: {test['agent_response'][:200]}...")
        
        print("\n" + "="*80)
        print("📁 OUTPUT FILES SUMMARY")
        print("="*80)
        
        all_output_files = []
        for test in self.tests_run:
            all_output_files.extend(test['output_files'])
        
        if all_output_files:
            print(f"Total Output Files Created: {len(all_output_files)}")
            total_size = sum(os.path.getsize(f) for f in all_output_files if os.path.exists(f))
            print(f"Total Size: {total_size} bytes ({total_size/1024:.1f} KB)")
            
            print("\nFiles created:")
            for file_path in all_output_files:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"  - {os.path.basename(file_path)} ({file_size} bytes)")
        else:
            print("No output files were created.")
        
        print("\n" + "="*80)
        print("🎯 RECOMMENDATIONS")
        print("="*80)
        
        if failed_tests > 0:
            print("❌ Some tests failed. Recommendations:")
            for test in self.tests_run:
                if not test['success']:
                    print(f"  - {test['name']}: {test['error_message'] or 'Check agent response for details'}")
        else:
            print("✅ All tests passed successfully!")
        
        if successful_tests > 0:
            print(f"\n📈 Performance: Average test duration was {duration/total_tests:.2f} seconds")
            print("💡 Consider running individual test categories for faster feedback")


def run_tracked_test(test_name: str, test_description: str, test_function, *args, **kwargs):
    """Run a test with tracking."""
    tracker = TestTracker()
    test_index = tracker.start_test(test_name, test_description)
    
    try:
        result = test_function(*args, **kwargs)
        tracker.end_test(test_index, str(result), success=True)
        return result
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
        raise


def run_basic_tests_with_tracking():
    """Run basic tests with comprehensive tracking."""
    tracker = TestTracker()
    tracker.start_testing()
    
    agent = get_agent()
    
    # Test 1: Create CSV with selected columns
    test_index = tracker.start_test(
        "Create Selected Columns CSV",
        "Create a new CSV file with only Name, Age, and Sex columns from train.csv"
    )
    
    try:
        result = agent.run(
            f"Use the create_csv_with_columns tool to create a new CSV file from {config.TRAIN_CSV} with only Name, Age, and Sex columns. "
            f"Save it as {config.OUTPUT_DIR}\\selected_columns.csv. "
            f"The function signature is: create_csv_with_columns(source_file, output_file, columns). "
            f"After creating the file, confirm the task is complete.",
            max_steps=config.MAX_STEPS
        )
        
        output_file = f"{config.OUTPUT_DIR}\\selected_columns.csv"
        
        # Verify the file was created and has content
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ File created successfully: {output_file} ({file_size} bytes)")
        else:
            print(f"⚠️ File not found: {output_file}")
        
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 2: Join CSV files
    test_index = tracker.start_test(
        "Join CSV Files",
        "Join train.csv and test.csv on PassengerId column using left join"
    )
    
    try:
        result = agent.run(
            f"Use the join_csv_files tool to join {config.TRAIN_CSV} and {config.TEST_CSV} on the PassengerId column using a left join. "
            f"Save the result as {config.OUTPUT_DIR}\\joined_data.csv. "
            f"The function signature is: join_csv_files(file1, file2, output_file, join_column, join_type)",
            max_steps=config.MAX_STEPS
        )
        
        output_file = f"{config.OUTPUT_DIR}\\joined_data.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 3: Filter and save
    test_index = tracker.start_test(
        "Filter Female Passengers",
        "Filter train.csv for female passengers and save to new file"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to filter {config.TRAIN_CSV} where Sex column contains 'female'. "
            f"Save the result as {config.OUTPUT_DIR}\\females_only.csv. "
            f"The function signature is: filter_and_save_csv(file_path, output_file, column, value, comparison)",
            max_steps=config.MAX_STEPS
        )
        
        output_file = f"{config.OUTPUT_DIR}\\females_only.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 4: Combine CSV files
    test_index = tracker.start_test(
        "Combine CSV Files",
        "Combine train.csv and test.csv vertically keeping only common columns"
    )
    
    try:
        result = agent.run(
            f"Use the combine_csv_files tool to combine {config.TRAIN_CSV} and {config.TEST_CSV} into one file. "
            f"Save the result as {config.OUTPUT_DIR}\\combined_data.csv. "
            f"Keep only common columns (keep_only_common=True). "
            f"The function signature is: combine_csv_files(file_list, output_file, ignore_index, keep_only_common)",
            max_steps=config.MAX_STEPS
        )
        
        output_file = f"{config.OUTPUT_DIR}\\combined_data.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 5: Read CSV file
    test_index = tracker.start_test(
        "Read CSV File",
        "Read the first 5 rows of train.csv"
    )
    
    try:
        result = agent.run(
            f"Use the read_csv tool to read the first 5 rows of {config.TRAIN_CSV}. "
            f"The function signature is: read_csv(file_path, n)",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 6: Get CSV info
    test_index = tracker.start_test(
        "Get CSV Information",
        "Get comprehensive information about train.csv"
    )
    
    try:
        result = agent.run(
            f"Use the get_csv_info tool to get detailed information about {config.TRAIN_CSV} including shape, columns, data types, and missing values. "
            f"The function signature is: get_csv_info(file_path)",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 7: Search CSV
    test_index = tracker.start_test(
        "Search CSV Data",
        "Search train.csv for female passengers"
    )
    
    try:
        result = agent.run(
            f"Use the search_csv tool to search {config.TRAIN_CSV} for rows where Sex column contains 'female'. Show first 3 matches. "
            f"The function signature is: search_csv(file_path, column, value, n)",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 8: Statistical description
    test_index = tracker.start_test(
        "Statistical Description",
        "Get statistical summary of numeric columns in train.csv"
    )
    
    try:
        result = agent.run(
            f"Use the describe_csv tool to get statistical summary of all numeric columns in {config.TRAIN_CSV}. "
            f"The function signature is: describe_csv(file_path)",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    tracker.end_testing()
    return tracker


def run_comprehensive_tests_with_tracking():
    """Run comprehensive tests with tracking."""
    tracker = TestTracker()
    tracker.start_testing()
    
    agent = get_agent()
    
    # Test 1: Basic CSV Operations
    test_index = tracker.start_test(
        "Basic CSV Operations",
        "Read CSV file, get info, get column names, and statistical description"
    )
    
    try:
        result = agent.run(
            f"Use the read_csv tool to read the first 10 rows of {config.TRAIN_CSV}. "
            f"Then use get_csv_info to get file information. "
            f"Then use get_column_names to get column names. "
            f"Finally use describe_csv to get statistical summary.",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 2: Search and Filter Operations
    test_index = tracker.start_test(
        "Search and Filter Operations",
        "Search for female passengers, first class passengers, and survivors"
    )
    
    try:
        result = agent.run(
            f"Use the search_csv tool to search {config.TRAIN_CSV} for female passengers, first class passengers, and survivors. "
            f"Show the results for each search.",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 3: Data Creation Operations
    test_index = tracker.start_test(
        "Data Creation Operations",
        "Create multiple CSV files with different column selections"
    )
    
    try:
        result = agent.run(
            f"Use the create_csv_with_columns tool to create multiple CSV files from {config.TRAIN_CSV}: "
            f"1. Basic info (Name, Age, Sex, Survived) - save as {config.OUTPUT_DIR}\\passenger_basic_info.csv "
            f"2. Demographics (Pclass, Sex, Age, Embarked) - save as {config.OUTPUT_DIR}\\passenger_demographics.csv "
            f"3. Family info (SibSp, Parch, Ticket, Fare) - save as {config.OUTPUT_DIR}\\passenger_family_info.csv",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [
            f"{config.OUTPUT_DIR}\\passenger_basic_info.csv",
            f"{config.OUTPUT_DIR}\\passenger_demographics.csv",
            f"{config.OUTPUT_DIR}\\passenger_family_info.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 4: Join Operations
    test_index = tracker.start_test(
        "Join Operations",
        "Perform different types of joins between train.csv and test.csv"
    )
    
    try:
        result = agent.run(
            f"Use the join_csv_files tool to perform different joins between {config.TRAIN_CSV} and {config.TEST_CSV}: "
            f"1. Inner join - save as {config.OUTPUT_DIR}\\inner_joined_data.csv "
            f"2. Left join - save as {config.OUTPUT_DIR}\\left_joined_data.csv "
            f"3. Outer join - save as {config.OUTPUT_DIR}\\outer_joined_data.csv",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [
            f"{config.OUTPUT_DIR}\\inner_joined_data.csv",
            f"{config.OUTPUT_DIR}\\left_joined_data.csv",
            f"{config.OUTPUT_DIR}\\outer_joined_data.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 5: Filter and Save Operations
    test_index = tracker.start_test(
        "Filter and Save Operations",
        "Filter data by different criteria and save to separate files"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to filter {config.TRAIN_CSV} by different criteria: "
            f"1. Female passengers - save as {config.OUTPUT_DIR}\\female_passengers.csv "
            f"2. First class passengers - save as {config.OUTPUT_DIR}\\first_class_passengers.csv "
            f"3. Survivors - save as {config.OUTPUT_DIR}\\survivors.csv "
            f"4. Adult passengers (Age >= 18) - save as {config.OUTPUT_DIR}\\adult_passengers.csv",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [
            f"{config.OUTPUT_DIR}\\female_passengers.csv",
            f"{config.OUTPUT_DIR}\\first_class_passengers.csv",
            f"{config.OUTPUT_DIR}\\survivors.csv",
            f"{config.OUTPUT_DIR}\\adult_passengers.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 6: Combine Operations
    test_index = tracker.start_test(
        "Combine Operations",
        "Combine multiple CSV files with different strategies"
    )
    
    try:
        result = agent.run(
            f"Use the combine_csv_files tool to combine {config.TRAIN_CSV} and {config.TEST_CSV}: "
            f"1. Keep only common columns - save as {config.OUTPUT_DIR}\\combined_common_columns.csv "
            f"2. Keep all columns (fill missing with NaN) - save as {config.OUTPUT_DIR}\\combined_all_columns.csv",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [
            f"{config.OUTPUT_DIR}\\combined_common_columns.csv",
            f"{config.OUTPUT_DIR}\\combined_all_columns.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 7: Data Insights and Analysis
    test_index = tracker.start_test(
        "Data Insights and Analysis",
        "Analyze survival rates, demographics, and patterns in the data"
    )
    
    try:
        result = agent.run(
            f"Analyze the data in {config.TRAIN_CSV} to provide insights about: "
            f"1. Survival rates by gender "
            f"2. Passenger class distribution "
            f"3. Age distribution "
            f"4. Fare distribution",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 8: CRUD Operations
    test_index = tracker.start_test(
        "CRUD Operations",
        "Create, read, update, and delete operations on CSV files"
    )
    
    try:
        result = agent.run(
            f"Perform CRUD operations: "
            f"1. Create a new CSV with sample data - save as {config.OUTPUT_DIR}\\sample_passengers.csv "
            f"2. Append new data to the CSV "
            f"3. Read and verify the data "
            f"4. Delete the test file",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [f"{config.OUTPUT_DIR}\\sample_passengers.csv"]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 9: Error Handling and Edge Cases
    test_index = tracker.start_test(
        "Error Handling and Edge Cases",
        "Test error handling for invalid operations and missing files"
    )
    
    try:
        result = agent.run(
            f"Test error handling by attempting: "
            f"1. Read a non-existent file "
            f"2. Search for non-existent column "
            f"3. Create CSV with non-existent columns "
            f"4. Join files on non-existent column",
            max_steps=config.MAX_STEPS
        )
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 10: Complex Data Manipulation
    test_index = tracker.start_test(
        "Complex Data Manipulation",
        "Perform complex data manipulation scenarios"
    )
    
    try:
        result = agent.run(
            f"Perform complex data manipulation: "
            f"1. Create comprehensive analysis dataset - save as {config.OUTPUT_DIR}\\complete_passenger_data.csv "
            f"2. Create demographic analysis dataset - save as {config.OUTPUT_DIR}\\adult_demographics.csv "
            f"3. Create family analysis dataset - save as {config.OUTPUT_DIR}\\family_passengers.csv "
            f"4. Create survival analysis dataset - save as {config.OUTPUT_DIR}\\survival_analysis.csv",
            max_steps=config.MAX_STEPS
        )
        
        output_files = [
            f"{config.OUTPUT_DIR}\\complete_passenger_data.csv",
            f"{config.OUTPUT_DIR}\\adult_demographics.csv",
            f"{config.OUTPUT_DIR}\\family_passengers.csv",
            f"{config.OUTPUT_DIR}\\survival_analysis.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    tracker.end_testing()
    return tracker


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "basic":
            run_basic_tests_with_tracking()
        elif test_type == "comprehensive":
            run_comprehensive_tests_with_tracking()
        else:
            print("Usage: python test_tracker.py [basic|comprehensive]")
    else:
        print("Running basic tests with tracking...")
        run_basic_tests_with_tracking()
