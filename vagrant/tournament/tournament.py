#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


connection = connect()
cursor = connection.cursor()


def deleteMatches():
    """Remove all the match records from the database."""
    cursor.execute("DELETE FROM Matches")
    connection.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    cursor.execute("DELETE FROM Players")
    connection.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    result = cursor.execute("SELECT COUNT(*) AS num FROM Players")
    # Get count value for function return
    return cursor.fetchall()[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    cursor.execute("INSERT INTO Players(name) VALUES (%s)", (name,))
    connection.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the numer of matches the player has played
    """
    # Use standings view
    cursor.execute("SELECT * FROM standings")
    connection.commit()
    return cursor.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cursor.execute("INSERT INTO Matches(winner, loser) VALUES (%s, %s)", (winner, loser))
    connection.commit()


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
    # Pair every two by ranking using rank view
    cursor.execute("SELECT A.id AS id1, A.name as name1, B.id AS id2, B.name as name2 FROM ranks AS A, ranks AS B WHERE A.rank+1 = B.rank AND A.rank % 2 = 1")
    return cursor.fetchall()
