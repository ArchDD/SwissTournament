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
	id SERIAL NOT NULL,
	winner INT NOT NULL,
	loser INT NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (winner) REFERENCES Players(id),
	FOREIGN KEY (loser) REFERENCES Players(id)
);

-- Create a view that counts all wins for every player
CREATE OR REPLACE VIEW win_count AS
(
	SELECT Players.id AS id, COUNT(Matches.winner) AS wins 
	FROM Players LEFT JOIN Matches
	ON Players.id = Matches.winner
	GROUP BY Players.id
	ORDER BY wins
);

-- Create a view that counts all matches for every player
CREATE OR REPLACE VIEW match_count AS
(
	SELECT Players.id AS id, COUNT(Matches) AS matches 
	FROM Players LEFT JOIN Matches
	ON Players.id = Matches.winner OR Players.id = Matches.loser
	GROUP BY Players.id
	ORDER BY matches
);

-- Create a standings view from win count and match count
CREATE OR REPLACE VIEW standings AS 
(
	SELECT	
		Players.id,
		Players.name, 
		(SELECT wins FROM win_count WHERE win_count.id = Players.id) AS wins,
		(SELECT matches FROM match_count WHERE match_count.id = Players.id) AS matches 
	FROM Players ORDER BY wins DESC
);

-- Use standings view to generate ranking based on wins
CREATE OR REPLACE VIEW ranks AS 
(
	SELECT ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank, id, name 
	FROM standings
);
