from rlbot.utils.structures.game_data_struct import ScoreInfo


class RLBotInterfacer:
    """Interface for RLBot will be called to interface with the and automate starting and killing of python processes"""

    def __init__(self, match_ended_listener):
        """
        :param match_ended_listener:  A listener for the rest of the match maker to start its process.
        """
        self.match_ended_listener = match_ended_listener

    def start_match(self, config_path):
        """Starts a match, this assumes that you have gone to the main menu in the game itself."""

    def kill_bots(self):
        """Kills all running processes created by RLBot, does not kill external processes """

    def end_match(self):
        """Called to end the match early will make a call to the listener"""

    def on_match_end(self, score, stats):
        """
        Called when a match has ended.
        :param score: This contains a list of scores.  One score per a team.
                      In order so team 0 score is listed ten team 1
        :param stats: This contains the stats as how they appear on the scoreboard at the end of the game.
        """
        self.match_ended_listener(score, stats)

    def fake_end(self):
        """Fake test data maybe get called on a key press?"""
        player1 = ScoreInfo()
        player1.score = 1000
        player1.goals = 4
        player1.own_goals = 1
        player1.assists = 0
        player1.saves = 10
        player1.shots = 2
        player1.demolitions = 20
        fake_score_board = [{
            "gosling": player1
        }, {
            "player2": ScoreInfo()
        }]
        self.on_match_end([4, 6], fake_score_board)
