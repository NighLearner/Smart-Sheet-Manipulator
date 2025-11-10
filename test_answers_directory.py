# ================================================================================
# FILE: test_answers_directory.py
# ================================================================================
"""
Test script to verify that CSV files are saved in the answers directory.
"""
import sys
import os

# Add app2 to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app2'))

from agent.enhanced_csv_agent_v2 import run_with_data_inspection_v2
import config

def test_answers_directory():
    """Test that CSV files are saved in the answers directory."""
    print("="*80)
    print("TESTING ANSWERS DIRECTORY")
    print("="*80)
    
    # Check if answers directory exists
    answers_dir = config.OUTPUT_DIR
    print(f"Answers directory: {answers_dir}")
    print(f"Directory exists: {os.path.exists(answers_dir)}")
    
    if not os.path.exists(answers_dir):
        print("Creating answers directory...")
        os.makedirs(answers_dir, exist_ok=True)
        print(f"Directory created: {os.path.exists(answers_dir)}")
    
    # Test creating a CSV file
    query = "Create a CSV file with the first 5 passengers from train.csv and save it as answers/test_passengers.csv"
    
    print(f"\nQuery: {query}")
    print("\nProcessing with app2 (V2 agent)...")
    
    try:
        result = run_with_data_inspection_v2(query)
        print(f"\nResult:\n{result}")
        
        # Check if file was created
        test_file = os.path.join(answers_dir, "test_passengers.csv")
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"\n✅ Test file created successfully!")
            print(f"File: {test_file}")
            print(f"Size: {file_size} bytes")
        else:
            print(f"\n❌ Test file not found: {test_file}")
            
    except Exception as e:
        print(f"Error: {e}")

def list_answers_directory():
    """List all files in the answers directory."""
    print("\n" + "="*80)
    print("ANSWERS DIRECTORY CONTENTS")
    print("="*80)
    
    answers_dir = config.OUTPUT_DIR
    
    if os.path.exists(answers_dir):
        files = os.listdir(answers_dir)
        if files:
            print(f"Found {len(files)} files in answers directory:")
            for file in files:
                file_path = os.path.join(answers_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"  - {file} ({file_size} bytes)")
        else:
            print("Answers directory is empty.")
    else:
        print("Answers directory does not exist.")

def main():
    """Run all tests."""
    print("ANSWERS DIRECTORY TESTING")
    print("Features:")
    print("- All CSV output files saved in app2/answers directory")
    print("- Automatic directory creation")
    print("- File verification")
    
    test_answers_directory()
    list_answers_directory()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
