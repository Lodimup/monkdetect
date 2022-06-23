class Source:
    def __init__(self, path):
        self.path = path
        self.scores = []
        self.curr_avg_score = 0

    def append_score(self, score):
        if len(self.scores) >= 10:
            self.scores = self.scores[1:]
        self.scores.append(score)
        self.calc_avg_score()

    def calc_avg_score(self):
        if len(self.scores) != 0:
            self.curr_avg_score = sum(self.scores) / len(self.scores)
            return self.curr_avg_score

        return 0

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
