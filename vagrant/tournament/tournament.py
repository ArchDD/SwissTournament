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
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Matches")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Players")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    result = cursor.execute("SELECT COUNT(*) AS num FROM Players")
    # Get count value for function return
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
    cursor.execute("INSERT INTO Players(name) VALUES (%s)", (name,))
    connection.commit()
    connection.close()


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
    connection = connect()
    cursor = connection.cursor()
    # Use subqueries to count wins and matches
    wins = "SELECT COUNT(*) FROM Matches WHERE Matches.winner = Players.id"
    matches = "SELECT COUNT(*) FROM Matches WHERE Matches.p1 = Players.id OR Matches.p2 = Players.id"
    # Create a standings view to use
    cursor.execute("CREATE OR REPLACE VIEW standings AS SELECT Players.id, Players.name,("+wins+") AS wins, ("+matches+") AS matches FROM Players ORDER BY wins DESC")
    cursor.execute("SELECT * FROM standings")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Matches(p1, p2, winner) VALUES (%s, %s, %s)", (winner, loser, winner))
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
    connection = connect()
    cursor = connection.cursor()
    # Use standings view to generate ranking based on wins
    cursor.execute("CREATE OR REPLACE VIEW ranks AS SELECT ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank, id, name FROM standings")
    # Pairing every two closest competitors
    cursor.execute("SELECT A.id AS id1, A.name as name1, B.id AS id2, B.name as name2 FROM ranks AS A, ranks AS B WHERE A.rank+1 = B.rank AND A.rank % 2 = 1")
    result = cursor.fetchall()
    connection.close()
    return result
