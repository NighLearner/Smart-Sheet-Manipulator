"""
Configuration settings for the data manipulation agent.
"""
import os

# Model Configuration
MODEL_ID = "ollama/qwen2.5-coder:3b"
MODEL_API_KEY = "ollama"

# File Paths (automatically configured in main.py)
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(DATA_DIR, "resultant")

# Agent Configuration
MAX_STEPS = 3  # Maximum steps for agent execution
ADD_BASE_TOOLS = False
