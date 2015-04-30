#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from setupdb import connect_db
from support import *


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return connect_db()


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    query = 'delete from matches'
    cursor.execute(query)
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    query = 'delete from players'
    cursor.execute(query)
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    query = 'select count(id) from players'
    cursor.execute(query)
    num = cursor.fetchall()[0][0]
    connection.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    # bye is a reserved name so prevent this name
    if name == 'bye':
        name = 'player named bye'
    # replace any single apostrophes with doubled
    # single apostrophes and insert name into query
    query = """insert into players (name)
               values (%s)"""
    cursor.execute(query, (name, ))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    query = 'select * from players'
    cursor.execute(query)
    players = cursor.fetchall()
    standings = []
    for player in players:
        player += (get_wins(player[0]), get_rounds())
        standings.append(player)
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    query = """insert into matches (winner, loser)
                  values (%s, %s)"""
    cursor.execute(query, (winner, loser))
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = pair_players(get_players())
    full_pairs = [(pair[0], get_name(pair[0]), pair[1], get_name(pair[1]))
                  for pair in pairs]
    return full_pairs
