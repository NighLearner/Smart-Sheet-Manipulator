"""
Simple data manipulation tool for CSV and Excel files.
"""
from pathlib import Path
from agent import get_agent
from utils import enhance_query_with_metadata
from test_runner import (
    create_student_datasets,
    setup_titanic_dataset,
    run_student_tests,
    run_titanic_tests
)
import config


# Setup paths
APP_DIR = Path(__file__).resolve().parent
config.OUTPUT_DIR = str(APP_DIR / "resultant")
Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def interactive_mode():
    """
    Run the agent in interactive mode for data manipulation.
    """
    print("\n" + "="*80)
    print("DATA MANIPULATION TOOL - Interactive Mode")
    print("="*80)
    print("Transform CSV and Excel files using natural language.")
    print("Examples:")
    print("  - 'Select Name and Age columns from data.csv and save to output.csv'")
    print("  - 'Create a new column Total as Price + Tax in data.csv and save to output.csv'")
    print("  - 'Normalize the Age column in data.csv using min_max and save to output.csv'")
    print("  - 'One-hot encode the Category column in data.csv and save to output.csv'")
    print("  - 'Filter rows where Age > 30 from data.csv and save to output.csv'")
    print("  - 'Combine data1.csv and data2.csv vertically and save to output.csv'")
    print("Type 'exit' or 'quit' to stop.\n")
    
    agent = get_agent()
    
    while True:
        try:
            query = input("\n📝 Enter your manipulation query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🤖 Processing with metadata injection...")
            
            # Enhance query with automatic metadata injection
            enhanced_query = enhance_query_with_metadata(query, auto_detect=True)
            
            # Run the enhanced query
            result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
            print(f"\n✅ Result:\n{result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def run_all_tests():
    """Run all test suites (student and titanic)."""
    print("\n" + "="*80)
    print("RUNNING ALL TESTS")
    print("="*80 + "\n")
    
    # Create test datasets
    create_student_datasets()
    setup_titanic_dataset()
    
    # Run tests
    print("\nStarting all tests...\n")
    
    student_results = run_student_tests()
    titanic_results = run_titanic_tests()
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    student_passed = sum(1 for _, success, _ in student_results if success)
    titanic_passed = sum(1 for _, success, _ in titanic_results if success)
    total_passed = student_passed + titanic_passed
    total_tests = len(student_results) + len(titanic_results)
    
    print(f"Student Tests: {student_passed}/{len(student_results)} passed")
    print(f"Titanic Tests: {titanic_passed}/{len(titanic_results)} passed")
    print(f"Total: {total_passed}/{total_tests} passed")
    print("="*80 + "\n")
    
    from test_runner import RESULTS_DIR
    print(f"Results saved to:")
    print(f"  - {RESULTS_DIR / 'student'}")
    print(f"  - {RESULTS_DIR / 'titanic'}")
    print("\n")


def run_student_tests_only():
    """Run only student dataset tests."""
    print("\n" + "="*80)
    print("RUNNING STUDENT TESTS ONLY")
    print("="*80 + "\n")
    
    # Create test datasets
    create_student_datasets()
    
    # Run tests
    student_results = run_student_tests()
    
    # Summary
    print("\n" + "="*80)
    print("STUDENT TESTS SUMMARY")
    print("="*80)
    student_passed = sum(1 for _, success, _ in student_results if success)
    print(f"Passed: {student_passed}/{len(student_results)}")
    print("="*80 + "\n")
    
    from test_runner import RESULTS_DIR
    print(f"Results saved to: {RESULTS_DIR / 'student'}")
    print("\n")


def run_titanic_tests_only():
    """Run only titanic dataset tests."""
    print("\n" + "="*80)
    print("RUNNING TITANIC TESTS ONLY")
    print("="*80 + "\n")
    
    # Setup titanic dataset
    setup_titanic_dataset()
    
    # Run tests
    titanic_results = run_titanic_tests()
    
    # Summary
    print("\n" + "="*80)
    print("TITANIC TESTS SUMMARY")
    print("="*80)
    titanic_passed = sum(1 for _, success, _ in titanic_results if success)
    print(f"Passed: {titanic_passed}/{len(titanic_results)}")
    print("="*80 + "\n")
    
    from test_runner import RESULTS_DIR
    print(f"Results saved to: {RESULTS_DIR / 'titanic'}")
    print("\n")


def main():
    """
    Main function to run the application.
    """
    print("\n" + "="*80)
    print("DATA MANIPULATION TOOL")
    print("="*80)
    print("\nChoose an option:")
    print("1. Interactive mode")
    print("2. Run all tests (Student + Titanic)")
    print("3. Run student tests only")
    print("4. Run titanic tests only")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        run_all_tests()
    elif choice == "3":
        run_student_tests_only()
    elif choice == "4":
        run_titanic_tests_only()
    elif choice == "5":
        print("\nGoodbye!")
    else:
        print("\nInvalid choice. Please run again.")


if __name__ == "__main__":
    main()
