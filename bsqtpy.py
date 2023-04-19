import sys
from PyQt5.QtWidgets import QApplication
from scoreboardwindow import ScoreboardWindow

app = QApplication(sys.argv)
app.setStyle("Fusion")

window = ScoreboardWindow()
window.show()

app.exec()