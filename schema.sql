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
    user_id INTEGER REFERENCES Users
    );

CREATE TABLE Reactions (
    id INTEGER PRIMARY KEY,
    emoji TEXT,
    user_id INTEGER REFERENCES Users,
    report_id INTEGER REFERENCES Reports
    );
