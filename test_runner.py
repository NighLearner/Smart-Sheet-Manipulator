"""
Test runner for data manipulation operations.
Creates test datasets and runs comprehensive tests with automatic metadata injection.
"""
import pandas as pd
import os
from pathlib import Path
from agent import get_agent
from utils import enhance_query_with_metadata
import config


# Setup directories
APP_DIR = Path(__file__).resolve().parent
STUDENT_DIR = APP_DIR / "student"
TITANIC_DIR = APP_DIR / "titanic"
RESULTS_DIR = APP_DIR / "results"

# Create directories
STUDENT_DIR.mkdir(exist_ok=True)
TITANIC_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)




def create_student_datasets():
    """Create sample student datasets for testing."""
    print("Creating student datasets...")
    
    # Dataset 1: Student Information
    student_info = pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [20, 21, 19, 22, 20],
        'gender': ['F', 'M', 'M', 'F', 'F'],
        'grade': ['A', 'B', 'A', 'A', 'B']
    })
    student_info.to_csv(STUDENT_DIR / "student_info.csv", index=False)
    print(f"  Created: {STUDENT_DIR / 'student_info.csv'}")
    
    # Dataset 2: Student Grades
    student_grades = pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'math_score': [95, 85, 92, 88, 90],
        'science_score': [90, 80, 95, 85, 92],
        'english_score': [88, 82, 90, 91, 87]
    })
    student_grades.to_csv(STUDENT_DIR / "student_grades.csv", index=False)
    print(f"  Created: {STUDENT_DIR / 'student_grades.csv'}")
    
    # Dataset 3: Student Attendance
    student_attendance = pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5],
        'days_present': [180, 175, 182, 178, 180],
        'days_absent': [5, 10, 3, 7, 5],
        'attendance_rate': [0.97, 0.95, 0.98, 0.96, 0.97]
    })
    student_attendance.to_csv(STUDENT_DIR / "student_attendance.csv", index=False)
    print(f"  Created: {STUDENT_DIR / 'student_attendance.csv'}")
    
    # Dataset 4: Student Courses
    student_courses = pd.DataFrame({
        'student_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        'course': ['Math', 'Science', 'Math', 'English', 'Science', 'Math', 'English', 'Science', 'Math', 'English'],
        'credits': [3, 4, 3, 3, 4, 3, 3, 4, 3, 3],
        'semester': ['Fall', 'Fall', 'Fall', 'Spring', 'Fall', 'Spring', 'Fall', 'Spring', 'Fall', 'Spring']
    })
    student_courses.to_csv(STUDENT_DIR / "student_courses.csv", index=False)
    print(f"  Created: {STUDENT_DIR / 'student_courses.csv'}")
    
    print("Student datasets created successfully!\n")


def setup_titanic_dataset():
    """Copy titanic dataset to titanic folder if it exists."""
    print("Setting up titanic dataset...")
    
    train_csv = APP_DIR / "train.csv"
    test_csv = APP_DIR / "test.csv"
    
    if train_csv.exists():
        import shutil
        shutil.copy(train_csv, TITANIC_DIR / "train.csv")
        print(f"  Copied: {TITANIC_DIR / 'train.csv'}")
    
    if test_csv.exists():
        import shutil
        shutil.copy(test_csv, TITANIC_DIR / "test.csv")
        print(f"  Copied: {TITANIC_DIR / 'test.csv'}")
    
    print("Titanic dataset setup complete!\n")


def run_test_case(test_name: str, query: str, file_paths: list = None):
    """
    Run a single test case with metadata injection.
    
    Args:
        test_name: Name of the test case
        query: Query to execute
        file_paths: List of file paths to include metadata for (optional, auto-detected if None)
    """
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Query: {query}")
    print(f"\nProcessing...")
    
    try:
        # Enhance query with metadata (auto-detects file paths if not provided)
        enhanced_query = enhance_query_with_metadata(query, file_paths=file_paths, auto_detect=True)
        
        # Get agent and run query
        agent = get_agent()
        result = agent.run(enhanced_query, max_steps=config.MAX_STEPS)
        
        print(f"\n✅ Result:")
        print(result)
        print(f"\n{'='*80}\n")
        
        return True, result
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*80}\n")
        return False, str(e)


def run_student_tests():
    """Run test cases on student datasets."""
    print("\n" + "="*80)
    print("RUNNING STUDENT DATASET TESTS")
    print("="*80 + "\n")
    
    student_info = str(STUDENT_DIR / "student_info.csv")
    student_grades = str(STUDENT_DIR / "student_grades.csv")
    student_attendance = str(STUDENT_DIR / "student_attendance.csv")
    student_courses = str(STUDENT_DIR / "student_courses.csv")
    results_dir = str(RESULTS_DIR / "student")
    
    tests = [
        # Test 1: Select columns
        (
            "Select Columns - Student Info",
            f"Select name, age, and gender columns from {student_info} and save to {results_dir}/selected_columns.csv",
            [student_info]
        ),
        
        # Test 2: Create column
        (
            "Create Column - Total Score",
            f"Create a new column total_score as math_score + science_score + english_score in {student_grades} and save to {results_dir}/grades_with_total.csv",
            [student_grades]
        ),
        
        # Test 3: Normalize column
        (
            "Normalize Column - Math Score",
            f"Normalize the math_score column in {student_grades} using min_max and save to {results_dir}/grades_normalized.csv",
            [student_grades]
        ),
        
        # Test 4: One-hot encode
        (
            "One-Hot Encode - Gender",
            f"One-hot encode the gender column in {student_info} and save to {results_dir}/student_encoded.csv",
            [student_info]
        ),
        
        # Test 5: Label encode
        (
            "Label Encode - Grade",
            f"Label encode the grade column in {student_info} and save to {results_dir}/student_label_encoded.csv",
            [student_info]
        ),
        
        # Test 6: Filter rows
        (
            "Filter Rows - Age > 20",
            f"Filter rows where age > 20 from {student_info} and save to {results_dir}/students_above_20.csv",
            [student_info]
        ),
        
        # Test 7: Combine files (vertical)
        (
            "Combine Files - Vertical",
            f"Combine {student_info} and {student_grades} horizontally and save to {results_dir}/combined_student_data.csv",
            [student_info, student_grades]
        ),
        
        # Test 8: Join files
        (
            "Join Files - Student Info and Grades",
            f"Join {student_info} and {student_grades} on student_id and save to {results_dir}/joined_student_data.csv",
            [student_info, student_grades]
        ),
        
        # Test 9: Multiple operations
        (
            "Multiple Operations - Filter and Select",
            f"Filter rows where gender equals 'F' from {student_info} and save to {results_dir}/female_students.csv, then select name and age columns from {results_dir}/female_students.csv and save to {results_dir}/female_students_selected.csv",
            [student_info]
        ),
    ]
    
    # Create results directory
    Path(results_dir).mkdir(parents=True, exist_ok=True)
    
    results = []
    for test_name, query, file_paths in tests:
        success, result = run_test_case(test_name, query, file_paths)
        results.append((test_name, success, result))
    
    # Print summary
    print("\n" + "="*80)
    print("STUDENT TESTS SUMMARY")
    print("="*80)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    for test_name, success, _ in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")
    print("="*80 + "\n")
    
    return results


def run_titanic_tests():
    """Run test cases on titanic dataset."""
    print("\n" + "="*80)
    print("RUNNING TITANIC DATASET TESTS")
    print("="*80 + "\n")
    
    train_csv = str(TITANIC_DIR / "train.csv")
    test_csv = str(TITANIC_DIR / "test.csv")
    results_dir = str(RESULTS_DIR / "titanic")
    
    # Check if titanic dataset exists
    if not os.path.exists(train_csv):
        print(f"❌ Titanic dataset not found at {train_csv}")
        print("Please ensure train.csv exists in the app directory.")
        return []
    
    tests = [
        # Test 1: Select columns
        (
            "Select Columns - Passenger Info",
            f"Select Name, Age, Sex, and Survived columns from {train_csv} and save to {results_dir}/passenger_info.csv",
            [train_csv]
        ),
        
        # Test 2: Create column
        (
            "Create Column - Family Size",
            f"Create a new column family_size as SibSp + Parch + 1 in {train_csv} and save to {results_dir}/titanic_family_size.csv",
            [train_csv]
        ),
        
        # Test 3: Normalize column
        (
            "Normalize Column - Age",
            f"Normalize the Age column in {train_csv} using min_max and save to {results_dir}/titanic_age_normalized.csv",
            [train_csv]
        ),
        
        # Test 4: Normalize column (z-score)
        (
            "Normalize Column - Fare (Z-Score)",
            f"Normalize the Fare column in {train_csv} using z_score and save to {results_dir}/titanic_fare_standardized.csv",
            [train_csv]
        ),
        
        # Test 5: One-hot encode
        (
            "One-Hot Encode - Sex",
            f"One-hot encode the Sex column in {train_csv} and save to {results_dir}/titanic_sex_encoded.csv",
            [train_csv]
        ),
        
        # Test 6: One-hot encode multiple columns
        (
            "One-Hot Encode - Embarked and Pclass",
            f"One-hot encode the Embarked and Pclass columns in {train_csv} and save to {results_dir}/titanic_multi_encoded.csv",
            [train_csv]
        ),
        
        # Test 7: Label encode
        (
            "Label Encode - Embarked",
            f"Label encode the Embarked column in {train_csv} and save to {results_dir}/titanic_embarked_encoded.csv",
            [train_csv]
        ),
        
        # Test 8: Filter rows
        (
            "Filter Rows - Survived",
            f"Filter rows where Survived equals 1 from {train_csv} and save to {results_dir}/titanic_survivors.csv",
            [train_csv]
        ),
        
        # Test 9: Filter rows - Age
        (
            "Filter Rows - Age > 30",
            f"Filter rows where Age > 30 from {train_csv} and save to {results_dir}/titanic_adults.csv",
            [train_csv]
        ),
        
        # Test 10: Filter rows - Sex
        (
            "Filter Rows - Female Passengers",
            f"Filter rows where Sex equals 'female' from {train_csv} and save to {results_dir}/titanic_females.csv",
            [train_csv]
        ),
        
        # Test 11: Combine files (if test.csv exists)
        (
            "Combine Files - Train and Test",
            f"Combine {train_csv} and {test_csv} vertically and save to {results_dir}/titanic_combined.csv",
            [train_csv, test_csv] if os.path.exists(test_csv) else [train_csv]
        ) if os.path.exists(test_csv) else None,
        
        # Test 12: Join files (if both exist)
        (
            "Join Files - Train and Test",
            f"Join {train_csv} and {test_csv} on PassengerId and save to {results_dir}/titanic_joined.csv",
            [train_csv, test_csv] if os.path.exists(test_csv) else [train_csv]
        ) if os.path.exists(test_csv) else None,
        
        # Test 13: Multiple operations
        (
            "Multiple Operations - Filter, Select, and Normalize",
            f"Filter rows where Pclass equals 1 from {train_csv} and save to {results_dir}/titanic_first_class.csv, then select Age, Fare, and Survived columns from {results_dir}/titanic_first_class.csv and save to {results_dir}/titanic_first_class_selected.csv, then normalize the Fare column in {results_dir}/titanic_first_class_selected.csv using min_max and save to {results_dir}/titanic_first_class_final.csv",
            [train_csv]
        ),
    ]
    
    # Filter out None tests
    tests = [t for t in tests if t is not None]
    
    # Create results directory
    Path(results_dir).mkdir(parents=True, exist_ok=True)
    
    results = []
    for test_name, query, file_paths in tests:
        success, result = run_test_case(test_name, query, file_paths)
        results.append((test_name, success, result))
    
    # Print summary
    print("\n" + "="*80)
    print("TITANIC TESTS SUMMARY")
    print("="*80)
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    for test_name, success, _ in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")
    print("="*80 + "\n")
    
    return results


def main():
    """Main test runner."""
    print("\n" + "="*80)
    print("DATA MANIPULATION TEST RUNNER")
    print("="*80)
    print("\nThis test runner will:")
    print("1. Create student datasets")
    print("2. Setup titanic dataset")
    print("3. Run comprehensive tests with automatic metadata injection")
    print("4. Save all results to results/ folder")
    print("\n" + "="*80 + "\n")
    
    # Create test datasets
    create_student_datasets()
    setup_titanic_dataset()
    
    # Run tests
    print("\nStarting tests...\n")
    
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
    
    print(f"Results saved to:")
    print(f"  - {RESULTS_DIR / 'student'}")
    print(f"  - {RESULTS_DIR / 'titanic'}")
    print("\n")


if __name__ == "__main__":
    main()

