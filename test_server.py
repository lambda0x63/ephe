import os
import sys

print("--- Testing Environment ---")

# 1. Test Syntax / Imports
try:
    import swisseph as swe
    import geopy
    import timezonefinder
    import pytz
    import sqlalchemy
    import psycopg2
    print("[PASS] All modules imported.")
except ImportError as e:
    print(f"[FAIL] Import Error: {e}")
    sys.exit(1)

# 2. Test DB Connection
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://natal_user:natal_secret_2024@localhost:5432/natal_chart"
)

print(f"Testing DB connection to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("[PASS] DB Connection successful!")
    connection.close()
except Exception as e:
    print(f"[FAIL] DB Connection failed: {e}")
    sys.exit(1)

print("--- All Tests Passed ---")
