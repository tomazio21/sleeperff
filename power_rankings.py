class PowerRankings:
    def __init__(self, matchups, num_of_teams):
        self.matchups = matchups
        self.num_of_teams = num_of_teams
        self.dom_matrix = self.get_empty_matrix(num_of_teams)
        self.dom_matrix_second = self.get_empty_matrix(num_of_teams)
        self.supremacy_matrix = self.get_empty_matrix(num_of_teams)

    def get_empty_matrix(self, n):
        return [[0 for j in range(n)] for i in range(n)]

    def calculate_dominance_matrix(self):
        for matchup in self.matchups:
            i,j = matchup.get_power_ranking_coords()
            self.dom_matrix[i][j] += 1 

    def calculate_dominance_matrix_second(self):
        matrix_len = self.num_of_teams 
        result = self.get_empty_matrix(self.num_of_teams)
        for i in range(matrix_len):
            for j in range(matrix_len):
                for k in range(matrix_len):
                    result[i][j] += self.dom_matrix[i][k] * self.dom_matrix[k][j]
        self.dom_matrix_second = result

    def calculate_supremacy_matrix(self, weighting):
        matrix_len = self.num_of_teams 
        result = self.get_empty_matrix(self.num_of_teams)
        for i in range(matrix_len):
            for j in range(matrix_len):
                    result[i][j] += self.dom_matrix[i][j] + (weighting* self.dom_matrix_second[i][j])
        self.supremacy_matrix = result

    def get_scoreboard(self, weighting):
        self.calculate_dominance_matrix()
        self.calculate_dominance_matrix_second()
        self.calculate_supremacy_matrix(weighting)
        power_rankings = {}
        for i in range(self.num_of_teams):
            power_rankings[i+1]=sum(self.supremacy_matrix[i])
        power_rankings = dict(sorted(power_rankings.items(), key=lambda item: item[1], reverse=True))
        return power_rankings
