-- SQLite
-- CREATE TABLE users(
--  id INTEGER PRIMARY KEY AUTOINCREMENT,
--  name TEXT,
--  password INTEGER,
--  is_customer BOOLEAN,
--  created_date TIMESTAMP DEFAULT (datetime('now','localtime'))
-- );

-- DROP TABLE users;

-- CREATE TABLE users(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL,
--     hash TEXT NOT NULL,
--     is_business BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime'))
-- );

-- CREATE TABLE secrets(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     title TEXT NOT NULL,
--     content TEXT NOT NULL,
--     image BLOB NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id)
-- );

-- CREATE TABLE dreams(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     content TEXT NOT NULL,
--     is_solved BOOLEAN NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id)
-- );

-- CREATE TABLE coments(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     dreams_id INTEGER NOT NULL,
--     content TEXT NOT NULL,
--     is_best BOOLEAN NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id),
--     FOREIGN KEY(dreams_id) REFERENCES dreams(id)
-- );

-- CREATE TABLE replies(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     coments_id INTEGER NOT NULL,
--     content TEXT NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id),
--     FOREIGN KEY(coments_id) REFERENCES coments(id)
-- );

-- DROP TABLE coments;

-- CREATE TABLE comments(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     dreams_id INTEGER NOT NULL,
--     content TEXT NOT NULL,
--     is_best BOOLEAN NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id),
--     FOREIGN KEY(dreams_id) REFERENCES dreams(id)
-- );

-- DROP TABLE replies;

-- CREATE TABLE replies(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     comments_id INTEGER NOT NULL,
--     content TEXT NOT NULL,
--     is_deleted BOOLEAN NOT NULL,
--     created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
--     FOREIGN KEY(user_id) REFERENCES users(id),
--     FOREIGN KEY(comments_id) REFERENCES comments(id)
-- );

--DROP TABLE secrets;

CREATE TABLE secrets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image BLOB NOT NULL,
    is_deleted BOOLEAN NOT NULL,
    created_date TIMESTAMP DEFAULT (datetime('now','localtime')),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

