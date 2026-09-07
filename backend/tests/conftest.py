import sys
import os
from pathlib import Path
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["AUTH_EMAIL"] = "admin@pricetracker.com"
os.environ["AUTH_PASSWORD_HASH"] = generate_password_hash("admin123")
