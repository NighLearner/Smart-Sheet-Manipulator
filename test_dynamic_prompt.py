# ================================================================================
# FILE: test_dynamic_prompt.py
# ================================================================================
"""
Test script to verify the dynamic prompt template functionality.
"""
import sys
import os

# Add app2 to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app2'))

from dynamic_prompt_template import create_dynamic_prompt_template, create_simple_dataset_info
from agent.enhanced_csv_agent_v2 import get_enhanced_agent_v2
import config

def test_dynamic_prompt_template():
    """Test the dynamic prompt template."""
    print("="*80)
    print("TESTING DYNAMIC PROMPT TEMPLATE")
    print("="*80)
    
    # Test query
    query = "What's the mean age of passengers?"
    
    print(f"Original query: {query}")
    print("\nCreating dynamic prompt template...")
    
    # Create enhanced prompt
    enhanced_query = create_dynamic_prompt_template(query)
    
    print(f"\nEnhanced query length: {len(enhanced_query)} characters")
    print(f"Enhanced query preview (first 500 chars):\n{enhanced_query[:500]}...")
    
    return enhanced_query

def test_agent_with_dynamic_prompt():
    """Test the agent with dynamic prompt."""
    print("\n" + "="*80)
    print("TESTING AGENT WITH DYNAMIC PROMPT")
    print("="*80)
    
    # Test query that was failing before
    query = "Search for female survivors and show the count"
    
    print(f"Query: {query}")
    print("Creating dynamic prompt...")
    
    # Create enhanced prompt
    enhanced_query = create_dynamic_prompt_template(query)
    
    print("Running agent with dynamic prompt...")
    
    try:
        agent = get_enhanced_agent_v2()
        result = agent.run(enhanced_query, max_steps=3)
        print(f"\nResult:\n{result}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_simple_dataset_info():
    """Test the simple dataset info function."""
    print("\n" + "="*80)
    print("TESTING SIMPLE DATASET INFO")
    print("="*80)
    
    query = "Show me passenger data"
    dataset_path = config.TRAIN_CSV
    
    print(f"Query: {query}")
    print(f"Dataset: {dataset_path}")
    
    enhanced_query = create_simple_dataset_info(query, dataset_path)
    
    print(f"\nEnhanced query:\n{enhanced_query}")

def main():
    """Run all tests."""
    print("DYNAMIC PROMPT TEMPLATE TESTING")
    print("Features:")
    print("- Automatic df.info() and df.describe() inclusion")
    print("- Dataset metadata and structure information")
    print("- Tool signatures and guidelines")
    print("- Prevents data type and parameter errors")
    
    test_dynamic_prompt_template()
    test_simple_dataset_info()
    test_agent_with_dynamic_prompt()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
