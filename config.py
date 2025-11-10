# ================================================================================
# FILE 1: config.py
# ================================================================================
"""
Configuration settings for the CSV manipulator agent.
"""
import os

# Model Configuration
MODEL_ID = "ollama/qwen2.5-coder:3b"  # Optimized quantized model for better performance
MODEL_API_KEY = "ollama"

# File Paths (Update these for your environment)
DATA_DIR = r"D:\sheet_manipulator"
TRAIN_CSV = os.path.join(DATA_DIR, "train.csv")
TEST_CSV = os.path.join(DATA_DIR, "test.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "answers")  # answers folder in app2 directory

# Agent Configuration
MAX_STEPS = 3  # Reduced to 3 steps for app2
ADD_BASE_TOOLS = False

# Display Settings
DISPLAY_MAX_COLUMNS = None
DISPLAY_WIDTH = None
DISPLAY_MAX_COLWIDTH = 50
