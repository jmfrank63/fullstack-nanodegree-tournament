-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a table with players containing id and name
create table players (id serial primary key,
                      name varchar);

-- Create a matches table with players and matches and results                          
create table matches (winner integer references players(id),
                      loser integer references players(id),
                      primary key (winner, loser)
                      );

