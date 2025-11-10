# ================================================================================
# FILE: simple_test.py
# ================================================================================
"""
Simple test to verify answers directory functionality.
"""
import sys
import os

# Add app2 to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app2'))

from agent.enhanced_csv_agent_v2 import get_enhanced_agent_v2
import config

def simple_test():
    """Simple test without complex data inspection."""
    print("="*80)
    print("SIMPLE ANSWERS DIRECTORY TEST")
    print("="*80)
    
    # Check answers directory
    answers_dir = config.OUTPUT_DIR
    print(f"Answers directory: {answers_dir}")
    print(f"Directory exists: {os.path.exists(answers_dir)}")
    
    if not os.path.exists(answers_dir):
        os.makedirs(answers_dir, exist_ok=True)
        print("Created answers directory")
    
    # Get agent
    agent = get_enhanced_agent_v2()
    
    # Simple query
    query = "Create a CSV file with the first 3 passengers from train.csv and save it as answers/simple_test.csv"
    
    print(f"\nQuery: {query}")
    print("Processing...")
    
    try:
        result = agent.run(query, max_steps=3)
        print(f"\nResult:\n{result}")
        
        # Check if file was created
        test_file = os.path.join(answers_dir, "simple_test.csv")
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"\nSUCCESS: Test file created!")
            print(f"File: {test_file}")
            print(f"Size: {file_size} bytes")
        else:
            print(f"\nFAILED: Test file not found: {test_file}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_test()
