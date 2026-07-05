"""
Mission 80 Coach
Global Configuration
Version: 2.0
"""

from pathlib import Path

# ---------------------------------------------------
# Project Information
# ---------------------------------------------------

APP_NAME = "Mission 80 Coach"
APP_VERSION = "2.0.0"
APP_OWNER = "Femi Fajemilo"

TARGET_WEIGHT = 80.0
START_WEIGHT = 95.0

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

ROOT_DIR = Path(__file__).parent

ASSETS_DIR = ROOT_DIR / "assets"
IMAGE_DIR = ASSETS_DIR / "images"
VIDEO_DIR = ASSETS_DIR / "videos"
ICON_DIR = ASSETS_DIR / "icons"
LOGO_DIR = ASSETS_DIR / "logos"

DATA_DIR = ROOT_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
BACKUP_DIR = DATA_DIR / "backups"
SAMPLE_DATA_DIR = DATA_DIR / "sample_data"

DOCS_DIR = ROOT_DIR / "docs"

DATABASE_FILE = DATABASE_DIR / "mission80.db"

# ---------------------------------------------------
# Theme
# ---------------------------------------------------

PRIMARY = "#7C3AED"
SECONDARY = "#3B82F6"

BACKGROUND = "#0F172A"
CARD = "#1E293B"

TEXT = "#F8FAFC"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"

# ---------------------------------------------------
# Dashboard
# ---------------------------------------------------

WATER_TARGET = 2.5
STEP_TARGET = 8000
PROTEIN_TARGET = 170

# ---------------------------------------------------
# Development
# ---------------------------------------------------

DEBUG = True