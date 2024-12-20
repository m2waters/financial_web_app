DROP TABLE IF EXISTS financials;
DROP TABLE IF EXISTS figures;
DROP TABLE IF EXISTS reddit_posts;

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

CREATE TABLE figures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE reddit_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_title TEXT NOT NULL,
    author TEXT,
    permalink TEXT,
    subreddit TEXT,
    upvote_ratio FLOAT
);



