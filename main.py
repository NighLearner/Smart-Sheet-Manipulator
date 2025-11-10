# ================================================================================
# FILE 8: main.py
# ================================================================================
"""
Main entry point for the CSV manipulator application.
"""
from agent.enhanced_csv_agent_v2 import run_with_data_inspection_v2
from examples.test_tracker import run_basic_tests_with_tracking, run_comprehensive_tests_with_tracking
from examples.titanic_test_suite import run_titanic_comprehensive_tests
from dynamic_prompt_template import create_smart_prompt_template
from enhanced_test_tracker import run_enhanced_basic_tests
import config


def interactive_mode():
    """
    Run the agent in interactive mode where users can input queries.
    """
    from agent import get_agent
    
    print("\n" + "="*80)
    print("CSV MANIPULATOR - Interactive Mode")
    print("="*80)
    print("Type your CSV manipulation queries below.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    agent = get_agent()
    
    while True:
        try:
            query = input("\n📝 Enter your query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🤖 Processing...")
            result = agent.run(query, max_steps=config.MAX_STEPS)
            print(f"\n✅ Result:\n{result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def enhanced_interactive_mode():
    """
    Run the enhanced agent in interactive mode with dynamic dataset information.
    """
    print("\n" + "="*80)
    print("CSV MANIPULATOR - Enhanced Interactive Mode V2")
    print("="*80)
    print("Enhanced mode automatically includes df.info() and df.describe() for better accuracy.")
    print("All CSV output files will be saved in the 'answers' directory.")
    print("Type your CSV manipulation queries below.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            query = input("\n📝 Enter your query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🤖 Processing with dynamic dataset information...")
            
            # Create dynamic prompt with dataset information
            enhanced_query = create_smart_prompt_template(query)
            
            # Use the enhanced agent directly instead of run_with_data_inspection_v2
            from agent.enhanced_csv_agent_v2 import get_enhanced_agent_v2
            agent = get_enhanced_agent_v2()
            result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
            
            print(f"\n✅ Result:\n{result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def main():
    """
    Main function to run the application.
    """
    print("\n" + "="*80)
    print("CSV MANIPULATOR WITH AI AGENT")
    print("="*80)
    print("\nChoose a mode:")
    print("1. Run enhanced basic tests with dynamic prompts")
    print("2. Run comprehensive tests with tracking")
    print("3. Run Titanic dataset comprehensive tests")
    print("4. Interactive mode")
    print("5. Enhanced Interactive mode V2 (with DataFrame returns and 3-step limit)")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\nRunning enhanced basic tests with dynamic prompts...")
        run_enhanced_basic_tests()
    elif choice == "2":
        print("\nRunning comprehensive tests with detailed tracking...")
        run_comprehensive_tests_with_tracking()
    elif choice == "3":
        print("\nRunning Titanic dataset comprehensive tests...")
        run_titanic_comprehensive_tests()
    elif choice == "4":
        interactive_mode()
    elif choice == "5":
        enhanced_interactive_mode()
    elif choice == "6":
        print("\nGoodbye!")
    else:
        print("\nInvalid choice. Please run again.")


if __name__ == "__main__":
    main()
