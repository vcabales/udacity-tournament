-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS players CASCADE; --need cascade to drop the table's children
DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE players (
    id SERIAL primary key, --Serial allows you to automatically generate unique integer numbers
    name text
    );

CREATE TABLE matches (
    id SERIAL primary key,
    winner SERIAL references players(id),
    loser SERIAL references players(id)
    );

--creates a view of all player ids, names, and the number of matches they won
CREATE VIEW wins AS
  SELECT players.id AS id, players.name AS name, COUNT(matches.winner) AS count FROM players
  LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id ORDER BY players.id DESC;
--Left join because not every player may have a win

--creates a view of all player ids,names, and the number of matches they lost
CREATE VIEW losses AS
  SELECT players.id AS id, players.name AS name, COUNT(matches.loser) AS count FROM players
  LEFT JOIN matches ON players.id = matches.loser GROUP BY players.id ORDER BY players.id DESC;

--sums up total number of matches so winners and losers don't double count
CREATE VIEW total_matches AS
  SELECT players.id AS id, COUNT(matches) AS count FROM players
  LEFT JOIN matches ON players.id = matches.winner
  OR players.id = matches.loser GROUP BY players.id;
