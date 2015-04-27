-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create table results with values attached to lose, draw, win
create table results (result integer primary key,
                      name varchar,
                      score numeric
                     );

-- Fill in the default values for lose, draw, win
insert into results (result, name, score) values 
                        (0, 'lose', 0),
                        (1, 'draw', 0.5),
                        (2, 'win', 1);

-- Create a table with players containing id and name
create table players (id serial primary key,
                      name varchar);

-- Create a strength table for estimation of win and lose
create table strength (id serial references players(id),
                       strength integer check (strength >=0 and strength <= 100)
                       );

-- Create a tournemts table to store matches of the tournament                     
create table tournaments (id serial primary key,
                          location varchar,
                          year integer check (year > 999),
                          unique (location, year)
                          );

-- Create a matches table with players and matches and results                          
create table matches (tournament_id integer references tournaments(id),
                      match_id integer check (match_id > 0),
                      player integer references players(id),
                      opponent integer references players(id) 
                          check (player != opponent),
                      result integer references results(result),
                      primary key (tournament_id, match_id)
                      );

