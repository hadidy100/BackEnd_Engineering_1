DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS threads;
-- users table which will be referenced by forums and threads tables
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
);
-- forums table which has the forum title, and has a foreign key to refernce the user id from the users table so that we can query the name if we needed it
--  You might ask, why can not we just add the name of the user in this table, and the answer is normalization methods, to preserve consistancy and avoid duplication and anomalies
CREATE TABLE forums(
    id INTEGER PRIMARY KEY,
    name TEXT,
    creator INTEGER NOT NULL,
    timestamp TEXT,
    FOREIGN KEY (creator) REFERENCES USERS(id)
);
--threads table also references users and forums by their id so normalization reasons as well
CREATE TABLE threads(
    id INTEGER PRIMARY KEY,
    title TEXT,
    comment TEXT,
    creator INTEGER,
    forumId INTEGER,
    timestamp TEXT,
    foreign key (creator) REFERENCES users (id),
    foreign key (forumId) REFERENCES forums (id)
);

CREATE UNIQUE INDEX idx_name ON forums (name);
CREATE UNIQUE INDEX idx_user ON users (username);
CREATE UNIQUE INDEX idx_thread ON threads (title);

-- isnert 3 sample users
INSERT INTO users(username,password) VALUES('david','password');
INSERT INTO users(username,password) VALUES('anas','password');
INSERT INTO users(username,password) VALUES('jon','password');

--isert 3 sample forums where each one is created by one of the sample users above
INSERT INTO forums(name,creator) VALUES('redis',(select id from users where username = 'david'));
INSERT INTO forums(name,creator) VALUES('mongodb',(select id from users where username ='jon'));
INSERT INTO forums(name,creator) VALUES('Oracle DB',(select id from users where username ='anas'));


--insert 3 sample threads for each one of the sample forums that are created above
--Each thread has the forum id so that we can see what forum does this thread belog to,
-- in addition to having a creator id so that we know who created that thread

INSERT INTO threads
(
  title,
  comment,
  creator,
  forumid,
  timestamp
)
  VALUES
  (
    'HELP',
    'Why do I get an error when I ping to redis-cli??, please help!!',
    (select id from users where username = 'david'),
    (select id from forums where name = 'redis'),
    DATETIME('now','localtime')
  );
--Thead #2
  INSERT INTO threads
  (
    title,
    comment,
    creator,
    forumid,
    timestamp
  )
    VALUES
    (
      'mongodb vs hadoop',
      'Can anyone please tell what is the difference between mangoDB and Hadoop? ',
      (select id from users where username = 'jon'),
      (select id from forums where name = 'mongodb'),
      DATETIME('now','localtime')
    );
--Thead #3
    INSERT INTO threads
    (
      title,
      comment,
      creator,
      forumid,
      timestamp
    )
      VALUES
      (
        'Price',
        'Why would any enterprise chooses to use Oracle instead of mySql is byond me,
        I mean it is a lot more expesive, and I do not see any performance or capability issues, thoughts? Anyone? ',
        (select id from users where username = 'anas'),
        (select id from forums where name = 'Oracle DB'),
        DATETIME('now','localtime')
      );
      --Thead #4
          INSERT INTO threads
          (
            title,
            comment,
            creator,
            forumid,
            timestamp
          )
            VALUES
            (
              'SQL Lite',
              'How handy is this SQL lite thing, I must admit, I have never used it before, but I love it!!! ',
              (select id from users where username = 'anas'),
              (select id from forums where name = 'Oracle DB'),
              DATETIME('now','localtime')
            );
