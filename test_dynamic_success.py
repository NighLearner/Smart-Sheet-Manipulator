# ================================================================================
# FILE: test_dynamic_success.py
# ================================================================================
"""
Test script to demonstrate successful dynamic prompt template usage.
"""
import sys
import os

# Add app2 to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app2'))

from dynamic_prompt_template import create_smart_prompt_template
from agent.enhanced_csv_agent_v2 import get_enhanced_agent_v2
import config

def test_successful_query():
    """Test a query that should work correctly with dynamic prompt."""
    print("="*80)
    print("TESTING SUCCESSFUL QUERY WITH DYNAMIC PROMPT")
    print("="*80)
    
    # Test query that should work well with the dataset info
    query = "Find all female passengers from train.csv and save to answers/female_passengers.csv"
    
    print(f"Query: {query}")
    print("Creating dynamic prompt...")
    
    # Create enhanced prompt
    enhanced_query = create_smart_prompt_template(query)
    
    print("Running agent with dynamic prompt...")
    
    try:
        agent = get_enhanced_agent_v2()
        result = agent.run(enhanced_query, max_steps=3)
        print(f"\nResult:\n{result}")
        
        # Check if file was created
        output_file = os.path.join(config.OUTPUT_DIR, "female_passengers.csv")
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"\nSUCCESS: File created!")
            print(f"File: {output_file}")
            print(f"Size: {file_size} bytes")
        else:
            print(f"\nFile not found: {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")

def test_statistical_query():
    """Test a statistical query."""
    print("\n" + "="*80)
    print("TESTING STATISTICAL QUERY")
    print("="*80)
    
    query = "What's the mean age of passengers in train.csv?"
    
    print(f"Query: {query}")
    
    try:
        enhanced_query = create_smart_prompt_template(query)
        agent = get_enhanced_agent_v2()
        result = agent.run(enhanced_query, max_steps=3)
        print(f"\nResult:\n{result}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests."""
    print("DYNAMIC PROMPT SUCCESS TESTING")
    print("Features:")
    print("- Automatic df.info() and df.describe() inclusion")
    print("- Correct data type awareness")
    print("- Proper column name usage")
    print("- Accurate tool parameter usage")
    
    test_successful_query()
    test_statistical_query()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
