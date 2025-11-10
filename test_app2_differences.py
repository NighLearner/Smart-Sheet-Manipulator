# ================================================================================
# FILE: test_app2_differences.py
# ================================================================================
"""
Test script to demonstrate the differences between app and app2.
"""
import sys
import os

# Add app2 to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app2'))

from agent.enhanced_csv_agent_v2 import run_with_data_inspection_v2, final_answer
import pandas as pd

def test_comprehensive_question():
    """Test a comprehensive question that should get detailed analysis."""
    print("="*80)
    print("TESTING COMPREHENSIVE QUESTION")
    print("="*80)
    
    query = "What's the mean age of all passengers in the train.csv file? Save any analysis results to the answers directory."
    
    print(f"Query: {query}")
    print("\nProcessing with app2 (V2 agent)...")
    
    try:
        result = run_with_data_inspection_v2(query)
        print(f"\nResult:\n{result}")
    except Exception as e:
        print(f"Error: {e}")

def test_dataframe_request():
    """Test a DataFrame request that should return data directly."""
    print("\n" + "="*80)
    print("TESTING DATAFRAME REQUEST")
    print("="*80)
    
    query = "Show me the first 10 passengers from train.csv and save the result to answers/first_10_passengers.csv"
    
    print(f"Query: {query}")
    print("\nProcessing with app2 (V2 agent)...")
    
    try:
        result = run_with_data_inspection_v2(query)
        print(f"\nResult:\n{result}")
    except Exception as e:
        print(f"Error: {e}")

def test_final_answer_function():
    """Test the final_answer function with different data types."""
    print("\n" + "="*80)
    print("TESTING FINAL_ANSWER FUNCTION")
    print("="*80)
    
    # Test with DataFrame
    df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
    print("Testing with DataFrame:")
    print(final_answer(df))
    
    # Test with string
    print("\nTesting with string:")
    print(final_answer("This is a test string"))
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    print("\nTesting with empty DataFrame:")
    print(final_answer(empty_df))

def main():
    """Run all tests."""
    print("APP2 TESTING - Enhanced CSV Agent V2")
    print("Features:")
    print("- Tools return pandas DataFrames instead of strings")
    print("- Maximum 3 steps")
    print("- final_answer() function with try-catch blocks")
    print("- Comprehensive analysis for statistical questions")
    print("- Direct DataFrame returns for data requests")
    
    test_final_answer_function()
    test_comprehensive_question()
    test_dataframe_request()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
