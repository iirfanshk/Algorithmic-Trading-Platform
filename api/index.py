import os
import sys
from pathlib import Path

# Add project root to sys.path so 'app', 'config', 'server', etc. are importable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import Flask app instance from server.py
from server import app

