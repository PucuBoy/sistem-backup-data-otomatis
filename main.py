# main.py
import schedule
import time
from src.backup import BackupSystem
from src.logger import BackupLogger
from config.config import BACKUP_CONFIG

def main():
    logger = BackupLogger()
    backup_system = BackupSystem()
    
    logger.info("=== Backup System Started ===")
    logger.info(f"Backup interval set to: {BACKUP_CONFIG['backup_interval']}")
    logger.info(f"Backup directory: {BACKUP_CONFIG['backup_dir']}")
    logger.info(f"Retention period: {BACKUP_CONFIG['retention_days']} days")
    
    # Jalankan backup pertama segera setelah program dimulai
    logger.info("Running initial backup...")
    backup_system.create_backup()
    
    # Schedule backup berdasarkan interval yang ditentukan
    interval = BACKUP_CONFIG['backup_interval']
    if interval.endswith('h'):
        hours = int(interval[:-1])
        schedule.every(hours).hours.do(backup_system.create_backup)
        logger.info(f"Scheduled next backup in {hours} hours")
    
    # Schedule cleanup setiap hari
    schedule.every().day.at("00:00").do(backup_system.cleanup_old_backups)
    logger.info("Scheduled daily cleanup at midnight")
    
    try:
        logger.info("System is running. Press Ctrl+C to stop.")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("=== Backup System Stopped ===")

if __name__ == "__main__":
    main()