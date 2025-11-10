# ================================================================================
# FILE: verify_setup.py
# ================================================================================
"""
Verification script to confirm app2 setup with answers directory.
"""
import os
import sys

def verify_setup():
    """Verify that app2 is properly set up with answers directory."""
    print("="*80)
    print("APP2 SETUP VERIFICATION")
    print("="*80)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"App2 directory: {current_dir}")
    
    # Check answers directory
    answers_dir = os.path.join(current_dir, "answers")
    print(f"Answers directory: {answers_dir}")
    print(f"Answers directory exists: {os.path.exists(answers_dir)}")
    
    if os.path.exists(answers_dir):
        files = os.listdir(answers_dir)
        print(f"Files in answers directory: {len(files)}")
        for file in files:
            file_path = os.path.join(answers_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"  - {file} ({file_size} bytes)")
    
    # Check key files
    key_files = [
        "main.py",
        "config.py", 
        "agent/enhanced_csv_agent_v2.py",
        "tools/basic_tools.py",
        "tools/advanced_tools.py",
        "tools/enhanced_tools.py"
    ]
    
    print(f"\nKey files verification:")
    for file in key_files:
        file_path = os.path.join(current_dir, file)
        exists = os.path.exists(file_path)
        print(f"  - {file}: {'OK' if exists else 'MISSING'}")
    
    # Check config
    try:
        sys.path.append(current_dir)
        import config
        print(f"\nConfiguration:")
        print(f"  - MAX_STEPS: {config.MAX_STEPS}")
        print(f"  - OUTPUT_DIR: {config.OUTPUT_DIR}")
        print(f"  - TRAIN_CSV: {config.TRAIN_CSV}")
        print(f"  - TEST_CSV: {config.TEST_CSV}")
    except Exception as e:
        print(f"  - Config error: {e}")
    
    print("\n" + "="*80)
    print("SETUP VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    verify_setup()
