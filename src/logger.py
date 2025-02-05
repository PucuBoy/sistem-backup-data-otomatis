import logging
import os
from datetime import datetime

class BackupLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BackupLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        self.logger = logging.getLogger('BackupSystem')
        
        # Hindari duplikasi handler
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            file_handler = logging.FileHandler('logs/backup.log')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)