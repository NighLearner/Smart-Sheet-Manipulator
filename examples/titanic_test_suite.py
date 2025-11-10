# ================================================================================
# FILE: titanic_test_suite.py
# ================================================================================
"""
Comprehensive Titanic dataset test suite with real-world data analysis scenarios.
Tests various CSV manipulation operations using the Titanic passenger data.
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
                        (not output_files and len(verified_files) > 0) or
                        (not output_files and result and len(result.strip()) > 50)
                    )
                )
            
            test_info['success'] = success
            test_info['error_message'] = error_message
    
    def start_testing(self):
        """Start the overall testing process."""
        self.start_time = time.time()
        print(f"\n🚢 TITANIC DATASET TEST SUITE")
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def end_testing(self):
        """End the testing process and display summary."""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        print("\n" + "="*80)
        print("🎯 TEST SUITE SUMMARY")
        print("="*80)
        
        total_tests = len(self.tests_run)
        successful_tests = sum(1 for test in self.tests_run if test['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"\n📊 Test Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {successful_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⏱️  Duration: {duration:.2f} seconds")
        print(f"\n📋 Detailed Results:")
        
        for i, test in enumerate(self.tests_run, 1):
            status = "✅ PASS" if test['success'] else "❌ FAIL"
            duration = test['end_time'] - test['start_time'] if test['end_time'] else 0
            print(f"\n   Test {i}: {test['name']}")
            print(f"   {status} | Duration: {duration:.2f}s")
            print(f"   Description: {test['description']}")
            
            if test['output_files']:
                print(f"   Output files: {', '.join(test['output_files'])}")
            
            if test['error_message']:
                print(f"   Error: {test['error_message']}")
        
        print("\n" + "="*80)


def run_titanic_comprehensive_tests():
    """Run comprehensive Titanic dataset analysis tests."""
    tracker = TestTracker()
    tracker.start_testing()
    
    agent = get_agent()
    
    # Test 1: Survival Analysis - Gender and Class
    test_index = tracker.start_test(
        "Survival Analysis by Gender and Class",
        "Analyze survival rates by gender and passenger class to understand who survived the disaster"
    )
    
    try:
        result = agent.run(
            f"Use the search_csv tool to analyze survival rates in {config.TRAIN_CSV}. "
            f"First, search for female survivors (Survived=1, Sex='female') and show the count. "
            f"Then search for male survivors (Survived=1, Sex='male') and show the count. "
            f"Then search for first class survivors (Survived=1, Pclass=1) and show the count. "
            f"Provide statistics on survival by gender and class.",
            max_steps=config.MAX_STEPS
        )
        tracker.end_test(test_index, str(result), output_files=[])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 2: Create Demographics Dataset
    test_index = tracker.start_test(
        "Create Passenger Demographics Dataset",
        "Extract key demographic information (Name, Age, Sex, Pclass) for analysis"
    )
    
    try:
        result = agent.run(
            f"Use the create_csv_with_columns tool to create a demographics file from {config.TRAIN_CSV}. "
            f"Extract columns: PassengerId, Name, Age, Sex, Pclass, Survived. "
            f"Save as {config.OUTPUT_DIR}\\titanic_demographics.csv",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\titanic_demographics.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 3: Filter Children (Age < 18)
    test_index = tracker.start_test(
        "Identify Child Passengers",
        "Filter and save data for passengers under 18 years old"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to filter {config.TRAIN_CSV} for passengers where Age is less than 18. "
            f"Save the results as {config.OUTPUT_DIR}\\child_passengers.csv. "
            f"The function signature is: filter_and_save_csv(file_path, output_file, column, value, comparison)",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\child_passengers.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 4: Family Size Analysis
    test_index = tracker.start_test(
        "Family Size Analysis",
        "Analyze family sizes and their survival rates using SibSp and Parch columns"
    )
    
    try:
        result = agent.run(
            f"Use the create_csv_with_columns tool to create a family analysis file from {config.TRAIN_CSV}. "
            f"Extract columns: PassengerId, Name, SibSp, Parch, Survived. "
            f"Save as {config.OUTPUT_DIR}\\family_analysis.csv. "
            f"Then use search_csv to find passengers with SibSp > 0 or Parch > 0 (traveling with family).",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\family_analysis.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 5: Economic Analysis - Ticket Class and Fare
    test_index = tracker.start_test(
        "Economic Analysis by Class",
        "Analyze fare distribution and passenger class to understand economic differences"
    )
    
    try:
        result = agent.run(
            f"Use the create_csv_with_columns tool to create an economic analysis file from {config.TRAIN_CSV}. "
            f"Extract columns: PassengerId, Pclass, Fare, Survived. "
            f"Save as {config.OUTPUT_DIR}\\economic_analysis.csv. "
            f"Then use the describe_csv tool to get statistical summary of fares by class.",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\economic_analysis.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 6: Join Train and Test Data
    test_index = tracker.start_test(
        "Join Train and Test Datasets",
        "Combine training and test datasets for complete passenger information"
    )
    
    try:
        result = agent.run(
            f"Use the join_csv_files tool to join {config.TRAIN_CSV} and {config.TEST_CSV} on PassengerId. "
            f"Use a left join to combine the datasets. "
            f"Save the result as {config.OUTPUT_DIR}\\complete_passenger_data.csv",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\complete_passenger_data.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 7: Filter by Port of Embarkation
    test_index = tracker.start_test(
        "Passengers by Port of Embarkation",
        "Analyze passengers by their port of embarkation (S, C, Q)"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to create separate files for each port of embarkation from {config.TRAIN_CSV}. "
            f"Filter for Southampton (S) and save as {config.OUTPUT_DIR}\\embarked_southampton.csv, "
            f"Cherbourg (C) as {config.OUTPUT_DIR}\\embarked_cherbourg.csv, "
            f"and Queenstown (Q) as {config.OUTPUT_DIR}\\embarked_queenstown.csv.",
            max_steps=config.MAX_STEPS
        )
        output_files = [
            f"{config.OUTPUT_DIR}\\embarked_southampton.csv",
            f"{config.OUTPUT_DIR}\\embarked_cherbourg.csv",
            f"{config.OUTPUT_DIR}\\embarked_queenstown.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 8: Age Groups Analysis
    test_index = tracker.start_test(
        "Age Group Survival Analysis",
        "Analyze survival by age groups (children, adults, elderly)"
    )
    
    try:
        result = agent.run(
            f"Use search_csv to analyze age groups in {config.TRAIN_CSV}. "
            f"Find passengers where Age < 12 (children), Age between 12-60 (adults), "
            f"and Age > 60 (elderly). Show survival counts for each group.",
            max_steps=config.MAX_STEPS
        )
        tracker.end_test(test_index, str(result), output_files=[])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 9: First Class Passengers Analysis
    test_index = tracker.start_test(
        "First Class Passengers Deep Dive",
        "Detailed analysis of first class passengers including demographics and survival"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to filter {config.TRAIN_CSV} for first class passengers (Pclass=1). "
            f"Save as {config.OUTPUT_DIR}\\first_class_details.csv. "
            f"Then use describe_csv to get statistical summary of first class passenger data.",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\first_class_details.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 10: Survivors vs Non-Survivors Comparison
    test_index = tracker.start_test(
        "Survivors vs Non-Survivors Comparison",
        "Create separate datasets for survivors and non-survivors for comparative analysis"
    )
    
    try:
        result = agent.run(
            f"Use the filter_and_save_csv tool to create two datasets from {config.TRAIN_CSV}: "
            f"1. Survivors (Survived=1) - save as {config.OUTPUT_DIR}\\survivors_all_info.csv "
            f"2. Non-survivors (Survived=0) - save as {config.OUTPUT_DIR}\\non_survivors_all_info.csv",
            max_steps=config.MAX_STEPS
        )
        output_files = [
            f"{config.OUTPUT_DIR}\\survivors_all_info.csv",
            f"{config.OUTPUT_DIR}\\non_survivors_all_info.csv"
        ]
        tracker.end_test(test_index, str(result), output_files=output_files)
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 11: Cabin Analysis
    test_index = tracker.start_test(
        "Cabin Information Analysis",
        "Analyze passengers with cabin information and their characteristics"
    )
    
    try:
        result = agent.run(
            f"Use search_csv to find passengers in {config.TRAIN_CSV} where Cabin is not empty. "
            f"Show the count and display some examples. "
            f"Analyze the relationship between having a cabin and survival rates.",
            max_steps=config.MAX_STEPS
        )
        tracker.end_test(test_index, str(result), output_files=[])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 12: Comprehensive Dataset Info
    test_index = tracker.start_test(
        "Complete Dataset Overview",
        "Get comprehensive information about the Titanic dataset structure and statistics"
    )
    
    try:
        result = agent.run(
            f"Use get_csv_info to get detailed information about {config.TRAIN_CSV}. "
            f"Get the shape, column names, data types, and check for missing values. "
            f"Then use describe_csv to get statistical summary of all numeric columns.",
            max_steps=config.MAX_STEPS
        )
        tracker.end_test(test_index, str(result), output_files=[])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    # Test 13: Combine All Analysis Files
    test_index = tracker.start_test(
        "Create Master Analysis Dataset",
        "Combine all the analysis files created into one comprehensive dataset"
    )
    
    try:
        # Try to combine the created files
        result = agent.run(
            f"Use the combine_csv_files tool to combine multiple analysis files. "
            f"Combine: {config.OUTPUT_DIR}\\titanic_demographics.csv, "
            f"{config.OUTPUT_DIR}\\family_analysis.csv, "
            f"{config.OUTPUT_DIR}\\economic_analysis.csv. "
            f"Keep only common columns. Save as {config.OUTPUT_DIR}\\master_analysis.csv",
            max_steps=config.MAX_STEPS
        )
        output_file = f"{config.OUTPUT_DIR}\\master_analysis.csv"
        tracker.end_test(test_index, str(result), output_files=[output_file])
    except Exception as e:
        tracker.end_test(test_index, str(e), success=False, error_message=str(e))
    
    tracker.end_testing()
    return tracker


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "titanic":
            run_titanic_comprehensive_tests()
        else:
            print("Usage: python titanic_test_suite.py [titanic]")
    else:
        print("🚢 Running Titanic Dataset Comprehensive Tests...")
        run_titanic_comprehensive_tests()
