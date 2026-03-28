CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
    );

CREATE TABLE Reports (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    title TEXT,
    reaction_1 INTEGER,
    user_id INTEGER REFERENCES Users
    );
