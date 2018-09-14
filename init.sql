DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS threads;

CREATE TABLE forums(
    id INTEGER PRIMARY KEY,
    name TEXT,
    creator TEXT
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT    
);

CREATE TABLE threads(
    id INTEGER PRIMARY KEY,
    title TEXT,
    creator TEXT,
    timestamp TEXT
);

CREATE UNIQUE INDEX idx_name ON forums (name);
CREATE UNIQUE INDEX idx_user ON users (username);
CREATE UNIQUE INDEX idx_thread ON threads (title);

INSERT INTO forums(name,creator) VALUES('redis','alice');
INSERT INTO forums(name,creator) VALUES('mongodb','bob');
INSERT INTO users(username,password) VALUES('david','password');
INSERT INTO users(username,password) VALUES('anas','password');
INSERT INTO users(username,password) VALUES('jon','password');
INSERT INTO threads(title,creator,timestamp) VALUES('HELP','david',DATETIME('now','localtime'));

