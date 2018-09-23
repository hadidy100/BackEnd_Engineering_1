DROP TABLE IF EXISTS threadPosts;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS users;


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
    creator INTEGER,
    forumId INTEGER,
    timestamp TEXT,
    foreign key (creator) REFERENCES users (id),
    foreign key (forumId) REFERENCES forums (id)
);
--threadComments referrenced by thread Id , but each row has its own Id to enable multiple posts for the same thread and the same createForum
CREATE TABLE threadPosts(
    id integer PRIMARY KEY,
    threadId INTEGER,
    creator INTEGER,
    comment TEXT,
    timestamp TEXT,
    foreign key (threadId) REFERENCES threads (id),
    foreign key (creator) REFERENCES users(id)
);

-- isnert 3 sample users
INSERT INTO users(username,password) VALUES('david','password');
INSERT INTO users(username,password) VALUES('anas','password');
INSERT INTO users(username,password) VALUES('jon','password');
commit;
--isert 3 sample forums where each one is created by one of the sample users above
INSERT INTO forums(name,creator,timestamp) VALUES('redis',(select id from users where username = 'david'),DATETIME('now','localtime'));
INSERT INTO forums(name,creator,timestamp) VALUES('mongodb',(select id from users where username ='jon'),DATETIME('now','localtime'));
INSERT INTO forums(name,creator,timestamp) VALUES('Oracle DB',(select id from users where username ='anas'),DATETIME('now','localtime'));


--insert 7 sample threads for each one of the sample forums that are created above
--Each thread has the forum id so that we can see what forum does this thread belog to,
-- in addition to having a creator id so that we know who created that thread but the actual text inside the thread is pushed into another table called threadPosts

INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
  VALUES
  (
    'HELP',
    (select id from users where username = 'david'),
    (select id from forums where name = 'redis'),
    DATETIME('now','localtime')
  );
  --******* Thread posts within a THREAD
  INSERT INTO threadPosts
  (
    threadId,
    creator,
    comment,
    timestamp
  )
    VALUES
    (
      1,
      1,
      'I can not start Redis, I ping to the IP address, but I get no response',
      DATETIME('now','localtime')
    );
    INSERT INTO threadPosts
    (
      threadId,
      creator,
      comment,
      timestamp
    )
    VALUES
    (
      1,
      3,
      'May be you are entering the wrong ip address or the wrong host name, can you share with us what you typed?',
      DATETIME('now','localtime')
    );
          -- thread post for Redis
        INSERT INTO threadPosts
        (
        threadId,
        creator,
        comment,
        timestamp
        )
        VALUES
        (
           1,
           2,
          'Me too, I can not start Redis, I tried all the instruction that were in the documentation but I get server error code 500, please help!!',
          DATETIME('now','localtime')
        );
--Thead #2
INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
  VALUES
  (
    'mongodb vs hadoop',
    3,
    (select id from forums where name = 'mongodb'),
    DATETIME('now','localtime')
  );
        --Thread posts within a THREAD
        INSERT INTO threadPosts
                  (
                    threadId,
                    creator,
                    comment,
                    timestamp
                  )
                    VALUES
                    (
                      2,
                      3,
                      'Can anyone please tell what is the difference between mangoDB and Hadoop? ',
                      DATETIME('now','localtime')
                      );
          INSERT INTO threadPosts
                    (
                      threadId,
                      creator,
                      comment,
                      timestamp
                    )
                      VALUES
                      (
                        2,
                        2,
                        'I have the same question, you took the words out of my mouth! ',
                        DATETIME('now','localtime')
                        );
--Thead #3
INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  'Price',
  2,
  (select id from forums where name = 'Oracle DB'),
  DATETIME('now','localtime')
);
        INSERT INTO threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
          3,
          2,
          'Why would any enterprise chooses to use Oracle instead of mySql is byond me, I mean it is a lot more expesive, and I do not see any performance or capability issues, thoughts? Anyone? ',
          DATETIME('now','localtime')
        );
        --Thead #4
INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  'SQL Lite',
  2,
  (select id from forums where name = 'Oracle DB'),
  DATETIME('now','localtime')
);
        INSERT INTO threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
          4,
          2,
          'How handy is this SQL lite thing, I must admit, I have never used it before, but I love it!!! ',
          DATETIME('now','localtime')
        );
--thead 5
INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  'Does anyone know how to start Redis?',
  (select id from users where username = 'david'),
  (select id from forums where name = 'redis'),
  DATETIME('now','localtime')
);
        INSERT INTO threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
           5,
           2,
          'I Think its redis-ctl start, but I am not sure',
          DATETIME('now','localtime')
        );

INSERT INTO threads
(
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  'Has anyone heard of Edis?',
   3,
  (select id from forums where name = 'redis'),
  DATETIME('now','localtime')
);

        INSERT INTO threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
           6,
           3,
          'I keep hearing about this Edis, what exactly is it? And how different is it from Redis?',
          DATETIME('now','localtime')
        );
        -- thread # 7
          INSERT INTO threadPosts
          (
            threadId,
            creator,
            comment,
            timestamp
          )
          VALUES
          (
             6,
             1,
            'I can not tell you why so many confusing names, Redis, Pedis, Ennis, Whats going on????',
            DATETIME('now','localtime')
          );
          INSERT INTO threadPosts
          (
            threadId,
            creator,
            comment,
            timestamp
          )
            VALUES
            (
               6,
               2,
              'According to this website, https://dbdb.io, Edis an an Erlang re-implementation of Redis',
              DATETIME('now','localtime')
            );
commit;
/*
 select
	 f.name,
	 u.username,
	 tp.comment,
	 t.title,
	 tp.timestamp
from
	 forums f,
	 users u,
	 threads t,
	 threadPosts tp
where
	f.id = t.forumId and
	u.id = t.creator and
	t.id = tp.threadId
order by
	tp.timestamp;



  select
	 f.name forumName,
	 u.username froumCreator,
	 tp.comment,
	 t.title,
	 tp.timestamp,
	 f.id forumId,
	 (select uu.username from users uu, threadPosts ttp where ttp.creator = uu.id and ttp.id = tp.id) PostCreator,
	 (select uuu.username from users uuu, threads ttt  where ttt.creator = uuu.id and ttt.id = t.id) threadCreator
from
	 forums f,
	 users u,
	 threads t,
	 threadPosts tp
where
	f.id = t.forumId and
	u.id = t.creator and
	t.id = tp.threadId and
	f.creator = u.id
order by
	tp.timestamp,  f.name;
*/
