import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

from itech_project.settings import sslmode

# Load .env
load_dotenv()

# Get DB URL from env
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL not set in .env")

# Parse connection string
result = urlparse(db_url)
dbname = result.path.lstrip('/')
user = result.username
password = result.password
host = result.hostname
port = result.port or 5432

print(f"dbname: {dbname}")
print(f"user: {user}")
print(f"password: {password}")
print(f"host: {host}")
print(f"port: {port}")

# Attempt DB connection
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        sslmode="require"
    )
    print("✅ Connected to the database successfully!")
    conn.close()
except Exception as e:
    print("❌ Failed to connect to the database:")
    print(e)
