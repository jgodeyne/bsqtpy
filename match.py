import time
from matchplayer import MatchPlayer


class Match:

    def __init__(self, player1, player2):
        self.date = time.localtime(time.time())
        self.player1 = player1
        self.player2 = player2
        self.filename = self.getDateTimeAsString() + "-" + self.player1.name + \
            "-" + self.player2.name+".json"

    def toJson(self):
        return {"match": {
            "date": time.strftime("%Y-%m-%d %H:%M:%S", self.date),
                "player1": self.player1.toJson(),
                "player2": self.player2.toJson()
                }
                }

    def getDateAsString(self):
        return time.strftime("%Y-%m-%d", self.date)

    def getDateTimeAsString(self):
        return time.strftime("%Y%m%d%H%M%S", self.date)
