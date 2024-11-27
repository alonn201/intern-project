import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

def db_connection():
    url = os.getenv("DATABASE_URL")
    return psycopg2.connect(url, cursor_factory=RealDictCursor)