"""
Configuration settings for SuperFund Site Safety Checker.
Loads environment variables and provides centralized access to all settings.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
EMBEDDINGS_PATH = DATA_PATH / "embeddings"

# LLM Configuration
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Application Settings
APP_TITLE: str = os.getenv("APP_TITLE", "SuperFund Site Proximity Detector")
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Data Settings
SUPERFUND_DATA_FILE: str = os.getenv("DATA_PATH", "./data/raw/superfund_sites.csv")
POLICY_DATA_FILE: str = os.getenv("POLICY_DATA_PATH", "./data/raw/policies.csv")

# Safety Scoring Configuration
PROXIMITY_RADIUS_MILES: float = float(os.getenv("PROXIMITY_RADIUS_MILES", "50"))
SCORE_PENALTY_PER_SITE: int = int(os.getenv("SCORE_PENALTY_PER_SITE", "25"))
INITIAL_SCORE: int = int(os.getenv("INITIAL_SCORE", "100"))
MINIMUM_SCORE: int = 0

# Risk Level Thresholds
RISK_LEVELS = {
    100: "SAFE",
    75: "LOW",
    50: "MEDIUM",
    25: "HIGH",
    0: "CRITICAL"
}

# Layout Configuration
CHAT_WIDTH_PERCENT: int = 60
SIDEBAR_WIDTH_PERCENT: int = 40

# Session Configuration
SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

# Validate critical settings
def validate_config() -> bool:
    """Validate that all critical configuration is present."""
    if not OPENAI_API_KEY:
        print("WARNING: OPENAI_API_KEY not set. Please configure .env file.")
        return False
    return True
