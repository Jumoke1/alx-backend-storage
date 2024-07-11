-- creates a table users following these requirements:
CREATE TABLE IF NOT EXIST user(
    id INT NOT NULL AUTO_INCREAMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
