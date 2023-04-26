from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from disciplineWidget import DisciplineWidget

class StartMatchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Maak de tekstvelden voor het invoeren van naam, club of team, discipline en te maken punten voor twee spelers.
        self.name1 = QLineEdit()
        self.name1.setMaxLength(25)
        self.name1.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9 ]+"), self.name1))
        self.club1 = QLineEdit()
        self.club1.setMaxLength(25)
        self.club1.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9 ]+"), self.club1))
        self.discipline1 = DisciplineWidget()
        self.points1 = QLineEdit()
        self.points1.setMaxLength(3)
        self.points1.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+"), self.points1))

        self.name2 = QLineEdit()
        self.name2.setMaxLength(25)
        self.name2.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9 ]+"), self.name2))
        self.club2 = QLineEdit()
        self.club2.setMaxLength(25)
        self.club2.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9 ]+"), self.club2))
        self.discipline2 = DisciplineWidget()
        self.points2 = QLineEdit()
        self.points2.setMaxLength(3)
        self.points2.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+"), self.points2))

        # Maak de labels voor elk van de tekstvelden.
        speler1Label = QLabel("Speler 1")
        speler1Label.setStyleSheet("font-weight: bold;")
        nameLabel1 = QLabel("Naam:")
        nameLabel1.setStyleSheet("font-weight: bold;")
        clubLabel1 = QLabel("Club of Team:")
        disciplineLabel1 = QLabel("Discipline:")
        pointsLabel1 = QLabel("TMP:")
        pointsLabel1.setStyleSheet("font-weight: bold;")

        speler2Label = QLabel("Speler 2")
        speler2Label.setStyleSheet("font-weight: bold;")
        nameLabel2 = QLabel("Naam:")
        nameLabel2.setStyleSheet("font-weight: bold;")
        clubLabel2 = QLabel("Club of Team:")
        disciplineLabel2 = QLabel("Discipline:")
        pointsLabel2 = QLabel("TMP:")
        pointsLabel2.setStyleSheet("font-weight: bold;")

        # Voeg de labels en tekstvelden toe aan een form layout.
        formLayout1 = QFormLayout()
        formLayout1.addRow(nameLabel1, self.name1)
        formLayout1.addRow(clubLabel1, self.club1)
        formLayout1.addRow(disciplineLabel1, self.discipline1)
        formLayout1.addRow(pointsLabel1, self.points1)

        formLayout2 = QFormLayout()
        formLayout2.addRow(nameLabel2, self.name2)
        formLayout2.addRow(clubLabel2, self.club2)
        formLayout2.addRow(disciplineLabel2, self.discipline2)
        formLayout2.addRow(pointsLabel2, self.points2)

        # Maak een knop en voeg deze toe aan een horizontale layout.
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close

        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        # Voeg de form layout en de horizontale layout toe aan een verticale layout.
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        gbox1 = QGroupBox()
        vbox1 = QVBoxLayout()
        gbox1.setLayout(vbox1)
        vbox1.addWidget(speler1Label)
        vbox1.addLayout(formLayout1)
        gbox2 = QGroupBox()
        vbox2 = QVBoxLayout()
        gbox2.setLayout(vbox2)
        vbox2.addWidget(speler2Label)
        vbox2.addLayout(formLayout2)
        hbox.addWidget(gbox1)
        hbox.addWidget(gbox2)
        vbox.addLayout(hbox)
        vbox.addWidget(buttonBox)

        # Stel de layout van het venster in op de verticale layout.
        self.setLayout(vbox)
        self.setWindowTitle('Nieuwe wedstrijd')
        self.show()

    def accept(self):
        # Controleer of de invoer geldig is.
        if self.name1.text() == "":
            self.name1.setFocus()
            self.name1.setStyleSheet("border: 1px solid red;")
            return
        elif self.points1.text() == "":
            self.points1.setFocus()
            self.points1.setStyleSheet("border: 1px solid red;")
            return
        elif self.name2.text() == "":
            self.name2.setFocus()
            self.name2.setStyleSheet("border: 1px solid red;")
            return
        elif self.points2.text() == "":
            self.points2.setFocus()
            self.points2.setStyleSheet("border: 1px solid red;")
            return
        else:
            super().accept()

    def close(self):
        exit()
