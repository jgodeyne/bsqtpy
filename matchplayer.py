class MatchPlayer:

    def __init__(self, name, club, discipline, points):
        self.name = name
        self.club = club
        self.discipline = discipline
        self.points = points
        self.scores = []

    def getAverage(self):
        if len(self.scores) == 0:
            return 0
        return round(sum(self.scores) / len(self.scores), 3)    
    def getHighrun(self):
        if len(self.scores) == 0:
            return 0
        return max(self.scores)
    
    def getPercentage(self):
        if len(self.scores) == 0:
            return 0
        return round((sum(self.scores) / self.points) * 100, 2)
    
    def getScore(self):
        return sum(self.scores)
    
    def getLastScores(self):
        if len(self.scores) == 0:
            return ""
        return " - ".join(map(str, self.scores[-5:]))

    def getRemainingPoints(self):
        return self.points - self.getScore()
    
    def isPointsReached(self):
        return self.getScore() >= self.points
        
    def toJson(self):
        return {"matchplayer": { 
                    "name": self.name,
                    "club": self.club,
                    "discipline": self.discipline,
                    "points": self.points,
                    "scores": self.scores,
                    "score": self.getScore(),
                    "innings": len(self.scores),
                    "average": self.getAverage(),
                    "highrun": self.getHighrun(),
                    "percentage": self.getPercentage()
                }
        }