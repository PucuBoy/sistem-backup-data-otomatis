import mysql.connector
from config.config import DB_CONFIG
from src.logger import BackupLogger

class DatabaseManager:
    def __init__(self):
        self.logger = BackupLogger()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            self.logger.info("Database connection established")
            return True
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}")
            return False

    def disconnect(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            self.logger.info("Database connection closed")

    def log_backup(self, backup_file, status, file_size=None, error_message=None):
        try:
            query = """
            INSERT INTO backup_logs (backup_file, status, file_size, error_message)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (backup_file, status, file_size, error_message))
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Failed to log backup: {str(e)}")