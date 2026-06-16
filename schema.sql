CREATE TABLE Emojis (
    id INTEGER PRIMARY KEY,
    emoji_char TEXT UNIQUE NOT NULL
);

INSERT INTO Emojis (id, emoji_char)
VALUES (1, '🌚'), (2, '🐳'), (3, '🗿'), (4, '😭'), (5, '🫠');

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Reports (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT NOT NULL,
    title TEXT,
    user_id INTEGER NOT NULL REFERENCES Users(id),

    moon_count INTEGER DEFAULT 0,
    whale_count INTEGER DEFAULT 0,
    moai_count INTEGER DEFAULT 0,
    crying_count INTEGER DEFAULT 0,
    melting_count INTEGER DEFAULT 0
);

CREATE TABLE Reactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users(id),
    report_id INTEGER NOT NULL REFERENCES Reports(id) ON DELETE CASCADE,
    emoji_id INTEGER NOT NULL REFERENCES Emojis(id),

    CONSTRAINT uq_user_report_emoji UNIQUE (user_id, report_id, emoji_id)
);

CREATE INDEX idx_reactions_report_id ON Reactions(report_id);
CREATE INDEX idx_reports_user ON Reports(user_id);
CREATE INDEX idx_reactions_user ON Reactions(user_id);
CREATE INDEX idx_reports_sent_at ON Reports(sent_at);
CREATE INDEX idx_reactions_report_emoji ON Reactions(report_id, emoji_id);

CREATE TRIGGER update_report_counts_on_insert
AFTER INSERT ON Reactions
FOR EACH ROW
BEGIN
    UPDATE Reports SET moon_count = moon_count + 1
        WHERE id = NEW.report_id AND NEW.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🌚');
    UPDATE Reports SET whale_count = whale_count + 1
        WHERE id = NEW.report_id AND NEW.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🐳');
    UPDATE Reports SET moai_count = moai_count + 1
        WHERE id = NEW.report_id AND NEW.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🗿');
    UPDATE Reports SET crying_count = crying_count + 1
        WHERE id = NEW.report_id AND NEW.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '😭');
    UPDATE Reports SET melting_count = melting_count + 1
        WHERE id = NEW.report_id AND NEW.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🫠');
END;

CREATE TRIGGER update_report_counts_on_delete
AFTER DELETE ON Reactions
FOR EACH ROW
BEGIN
    UPDATE Reports SET moon_count = moon_count - 1
        WHERE id = OLD.report_id AND OLD.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🌚');
    UPDATE Reports SET whale_count = whale_count - 1
        WHERE id = OLD.report_id AND OLD.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🐳');
    UPDATE Reports SET moai_count = moai_count - 1
        WHERE id = OLD.report_id AND OLD.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🗿');
    UPDATE Reports SET crying_count = crying_count - 1
        WHERE id = OLD.report_id AND OLD.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '😭');
    UPDATE Reports SET melting_count = melting_count - 1
        WHERE id = OLD.report_id AND OLD.emoji_id = (SELECT id FROM Emojis WHERE emoji_char = '🫠');
END;
