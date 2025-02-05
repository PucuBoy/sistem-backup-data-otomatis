CREATE DATABASE IF NOT EXISTS example_db;
USE example_db;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS backup_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    backup_file VARCHAR(255) NOT NULL,
    backup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    file_size BIGINT,
    error_message TEXT
);

INSERT INTO products (name, price, stock) VALUES
('Laptop', 15000000, 10),
('Mouse', 200000, 50),
('Keyboard', 500000, 30),
('Monitor', 3000000, 15);