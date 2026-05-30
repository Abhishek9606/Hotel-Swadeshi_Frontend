CREATE TABLE IF NOT EXISTS foods(
food_id INT PRIMARY KEY AUTO_INCREMENT,
food_name VARCHAR(50) NOT NULL,
description TINYTEXT NOT NULL,
food_type ENUM('Veg','Non-Veg') NOT NULL,
food_price INT NOT NULL,
popularity INT NOT NULL DEFUALT 0,
popular BOOL DEFAULT FALSE,
CHECK(food_price > 0)
)


CREATE TABLE IF NOT EXISTS reviews(
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_id INT,
    FOREIGN KEY(cust_id) REFERENCES customers(cust_id),
    food_id INT,
     FOREIGN KEY(cust_id) REFERENCES customers(cust_id),
     review TINYTEXT NOT NULL
)



CREATE TABLE IF NOT EXISTS customers(
cust_id INT PRIMARY KEY AUTO_INCREMENT,
cust_name  VARCHAR(50) NOT NULL,
email VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
contact_no DECIMAL(10)
)




CREATE TABLE IF NOT EXISTS orders(
order_id INT PRIMARY KEY AUTO_INCREMENT,
item_id INT,
quantity INT NOT NULL,
FOREIGN KEY(order_item) REFERENCES foods(food_id),
ordered_by INT,
FOREIGN KEY(ordered_by) REFERENCES customers(cust_id)
ordered_at DATETIME NOT NULL,
location VARCHAR(100) NOT NULL
)