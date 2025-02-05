import os
import subprocess
import gzip
from datetime import datetime, timedelta
from src.logger import BackupLogger
from src.database import DatabaseManager
from config.config import DB_CONFIG, BACKUP_CONFIG

class BackupSystem:
    def __init__(self):
        self.logger = BackupLogger()
        self.db_manager = DatabaseManager()
        
        # Tentukan path mysqldump
        if os.name == 'nt':  # Windows
            self.mysqldump_path = r"C:\xampp\mysql\bin\mysqldump.exe"
        else:  # Linux/Mac
            self.mysqldump_path = "mysqldump"
    
    def create_backup(self):
        if not os.path.exists(BACKUP_CONFIG['backup_dir']):
            os.makedirs(BACKUP_CONFIG['backup_dir'])

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{BACKUP_CONFIG['backup_dir']}/backup_{timestamp}.sql"
        
        try:
            # Buat file konfigurasi temporary untuk mysqldump
            cnf_content = f"""[client]
host={DB_CONFIG['host']}
user={DB_CONFIG['user']}
password={DB_CONFIG['password']}
"""
            cnf_path = "temp_mysql.cnf"
            with open(cnf_path, "w") as f:
                f.write(cnf_content)
            
            try:
                # Gunakan file konfigurasi untuk backup
                command = f'"{self.mysqldump_path}" --defaults-file="{cnf_path}" {DB_CONFIG["database"]} > "{backup_file}"'
                self.logger.info("Starting backup process...")
                
                # Jalankan backup
                subprocess.run(command, shell=True, check=True)
                
                if BACKUP_CONFIG['compress']:
                    with open(backup_file, 'rb') as f_in:
                        with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
                            f_out.writelines(f_in)
                    os.remove(backup_file)
                    backup_file = f"{backup_file}.gz"

                file_size = os.path.getsize(backup_file)
                self.logger.info(f"Backup created successfully: {backup_file}")
                
                if self.db_manager.connect():
                    self.db_manager.log_backup(backup_file, "SUCCESS", file_size)
                    self.db_manager.disconnect()
                    
                return True
                
            finally:
                # Hapus file konfigurasi temporary
                if os.path.exists(cnf_path):
                    os.remove(cnf_path)
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            if self.db_manager.connect():
                self.db_manager.log_backup(backup_file, "FAILED", error_message=str(e))
                self.db_manager.disconnect()
            return False

    def cleanup_old_backups(self):
        """
        Membersihkan file backup yang lebih lama dari retention_days yang ditentukan
        """
        try:
            self.logger.info("Starting cleanup of old backups...")
            retention_date = datetime.now() - timedelta(days=BACKUP_CONFIG['retention_days'])
            
            if not os.path.exists(BACKUP_CONFIG['backup_dir']):
                self.logger.info("Backup directory does not exist. Nothing to clean.")
                return
            
            count_deleted = 0
            for filename in os.listdir(BACKUP_CONFIG['backup_dir']):
                file_path = os.path.join(BACKUP_CONFIG['backup_dir'], filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_modified < retention_date:
                    os.remove(file_path)
                    count_deleted += 1
                    self.logger.info(f"Deleted old backup: {filename}")
            
            self.logger.info(f"Cleanup completed. Deleted {count_deleted} old backup files.")
                    
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")