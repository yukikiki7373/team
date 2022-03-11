-- SQLite
CREATE TABLE users(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 password INTEGER,
 is_customer BOOLEAN,
 created_date TIMESTAMP DEFAULT (datetime('now','localtime'))
);