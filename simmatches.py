import random
import os.path
import sys

from math import ceil, log
from operator import itemgetter
from setupdb import connect_db
from tournament import *


def get_players():
    """Get players from the database """
    connection = connect_db()
    cursor = connection.cursor()
    query = 'select id from players'
    cursor.execute(query)
    players = []
    for player in cursor:
        players.append(player[0])
    return players


def get_name(player):
    """Get a player name"""
    connection = connect_db()
    cursor = connection.cursor()
    query = 'select name from players where id = {}'.format(player)
    cursor.execute(query)
    return cursor.fetchall()[0]


def get_wins(player):
    """Calculate the number of wins from the stored matches"""
    connection = connect_db()
    cursor = connection.cursor()
    query = """select distinct count(winner) from matches
                 where winner = {}
                 group by winner
                 order by count desc limit 1""".format(player)
    cursor.execute(query)
    wins = cursor.fetchall()
    if not wins:
        return 0
    else:
        return wins[0][0]


def get_rounds():
    """Calculate the number of rounds played from the stored matches"""
    connection = connect_db()
    cursor = connection.cursor()
    query = """select distinct count(*) from matches as m1
                 full outer join matches m2 on m1.winner=m2.loser
                 group by m1.winner, m2.loser
                 order by count desc limit 1"""
    cursor.execute(query)
    rounds = cursor.fetchall()
    if not rounds:
        return 0
    else:
        return rounds[0][0]


def max_rounds():
    """Get maximum number of rounds to play"""
    return int(ceil(log(len(get_players()), 2)))


def get_opponents(player):
    """Gets a list of opponents the player has played"""
    connection = connect_db()
    cursor = connection.cursor()
    query = """select loser as opponent from matches
                 where winner = {0}
                 union
               select winner from matches
                 where loser = {0}""".format(player)
    cursor.execute(query)
    opponents = [opp[0] for opp in cursor]
    return opponents


def pair_players(players):
    """Pair players according to their wins avoiding double matches"""
    if get_rounds() > max_rounds:
        return []
    player_wins = [[player, get_wins(player)] for player in players]
    player_wins.sort(key=itemgetter(1), reverse=True)
    player_pairs = []
    while len(player_wins) > 0:
        player = player_wins.pop(0)[0]
        opponents = get_opponents(player)
        for idx, opponent in enumerate(player_wins):
            if not opponent[0] in opponents:
                opponent = player_wins.pop(idx)
                break
        player_pairs.append((player, opponent[0]))
    return player_pairs


def play_match(player, opponent):
    """Play a match. Return updated player and opponent"""
    outcome = random.choice([0, 1])
    if outcome:
        reportMatch(player, opponent)
        return player
    reportMatch(opponent, player)
    return opponent


if __name__ == '__main__':
    players = get_players()
    pairs = pair_players(players)
    for pair in pairs:
        play_match(*pair)
