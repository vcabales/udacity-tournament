#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) AS count FROM players;")
    count = c.fetchone()
    conn.commit()
    conn.close()
    return count[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT players.id, players.name, wins.count, total_matches.count \
        FROM players, wins, total_matches WHERE players.id = wins.id AND        \
        players.id = total_matches.id ORDER BY wins DESC;")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES ({0},{1});".format(winner,loser))
    conn.commit()
    conn.close()

def getWins():
    #Returns list of tuples with the player's id and number of wins
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM wins;")
    wins = []
    wins.append(c.fetchone())
    conn.commit()
    conn.close()
    return wins

def getMatches():
    #Returns list of tuples with the player's id and number of matches played
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM total_matches;")
    matches = []
    matches.append(c.fetchone())
    conn.commit()
    conn.close()
    return matches

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
    standings = playerStandings()
    total_players = countPlayers()
    print total_players
    wins = getWins()
    print wins
    matches = getMatches()
    print matches
    if len(matches) == 0: # first time
        for i in range(total_players):
            if i % 2 == 0:
                id1 = standings[i][0]
                name1 = standings[i][1]
                id2 = standings[i+1][0]
                name2 = standings[i+1][1]
                pairs.append(id1, name1, id2, name2)
    else:
    matched = []

    for i in range(total_players):
        id1 = standings[i][0]
        name1 = standings[i][1]
        matched.append(standings[i][0])
        while (j < total_players):
            if (standings[j][0] not in matched):
                if (wins[i][2] == wins[j][2]) and (matches[i][1] == matches[j][1]):
                    id2 = standings[j][0]
                    name2 - standings[j][1]
                    pairs.append((id1,name1,id2,name2))
                    matched.append(standings[j][0])
                    break
            else:
                j += 1

    print pairs
    return pairs
