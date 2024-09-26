class Team:
    def __init__(self, display_name, user_id):
        self.display_name = display_name
        self.user_id = user_id
        self.roster_id = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.pf = 0
        self.pa = 0

    def add_roster_data(self, roster_id, wins, losses, ties, pf, pa):
        self.roster_id = roster_id
        self.wins = wins
        self.losses = losses 
        self.ties = ties
        self.pf = pf
        self.pa = pa
