# ================================================================================
# FILE: enhanced_test_tracker.py
# ================================================================================
"""
Enhanced test tracker for app2 with dynamic prompt template integration.
All tests now include dataset structure information automatically.
"""
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add the parent directory to the path so we can import from app2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.enhanced_csv_agent_v2 import get_enhanced_agent_v2
from dynamic_prompt_template import create_smart_prompt_template
import config


class EnhancedTestTracker:
    """Enhanced test tracker with dynamic prompt integration."""
    
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
            
            if output_files is None:
                output_files = []
            
            verified_files = []
            for file_path in output_files:
                if os.path.exists(file_path):
                    verified_files.append(file_path)
            
            test_info['output_files'] = verified_files
            
            if success is None:
                success = (
                    error_message is None and
                    (not output_files or len(verified_files) > 0) and
                    (
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
                        (not output_files and len(verified_files) > 0) or
                        (not output_files and result and len(result.strip()) > 50)
                    )
                )
            
            test_info['success'] = success
            test_info['error_message'] = error_message
    
    def start_testing(self):
        """Start the overall testing process."""
        self.start_time = time.time()
        print(f"\nEnhanced CSV Manipulator Test Suite with Dynamic Prompts")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def end_testing(self):
        """End the overall testing process."""
        self.end_time = time.time()
        self.print_summary()
    
    def print_summary(self):
        """Print a comprehensive test summary."""
        if not self.tests_run:
            print("\nNo tests were run.")
            return
        
        total_tests = len(self.tests_run)
        successful_tests = sum(1 for test in self.tests_run if test['success'])
        failed_tests = total_tests - successful_tests
        
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        print("\n" + "="*80)
        print("ENHANCED TEST EXECUTION SUMMARY")
        print("="*80)
        print(f"Total Tests Run: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print(f"Total Duration: {duration:.2f} seconds")
        print(f"Average Test Duration: {duration/total_tests:.2f} seconds")
        
        print("\n" + "="*80)
        print("DETAILED TEST RESULTS")
        print("="*80)
        
        for i, test in enumerate(self.tests_run, 1):
            status = "PASS" if test['success'] else "FAIL"
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
        
        print("\n" + "="*80)
        print("OUTPUT FILES SUMMARY")
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


def run_enhanced_basic_tests():
    """Run basic tests with dynamic prompt template."""
    tracker = EnhancedTestTracker()
    tracker.start_testing()
    
    agent = get_enhanced_agent_v2()
    
    # Test 1: Create CSV with selected columns
    test_index = tracker.start_test(
        "Create Selected Columns CSV",
        "Create a new CSV file with only Name, Age, and Sex columns from train.csv"
    )
    
    try:
        # Use natural language query with dynamic prompt
        query = f"Create a new CSV file with only Name, Age, and Sex columns from train.csv and save it as answers/selected_columns.csv"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        output_file = f"{config.OUTPUT_DIR}/selected_columns.csv"
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"File created successfully: {output_file} ({file_size} bytes)")
        else:
            print(f"File not found: {output_file}")
        
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 2: Join CSV files
    test_index = tracker.start_test(
        "Join CSV Files",
        "Join train.csv and test.csv on PassengerId column using left join"
    )
    
    try:
        query = f"Join train.csv and test.csv on the PassengerId column using a left join and save the result as answers/joined_data.csv"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        output_file = f"{config.OUTPUT_DIR}/joined_data.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 3: Filter and save
    test_index = tracker.start_test(
        "Filter Female Passengers",
        "Filter train.csv for female passengers and save to new file"
    )
    
    try:
        query = f"Filter train.csv for female passengers and save the result as answers/females_only.csv"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        output_file = f"{config.OUTPUT_DIR}/females_only.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 4: Combine CSV files
    test_index = tracker.start_test(
        "Combine CSV Files",
        "Combine train.csv and test.csv vertically keeping only common columns"
    )
    
    try:
        query = f"Combine train.csv and test.csv into one file keeping only common columns and save as answers/combined_data.csv"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        output_file = f"{config.OUTPUT_DIR}/combined_data.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 5: Read CSV file
    test_index = tracker.start_test(
        "Read CSV File",
        "Read the first 5 rows of train.csv"
    )
    
    try:
        query = f"Read the first 5 rows of train.csv and show the data"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 6: Get CSV info
    test_index = tracker.start_test(
        "Get CSV Information",
        "Get comprehensive information about train.csv"
    )
    
    try:
        query = f"Get comprehensive information about train.csv including shape, columns, data types, and missing values"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 7: Search CSV
    test_index = tracker.start_test(
        "Search CSV Data",
        "Search train.csv for female passengers"
    )
    
    try:
        query = f"Search train.csv for female passengers and show the first 3 matches"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 8: Statistical description
    test_index = tracker.start_test(
        "Statistical Description",
        "Get statistical summary of numeric columns in train.csv"
    )
    
    try:
        query = f"Get statistical summary of all numeric columns in train.csv"
        enhanced_query = create_smart_prompt_template(query)
        
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        tracker.end_test(test_index, str(result), output_files=[])
        
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    tracker.end_testing()
    return tracker


if __name__ == "__main__":
    print("Running enhanced basic tests with dynamic prompt template...")
    run_enhanced_basic_tests()


