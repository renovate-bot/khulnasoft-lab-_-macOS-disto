CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    repo TEXT,
    commit_hash TEXT,
    author_name TEXT,
    author_email TEXT,
    commit_date TIMESTAMP,
    message TEXT
);
