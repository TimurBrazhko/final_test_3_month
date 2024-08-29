CREATE_TABLE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products 
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(255),
category VARCHAR(255),
size VARCHAR(255),
price VARCHAR(255),
id_product VARCHAR(255),
photo TEXT
)
"""

INSERT_PRODUCTS = """
INSERT INTO products(name, category, size, price, id_product, photo)
VALUES(?, ?, ?, ?, ?, ?)
"""