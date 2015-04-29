import random
import os.path
import sys

from math import ceil, log
from operator import itemgetter
from setupdb import connect_db, init_tournament
from tournament import *


def get_players():
    """Get players id from the database """
    connection = connect_db()
    cursor = connection.cursor()
    query = 'select id from players'
    cursor.execute(query)
    players = [player[0] for player in cursor]
    if is_odd(len(players)):
        players = create_bye(players)
    return players


def create_bye(players):
    """Create a bye player named 'bye'.
    A match against the bye player will always be won.
    """
    connection = connect_db()
    cursor = connection.cursor()
    query = """insert into players (name)
               values ('bye')"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    return get_players()


def is_odd(num):
    """Check if a number is odd"""
    return num & 0x1


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
    while len(ranked_players) > 1:
        player = ranked_players.pop(0)
        opponents = get_opponents(player)
        try:
            opponent = next(x for x in ranked_players if x not in opponents)
        except StopIteration, exp:
            # we ran into a problem as the last match already played
            # we therefore exchange two pairs
            opponent = None
            # create the unhappy pair
            unhappy_pair = [player, ranked_players[0]]
            # get all alternatives as opponent
            alternatives = rank_players([alt for alt in rank_players(players)
                                         if player not in
                                         get_opponents(alt) and
                                         player != alt])[::-1]

            # get all pairings of the alternatives
            alt_pairs = [pair for pair in player_pairs
                         if pair[0] in alternatives or
                         pair[1] in alternatives][::-1]
            # check if player can play against other opponent
            for alt_pair in alt_pairs:
                if not (alt_pair[0] in opponents or
                        player in get_opponents(alt_pair[1]) or
                        unhappy_pair[1] in get_opponents(alt_pair[0])):
                    player_pairs.remove(alt_pair)
                    player_pairs.append((alt_pair[0], unhappy_pair[1]))
                    opponent = alt_pair[1]
                    ranked_players.append(opponent)
                    break
        ranked_players.remove(opponent)
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
    ranked_players.sort(key=itemgetter(1, 2), reverse=True)
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
    if get_name(player) == 'bye':
        return opponent
    if get_name(opponent) == 'bye':
        return player
    outcome = random.choice([0, 1])
    if outcome:
        reportMatch(player, opponent)
        return player
    reportMatch(opponent, player)
    return opponent


def play_round(players):
    """Play a round of a swiss tournament"""
    pairs = pair_players(players)
    for pair in pairs:
        play_match(*pair)


def play_tournament():
    """Play a swiss tournanemt"""
    init_tournament()
    players = get_players()
    for idx in range(max_rounds()):
        play_round(players)
        print "Round", idx + 1, "played"
    print "Tournament played"


if __name__ == '__main__':
    for idx in range(20):
        play_tournament()
