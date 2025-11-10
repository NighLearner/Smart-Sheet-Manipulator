# ================================================================================
# FILE 8: main.py
# ================================================================================
"""
Main entry point for the CSV manipulator application.
"""
from pathlib import Path

from agent.enhanced_csv_agent import run_with_data_inspection
from examples.test_tracker import run_basic_tests_with_tracking, run_comprehensive_tests_with_tracking
from examples.titanic_test_suite import run_titanic_comprehensive_tests
import config


APP_DIR = Path(__file__).resolve().parent
config.TRAIN_CSV = str(APP_DIR / "train.csv")
config.TEST_CSV = str(APP_DIR / "test.csv")
config.OUTPUT_DIR = str(APP_DIR / "resultant")
Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


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
    Run the enhanced agent in interactive mode with automatic df.info() and df.describe() integration.
    """
    print("\n" + "="*80)
    print("CSV MANIPULATOR - Enhanced Interactive Mode")
    print("="*80)
    print("Enhanced mode automatically includes df.info() and df.describe() for better accuracy.")
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
            
            print("\n🤖 Processing with enhanced data inspection...")
            result = run_with_data_inspection(query, max_steps=config.MAX_STEPS)
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
    print("1. Run basic tests with tracking")
    print("2. Run comprehensive tests with tracking")
    print("3. Run Titanic dataset comprehensive tests")
    print("4. Interactive mode")
    print("5. Enhanced Interactive mode (with automatic df.info() and df.describe())")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\nRunning basic tests with comprehensive tracking...")
        run_basic_tests_with_tracking()
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
