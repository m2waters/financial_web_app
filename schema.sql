DROP TABLE IF EXISTS financials;

CREATE TABLE financials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company TEXT NOT NULL,
    volume INTEGER NOT NULL,
    volume_weighted FLOAT NOT NULL,
    opening_value FLOAT NOT NULL,
    closing_value FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    trades INTEGER NOT NULL
    );