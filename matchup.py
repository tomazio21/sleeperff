class Matchup:
    def __init__(self, roster_id, score, week):
        self.roster_ids = []
        self.scores = []
        self.roster_ids.append(roster_id)
        self.scores.append(score)
        self.week = week

    def add_opponent_data(self, roster_id, score):
        self.roster_ids.append(roster_id)
        self.scores.append(score)

    def get_winner(self):
        if(self.scores[0] > self.scores[1]):
            return (self.scores[0], self.roster_ids[0])
        else:
            return (self.scores[1], self.roster_ids[1])

    def get_loser(self):
        if(self.scores[0] < self.scores[1]):
            return (self.scores[0], self.roster_ids[0])
        else:
            return (self.scores[1], self.roster_ids[1])

    def get_score_difference(self):
        return abs(self.scores[0] - self.scores[1])

    def get_power_ranking_coords(self):
        if(self.scores[0] > self.scores[1]):
            return (self.roster_ids[0]-1, self.roster_ids[1]-1)
        else:
            return (self.roster_ids[1]-1, self.roster_ids[0]-1)
