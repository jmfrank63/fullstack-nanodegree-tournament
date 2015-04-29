import random
import os.path
import sys

from math import ceil, log
from operator import itemgetter
from setupdb import connect_db
from tournament import *


def get_players():
    """Get players id from the database """
    connection = connect_db()
    cursor = connection.cursor()
    query = 'select id from players'
    cursor.execute(query)
    return [player[0] for player in cursor]

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
    """Pair players according to their wins avoiding double matches
    This is already a swiss pairing but only for id without name
    """
    # don't return any more pairs if maximum number of rounds is already played
    if get_rounds() > max_rounds:
        return []
    ranked_players = rank_players(players)
    player_pairs = []
    while len(ranked_players) > 0:
        player = ranked_players.pop(0)
        opponents = get_opponents(player)
        for idx, opponent in enumerate(ranked_players):
            if not opponent in opponents:
                opponent = ranked_players.pop(idx)
                break
        player_pairs.append((player, opponent))
    return player_pairs


def rank_players(players):
    """Sort the players according to their current ranking
    Break tie by using the wins of the opponents they
    have won against
    """
    # Add values for wins and opponent match wins to the player for sorting
    ranked_players = [[player, get_wins(player), get_opponent_wins(player)]
                       for player in players]
    ranked_players.sort(key=itemgetter(1,2), reverse=True)
    # return ids only as the other info was only needed for sorting
    return [player[0] for player in ranked_players]


def get_opponent_wins(player):
    """Returns the sum of all opponent wins"""
    opponents = get_opponents(player)
    wins = 0
    for opponent in opponents:
        wins += get_wins(opponent)
    return wins


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
