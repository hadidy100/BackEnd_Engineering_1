ATTACH DATABASE 'forums.db' AS 'db1';
ATTACH DATABASE 'shard_0.db' AS 'db2';
ATTACH DATABASE 'shard_1.db' AS 'db3';
ATTACH DATABASE 'shard_2.db' AS 'db4';
  
 
DROP TABLE IF EXISTS db2.threadPosts;
DROP TABLE IF EXISTS db2.threads;
DROP TABLE IF EXISTS db3.threadPosts;
DROP TABLE IF EXISTS db3.threads;
DROP TABLE IF EXISTS db4.threadPosts;
DROP TABLE IF EXISTS db4.threads;

DROP TABLE IF EXISTS db1.forums;
DROP TABLE IF EXISTS db1.users;

-- users table which will be referenced by forums and threads tables
CREATE TABLE db1.users(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
);  
-- forums table which has the forum title, and has a foreign key to refernce the user id from the users table so that we can query the name if we needed it
--  You might ask, why can not we just add the name of the user in this table, and the answer is normalization methods, to preserve consistancy and avoid duplication and anomalies
CREATE TABLE db1.forums(
    id INTEGER PRIMARY KEY,
    name TEXT,
    creator INTEGER NOT NULL,
    timestamp TEXT,
    FOREIGN KEY (creator) REFERENCES users(id)
);   
--threads table also references users and forums by their id so normalization reasons as well
CREATE TABLE db2.threads(
    id TEXT PRIMARY KEY,
    title TEXT,
    creator INTEGER,
    forumId INTEGER,
    timestamp TEXT,
    foreign key (creator) REFERENCES  users (id),
    foreign key (forumId) REFERENCES  forums (id)
);  
--threadComments referrenced by thread Id , but each row has its own Id to enable multiple posts for the same thread and the same createForum
CREATE TABLE db2.threadPosts(
    id integer PRIMARY KEY,
    threadId TEXT,
    creator INTEGER,
    comment TEXT,
    timestamp TEXT,
    foreign key (threadId) REFERENCES threads (id),
    foreign key (creator) REFERENCES  users(id)
);  
CREATE TABLE db3.threads(
    id TEXT PRIMARY KEY,
    title TEXT,
    creator INTEGER,
    forumId INTEGER,
    timestamp TEXT,
    foreign key (creator) REFERENCES users (id),
    foreign key (forumId) REFERENCES forums (id)
);  
--threadComments referrenced by thread Id , but each row has its own Id to enable multiple posts for the same thread and the same createForum
CREATE TABLE db3.threadPosts(
    id integer PRIMARY KEY,
    threadId TEXT,
    creator INTEGER,
    comment TEXT,
    timestamp TEXT,
    foreign key (threadId) REFERENCES threads (id),
    foreign key (creator) REFERENCES  users(id)
);  
CREATE TABLE db4.threads(
    id TEXT PRIMARY KEY,
    title TEXT,
    creator INTEGER,
    forumId INTEGER,
    timestamp TEXT,
    foreign key (creator) REFERENCES users (id),
    foreign key (forumId) REFERENCES forums (id)
);  
--threadComments referrenced by thread Id , but each row has its own Id to enable multiple posts for the same thread and the same createForum
CREATE TABLE db4.threadPosts(
    id integer PRIMARY KEY,
    threadId TEXT,
    creator INTEGER,
    comment TEXT,
    timestamp TEXT,
    foreign key (threadId) REFERENCES threads (id),
    foreign key (creator) REFERENCES  users(id)
);  


-- isnert 3 sample users
INSERT INTO db1.users(username,password) VALUES('david','password');   

INSERT INTO db1.users(username,password) VALUES('anas','password');   

INSERT INTO db1.users(username,password) VALUES('jon','password');   

--isert 3 sample forums where each one is created by one of the sample users above
INSERT INTO  db1.forums(name,creator,timestamp) VALUES('redis',(select id from  db1.users where username = 'david'),DATETIME('now','localtime'));  
INSERT INTO  db1.forums(name,creator,timestamp) VALUES('mongodb',(select id from  db1.users where username ='jon'),DATETIME('now','localtime'));   
INSERT INTO  db1.forums(name,creator,timestamp) VALUES('Oracle DB',(select id from  db1.users where username ='anas'),DATETIME('now','localtime'));   


--insert 7 sample threads for each one of the sample forums that are created above
--Each thread has the forum id so that we can see what forum does this thread belog to,
-- in addition to having a creator id so that we know who created that thread but the actual text inside the thread is pushed into another table called threadPosts

INSERT INTO  db2.threads
(
  id,
  title,
  creator,
  forumid,
  timestamp
)
  VALUES
  (
    '58d85824-e164-4716-8051-20e430927936',
    'HELP',
    (select id from db1.users where username = 'david'),
    (select id from db1.forums where name = 'redis'),
    DATETIME('now','localtime')
  );    
 
  --******* Thread posts within a THREAD
  INSERT INTO db2.threadPosts
  (
    threadId,
    creator,
    comment,
    timestamp
  )
    VALUES
    (
      '58d85824-e164-4716-8051-20e430927936',
      1,
      'I can not start Redis, I ping to the IP address, but I get no response',
      DATETIME('now','localtime')
    );    
     

    INSERT INTO db2.threadPosts
    (
      threadId,
      creator,
      comment,
      timestamp
    )
    VALUES
    (
      '58d85824-e164-4716-8051-20e430927936',
      3,
      'May be you are entering the wrong ip address or the wrong host name, can you share with us what you typed?',
      DATETIME('now','localtime')
    );    
     

          -- thread post for Redis
        INSERT INTO db2.threadPosts
        (
        threadId,
        creator,
        comment,
        timestamp
        )
        VALUES
        (
           '58d85824-e164-4716-8051-20e430927936',
           2,
          'Me too, I can not start Redis, I tried all the instruction that were in the documentation but I get server error code 500, please help!!',
          DATETIME('now','localtime')
        );    
         

--Thead #2
INSERT INTO db3.threads
(
  id,
  title,
  creator,
  forumid,
  timestamp
)
  VALUES
  (
    '58d85824-e164-4716-8051-20e430927937',
    'mongodb vs hadoop',
    3,
    (select id from db1.forums where name = 'mongodb'),
    DATETIME('now','localtime')
  );    
   
        --Thread posts within a THREAD
        INSERT INTO db3.threadPosts
                  (
                    threadId,
                    creator,
                    comment,
                    timestamp
                  )
                    VALUES
                    (
                      '58d85824-e164-4716-8051-20e430927937',
                      3,
                      'Can anyone please tell what is the difference between mangoDB and Hadoop? ',
                      DATETIME('now','localtime')
                      );    
                      
          INSERT INTO db3.threadPosts
                    (
                      threadId,
                      creator,
                      comment,
                      timestamp
                    )
                      VALUES
                      (
                        '58d85824-e164-4716-8051-20e430927937',
                        2,
                        'I have the same question, you took the words out of my mouth! ',
                        DATETIME('now','localtime')
                        );    
                         

--Thead #3
INSERT INTO db4.threads
(
  id,
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  '58d85824-e164-4716-8051-20e430927938',
  'Price',
  2,
  (select id from db1.forums where name = 'Oracle DB'),
  DATETIME('now','localtime')
);    

        INSERT INTO db4.threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
          '58d85824-e164-4716-8051-20e430927938',
          2,
          'Why would any enterprise chooses to use Oracle instead of mySql is byond me, I mean it is a lot more expesive, and I do not see any performance or capability issues, thoughts? Anyone? ',
          DATETIME('now','localtime')
        );    

        --Thead #4
INSERT INTO db2.threads
(
  id, 
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  '58d85824-e164-4716-8051-20e430927939',
  'SQL Lite',
  2,
  (select id from db1.forums where name = 'Oracle DB'),
  DATETIME('now','localtime')
);    
        INSERT INTO db2.threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
          '58d85824-e164-4716-8051-20e430927939',
          2,
          'How handy is this SQL lite thing, I must admit, I have never used it before, but I love it!!! ',
          DATETIME('now','localtime')
        );    
--thead 5
INSERT INTO db3.threads
(
  id,
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  '58d85824-e164-4716-8051-20e43092793a',
  'Does anyone know how to start Redis?',
  (select id from db1.users where username = 'david'),
  (select id from db1.forums where name = 'redis'),
  DATETIME('now','localtime')
);    
        INSERT INTO db3.threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
          '58d85824-e164-4716-8051-20e43092793a',
           2,
          'I Think its redis-ctl start, but I am not sure',
          DATETIME('now','localtime')
        );    

INSERT INTO db4.threads
(
  id,
  title,
  creator,
  forumid,
  timestamp
)
VALUES
(
  '58d85824-e164-4716-8051-20e43092793b',
  'Has anyone heard of Edis?',
   3,
  (select id from db1.forums where name = 'redis'),
  DATETIME('now','localtime')
);    

        INSERT INTO db4.threadPosts
        (
          threadId,
          creator,
          comment,
          timestamp
        )
        VALUES
        (
           '58d85824-e164-4716-8051-20e43092793b',
           3,
          'I keep hearing about this Edis, what exactly is it? And how different is it from Redis?',
          DATETIME('now','localtime')
        );    
        -- thread # 7
          INSERT INTO db4.threadPosts
          (
            threadId,
            creator,
            comment,
            timestamp
          )
          VALUES
          (
            '58d85824-e164-4716-8051-20e43092793b',
             1,
            'I can not tell you why so many confusing names, Redis, Pedis, Ennis, Whats going on????',
            DATETIME('now','localtime')
          );    
          INSERT INTO db4.threadPosts
          (
            threadId,
            creator,
            comment,
            timestamp
          )
            VALUES
            (
               '58d85824-e164-4716-8051-20e43092793b',
               2,
              'According to this website, https://dbdb.io, Edis an an Erlang re-implementation of Redis',
              DATETIME('now','localtime')
            );  

/*
the following queries are not used right now, this is just proof of concepts and/or being proactive
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
