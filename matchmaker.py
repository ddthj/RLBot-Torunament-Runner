"""
Matchmaker Test v1 by GooseFairy/ddthj

This program generates a modified Swiss tournament that includes elimination to help minimize the number of matches and minimize unfairness
"""
from old_match_making.old_match import Old_Match

if __name__ == "__main__":
    z = Old_Match()
    z.runTournament(1)
