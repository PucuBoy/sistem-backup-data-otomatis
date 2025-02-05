import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'tes123'),
    'database': os.getenv('DB_NAME', 'example_db')
}

BACKUP_CONFIG = {
    'backup_dir': 'backups/',
    'backup_interval': '24h',  # Format: 24h, 12h, 1h
    'retention_days': 7,
    'compress': True
}