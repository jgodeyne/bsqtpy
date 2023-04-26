# Combobox widget for selecting a discipline
from PyQt6.QtWidgets import QComboBox
class DisciplineWidget(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["","Vrijspel", "Band", "Drieband", "K38/2", "K57/2", "K47/2", "K47/1", "K71/2","K38/1", "K57/1"])
        self.setCurrentIndex(0)
        self.setEditable(False)
        self.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.setDuplicatesEnabled(False)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
