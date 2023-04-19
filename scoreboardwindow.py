from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from startmatchform import StartMatchDialog
from matchplayer import MatchPlayer
from match import Match
import json

class ScoreboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Biljart Scorebord")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: black; color: white;")

        main = QVBoxLayout()

        container = QWidget()
        container.setLayout(main)
        self.setCentralWidget(container)

        head = QHBoxLayout()
        head.setSpacing(10)
        head.setContentsMargins(0, 0, 0, 0)
        main.addLayout(head, 25)

        middle = QHBoxLayout()
        middle.setSpacing(10)
        middle.setContentsMargins(0, 0, 0, 0)
        main.addLayout(middle, 65)

        bottom = QHBoxLayout()
        bottom.setSpacing(10)
        bottom.setContentsMargins(0, 0, 0, 0)
        main.addLayout(bottom, 10)

        # Player 1
        head.addWidget(self.createPlayer1Info(), 50)
        middle.addWidget(self.createPlayer1Score(), 40)
        bottom.addLayout(self.createPlayer1Summary(), 50)

        # Inning and self.score entry
        middle.addLayout(self.createInningScore(), 20)

        # Player 2
        head.addWidget(self.createPlayer2Info(), 50)
        middle.addLayout(self.createPlayer2Score(), 40)
        bottom.addLayout(self.createPlayer2Summary(), 50)

        self.startNewMatch()

    def createInningScore(self):
        inning_score = QVBoxLayout()
        inning_score.setSpacing(10)
        inning_score.setContentsMargins(0, 0, 0, 0)
        self.inning = QLabel("99")
        self.inning.setFont(QFont("Arial", 176))
        self.inning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inning_score.addWidget(self.inning)
        self.score = QLineEdit()
        self.score.setFont(QFont("Arial", 64))
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score.returnPressed.connect(self.scoreEntered)
        inning_score.addWidget(self.score)
        return inning_score
    
    def scoreEntered(self):
        if self.score.text().isnumeric():
            if self.current_player == 1:
                self.match.player1.scores.append(int(self.score.text()))
                self.p1_score.setText(str(self.match.player1.getScore()))
                self.inning.setText(str(int(self.inning.text()) + 1))
                self.updatePlayer1Summary()
                self.current_player = 2
                if self.match.player1.isPointsReached():
                    self.ended = True
                    self.showEqualizingInning()
            else:
                self.match.player2.scores.append(int(self.score.text()))
                self.p2_score.setText(str(self.match.player2.getScore()))
                self.updatePlayer2Summary()
                self.current_player = 1
                if self.match.player2.isPointsReached() or self.ended:
                    self.ended = True
                    self.showEndResult()
            self.saveMatch()
            self.score.setText("")
            if self.inning.text() == "1":
                self.started = True
                self.ended = False
        elif self.score.text() != "" and self.score.text()[0] == "/":
            command = self.score.text()[1:]
            if command == "*":
                self.switchPlayers()
                self.score.setText("")
            elif command == "9":
                self.startNewMatch()
            elif command == "/":
                self.undoLastScore()
                self.score.setText("")
            else:
                self.score.setStyleSheet("background-color: red;")

    def switchPlayers(self):
        if not self.started:
            player = self.match.player1
            self.match.player1 = self.match.player2
            self.match.player2 = player
            self.updatePlayer1Info()
            self.updatePlayer2Info()

    def updatePlayer2Info(self):
        self.p2_name.setText(self.match.player2.name)
        self.p2_club_team.setText(self.match.player2.club)
        self.p2_discipline.setText(self.match.player2.discipline)
        self.p2_ptbm.setText(str(self.match.player2.points))

    def updatePlayer1Info(self):
        self.p1_name.setText(self.match.player1.name)
        self.p1_club_team.setText(self.match.player1.club)
        self.p1_discipline.setText(self.match.player1.discipline)
        self.p1_ptbm.setText(str(self.match.player1.points))

    def saveMatch(self):
        json_object = json.dumps(self.match.toJson(), indent=4)
        with open(self.match.filename, "w") as f:
            f.write(json_object)

    def showEqualizingInning(self):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setStyleSheet("background-color: white; color: black;")
        dlg.setWindowTitle("Gelijkmakende beurt!")
        dlg.setText(self.match.player2.name + " nog " + str(self.match.player2.getRemainingPoints()) + " punten nodig om gelijk te komen.")
        dlg.exec()

    def showEndResult(self):
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setStyleSheet("background-color: white; color: black;")
        dlg.setWindowTitle("Einde van de wedtrijd!")
        if self.match.player1.isPointsReached() and self.match.player2.isPointsReached():
            dlg.setText("Gelijkspel!")
        elif self.match.player1.isPointsReached():
            dlg.setText(self.match.player1.name + " heeft gewonnen!")
        else:
            dlg.setText(self.match.player2.name + " heeft gewonnen!")
        dlg.exec()
        self.startNewMatch()

    def undoLastScore(self):
        if self.started:
            if self.current_player == 1:
                if len(self.match.player2.scores) > 0:
                    self.match.player2.scores.pop()
                    self.p2_score.setText(str(self.match.player2.getScore()))
                    self.updatePlayer2Summary()
                    self.current_player = 2
            else:
                if len(self.p1_scores) > 0:
                    self.match.player1.scores.pop()
                    self.p1_score.setText(str(self.match.player1.getScore()))
                    self.updatePlayer1Summary()
                    self.current_player = 1

    def updatePlayer2Summary(self):
        if len(self.match.player2.scores) > 0: 
            self.p2_average.setText(str(self.match.player2.getAverage()))
            self.p2_highrun.setText(str(self.match.player2.getHighrun()))
            self.p2_percentage.setText(str(self.match.player2.getPercentage()))
            self.p2_lastscores.setText(str(self.match.player2.getLastScores()))
        else:
            self.p2_average.setText("0.000")
            self.p2_highrun.setText("0")
            self.p2_percentage.setText("0.00")
            self.p2_lastscores.setText("")
    

    def updatePlayer1Summary(self):
        if len(self.match.player1.scores) > 0: 
            self.p1_average.setText(
                    str(self.match.player1.getAverage()))
            self.p1_highrun.setText(str(self.match.player1.getHighrun()))
            self.p1_percentage.setText(
                    str(self.match.player1.getPercentage()))
            self.p1_lastscores.setText(str(self.match.player1.getLastScores()))
        else:
            self.p1_average.setText("0.000")
            self.p1_highrun.setText("0")
            self.p1_percentage.setText("0.00")
            self.p1_lastscores.setText("")

    def startNewMatch(self):
        startMatchDialog = StartMatchDialog()
        if startMatchDialog.exec():
            player1 = MatchPlayer(startMatchDialog.name1.text(), startMatchDialog.club1.text(), startMatchDialog.discipline1.currentText(), int(startMatchDialog.points1.text()))
            player2 = MatchPlayer(startMatchDialog.name2.text(), startMatchDialog.club2.text(), startMatchDialog.discipline2.currentText(), int(startMatchDialog.points2.text()))
            self.match = Match(player1, player2)
            self.updatePlayer1Info()
            self.updatePlayer2Info()

            if self.p1_discipline.text() == "":
                self.p1_discipline.setVisible(False)
                self.p1_discipline_ptbm_dash.setVisible(False)

            if self.p2_discipline.text() == "":
                self.p2_discipline.setVisible(False)
                self.p2_discipline_ptbm_dash.setVisible(False)

            self.current_player = 1
            self.p1_score.setText("0")
            self.p2_score.setText("0")
            self.inning.setText("0")
            self.p1_average.setText("0,000")
            self.p1_highrun.setText("0")
            self.p1_percentage.setText("0,00")
            self.p2_average.setText("0,000")
            self.p2_highrun.setText("0")
            self.p2_percentage.setText("0,00")
            self.started = False
        else:
            exit()

    def createPlayer2Summary(self):
        p2_summary = QVBoxLayout()

        summary1 = QHBoxLayout()

        self.p2_average = QLabel()
        self.p2_average.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_average.setFont(QFont("Arial", 32))
        self.p2_average.setText("99,999")
        summary1.addWidget(self.p2_average)

        self.p2_highrun = QLabel()
        self.p2_highrun.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_highrun.setFont(QFont("Arial", 32))
        self.p2_highrun.setText("999")
        summary1.addWidget(self.p2_highrun)

        self.p2_percentage = QLabel()
        self.p2_percentage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_percentage.setFont(QFont("Arial", 32))
        self.p2_percentage.setText("999")
        summary1.addWidget(self.p2_percentage)
        p2_summary.addLayout(summary1)

        summary2 = QHBoxLayout()
        self.p2_lastscores = QLabel()
        self.p2_lastscores.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_lastscores.setFont(QFont("Arial", 32))
        self.p2_lastscores.setText("")
        summary2.addWidget(self.p2_lastscores)
        p2_summary.addLayout(summary2)

        return p2_summary

    def createPlayer2Score(self):
        p2_middle = QVBoxLayout()

        self.p2_score = QLabel()
        self.p2_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_score.setFont(QFont("Arial", 176))
        self.p2_score.setText("999")
        p2_middle.addWidget(self.p2_score)
        return p2_middle

    def createPlayer2Info(self):
        p2_head_layout = QVBoxLayout()
        p2_head_layout.setSpacing(0)
        p2_head_layout.setContentsMargins(10, 10, 10, 10)
        p2_head_layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # type: ignore
        p2_head = QWidget()
        p2_head.setStyleSheet(
            "background-color: yellow; color: black; border-radius: 20px;")
        p2_head.setLayout(p2_head_layout)

        self.p2_name = QLabel()
        self.p2_name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_name.setFont(QFont("Arial", 64))
        self.p2_name.setText("")
        p2_head_layout.addWidget(self.p2_name)

        self.p2_club_team = QLabel()
        self.p2_club_team.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_club_team.setFont(QFont("Arial", 32))
        self.p2_club_team.setText("")
        p2_head_layout.addWidget(self.p2_club_team)

        p2_discipline_ptbm = QHBoxLayout()
        p2_discipline_ptbm.setSpacing(5)
        p2_discipline_ptbm.setContentsMargins(0, 0, 0, 0)
        p2_head_layout.addLayout(p2_discipline_ptbm)

        self.p2_discipline = QLabel()
        self.p2_discipline.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_discipline.setFont(QFont("Arial", 32))
        p2_discipline_ptbm.addWidget(self.p2_discipline)

        self.p2_discipline_ptbm_dash = QLabel()
        self.p2_discipline_ptbm_dash.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_discipline_ptbm_dash.setFont(QFont("Arial", 32))
        self.p2_discipline_ptbm_dash.setText(" - ")
        p2_discipline_ptbm.addWidget(self.p2_discipline_ptbm_dash)

        self.p2_ptbm = QLabel()
        self.p2_ptbm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_ptbm.setFont(QFont("Arial", 32))
        self.p2_ptbm.setText("")
        p2_discipline_ptbm.addWidget(self.p2_ptbm)
        return p2_head

    def createPlayer1Summary(self):
        p1_summary = QVBoxLayout()

        summary1 = QHBoxLayout()
        self.p1_average = QLabel()
        self.p1_average.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_average.setFont(QFont("Arial", 32))
        self.p1_average.setText("")
        summary1.addWidget(self.p1_average)

        self.p1_highrun = QLabel()
        self.p1_highrun.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_highrun.setFont(QFont("Arial", 32))
        self.p1_highrun.setText("")
        summary1.addWidget(self.p1_highrun)

        self.p1_percentage = QLabel()
        self.p1_percentage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_percentage.setFont(QFont("Arial", 32))
        self.p1_percentage.setText("")
        summary1.addWidget(self.p1_percentage)
        
        p1_summary.addLayout(summary1)
        summay2 = QHBoxLayout()
        self.p1_lastscores = QLabel()
        self.p1_lastscores.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_lastscores.setFont(QFont("Arial", 32))
        self.p1_lastscores.setText("")
        summay2.addWidget(self.p1_lastscores)
        p1_summary.addLayout(summay2)

        return p1_summary

    def createPlayer1Score(self):
        self.p1_score = QLabel()
        self.p1_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_score.setFont(QFont("Arial", 176))
        self.p1_score.setText("")
        return self.p1_score

    def createPlayer1Info(self):
        p1_head_layout = QVBoxLayout()
        p1_head_layout.setSpacing(0)
        p1_head_layout.setContentsMargins(10, 10, 10, 10)
        p1_head_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)  # type: ignore
        p1_head = QWidget()
        p1_head.setLayout(p1_head_layout)
        p1_head.setStyleSheet("background-color: white; color: black; border-radius: 20px;")

        self.p1_name = QLabel()
        self.p1_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_name.setFont(QFont("Arial", 72))
        self.p1_name.setText("")
        p1_head_layout.addWidget(self.p1_name)

        self.p1_club_team = QLabel()
        self.p1_club_team.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_club_team.setFont(QFont("Arial", 32))
        self.p1_club_team.setText("")
        p1_head_layout.addWidget(self.p1_club_team)

        p1_discipline_ptbm = QHBoxLayout()
        p1_discipline_ptbm.setSpacing(5)
        p1_discipline_ptbm.setContentsMargins(0, 0, 0, 0)
        p1_head_layout.addLayout(p1_discipline_ptbm)

        self.p1_discipline = QLabel()
        self.p1_discipline.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_discipline.setFont(QFont("Arial", 32))
        p1_discipline_ptbm.addWidget(self.p1_discipline)

        self.p1_discipline_ptbm_dash = QLabel()
        self.p1_discipline_ptbm_dash.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_discipline_ptbm_dash.setFont(QFont("Arial", 32))
        self.p1_discipline_ptbm_dash.setText(" - ")
        p1_discipline_ptbm.addWidget(self.p1_discipline_ptbm_dash)

        self.p1_ptbm = QLabel()
        self.p1_ptbm.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_ptbm.setFont(QFont("Arial", 32))
        self.p1_ptbm.setText("")
        p1_discipline_ptbm.addWidget(self.p1_ptbm)
        return p1_head
