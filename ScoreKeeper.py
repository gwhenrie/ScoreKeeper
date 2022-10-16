from multiprocessing.sharedctypes import Value
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QVBoxLayout,
                             QTableWidget,
                             QTableWidgetItem,
                             QHBoxLayout,
                             QLineEdit,
                             QCheckBox) 
from PyQt5.QtGui import QColor

class ScoreKeeper(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Score Keeper')

        # Set up the new player code
        self.playerLayout = QHBoxLayout()
        self.newPlayer = QLineEdit()
        self.newPlayer.editingFinished.connect(self.add_player)
        self.playerLayout.addWidget(self.newPlayer)
        self.numberOfPlayers = 0
        self.addPlayer = QPushButton('Add Player')
        self.addPlayer.clicked.connect(self.add_player)
        self.playerLayout.addWidget(self.addPlayer)

        # Set up the main Layout, placing the new player above the table
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.playerLayout)

        # High or Low wins
        self.lowWins = QCheckBox('Check if lowest score wins')
        self.mainLayout.addWidget(self.lowWins)

        # Table of scores
        self.table = QTableWidget()
        self.mainLayout.addWidget(self.table)
        self.setLayout(self.mainLayout)

        # Set up the TOTAL row
        self.numRounds = 1
        self.table.setRowCount(self.numRounds)
        self.table.setVerticalHeaderItem(0, QTableWidgetItem('Total'))
        self.table.currentCellChanged.connect(self.calculate_total)

        self.newRound = QPushButton('New Round')
        self.newRound.clicked.connect(self.new_round)
        self.mainLayout.addWidget(self.newRound)

    def show_winner(self):
        # Depending on if the lowWins is checked or not 
        # highlight the column of the winner.
        # See who is currently winning 
        winner = 0
        peopleTied = set()
        winValue = int(self.table.item(self.table.rowCount() - 1, winner).text())
        if self.lowWins.isChecked():
            # Low wins 
            for total in range(1, self.table.columnCount()):
                value = int(self.table.item(self.table.rowCount() - 1, total).text())
                if value < winValue: 
                    winner = total 
                    winValue = value
                    peopleTied = set()
                elif value == winValue:
                    peopleTied.add(total)
        else: 
            # High wins
            for total in range(1, self.table.columnCount()):
                value = int(self.table.item(self.table.rowCount() - 1, total).text())
                if value > winValue: 
                    winner = total 
                    winValue = value
                    peopleTied = set()
                elif value == winValue:
                    peopleTied.add(total)

        peopleTied.add(winner)
        for player in peopleTied:
            # Highlight the winner(s) by changing their total text color
            self.table.item(self.table.rowCount() - 1, player).setForeground(QColor(0,255,0))

        # Make sure that those who are not winning are not highlighed 
        losers = set(range(self.table.columnCount())) - peopleTied
        for player in losers:
            self.table.item(self.table.rowCount() - 1, player).setForeground(QColor(0,0,0))



    def calculate_total(self):
        # For each player, calculate their score 
        # print(f'Columns: {self.table.columnCount()}, Rows: {self.table.rowCount()}')
        for player in range(self.table.columnCount()):
            # Iterate through each row 
            totalScore = 0 
            for round in range(self.table.rowCount() - 1):
                if self.table.item(round, player) != None:
                    roundScore = self.table.item(round, player).text()
                    try:
                        totalScore += int(roundScore)
                    except ValueError:
                        totalScore += 0
                else: 
                    totalScore += 0
            total = QTableWidgetItem(f'{totalScore}')
            self.table.setItem(self.table.rowCount()-1, player, total)
        self.show_winner()

    def add_player(self):
        # Get the player name text 
        playerName = self.newPlayer.text()
        if playerName != '':
            self.numberOfPlayers += 1
            self.table.setColumnCount(self.numberOfPlayers)
            self.table.setHorizontalHeaderItem(self.numberOfPlayers - 1, QTableWidgetItem(playerName))
            self.newPlayer.setText('')

    def new_round(self):
        self.numRounds += 1
        self.table.insertRow(0)

if __name__ == "__main__":
    app = QApplication([])
    window = ScoreKeeper()
    window.show()
    app.exec()