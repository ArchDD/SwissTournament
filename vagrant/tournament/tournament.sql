-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players
(
	-- Using serial in place of auto_increment
	id SERIAL NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY (ID)
);

CREATE TABLE Matches
(
	p1 INT NOT NULL,
	p2 INT NOT NULL,
	winner INT NOT NULL,
	-- Primary key from players as they will not play each other again
	PRIMARY KEY (p1, p2),
	FOREIGN KEY (p1) REFERENCES Players(id),
	FOREIGN KEY (p2) REFERENCES Players(id),
	FOREIGN KEY (winner) REFERENCES Players(id)
);