import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PL import optimal_electricity_supply

def exit_program():
    app.quit()

class ElectricitySupplyApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('sus.png'))
        self.setWindowTitle("Optimisation de l'approvisionnement en électricité")

    def initUI(self):
        # Set window size and position
        window_width = 1000
        window_height = 800
        screen_geometry = app.primaryScreen().geometry()
        x_coordinate = int((screen_geometry.width() / 2) - (window_width / 2))
        y_coordinate = int((screen_geometry.height() / 2) - (window_height / 2))
        self.resize(window_width, window_height)
        self.move(x_coordinate, y_coordinate)

        # Apply background image to window using stylesheet
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("bg.jpg").scaledToWidth(self.width()).scaledToHeight(self.height())  # Scale pixmap to window width
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        # Project Name in the middle at the top
        self.project_name = QLabel("Optimisation de l'approvisionnement en électricité", self)
        self.project_name.setStyleSheet(
            "color: #FFD700; font-family: Trebuchet MS; font-size: 28px;")  # Gold color, Impact font
        self.project_name.setAlignment(Qt.AlignCenter)

        # Description of the project
        self.project_description = QLabel("Saisir les données", self)
        self.project_description.setStyleSheet(
            "color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")  # White color, Arial font
        self.project_description.setAlignment(Qt.AlignCenter)

        # Labels and LineEdits for input data
        self.centralLabel = QLabel("Centrales(séparés par des virgules):", self)
        self.centralEdit = QLineEdit(self)
        self.cityLabel = QLabel("Villes(séparés par des virgules):", self)
        self.cityEdit = QLineEdit(self)
        self.supplyLabel = QLabel("Offres(séparés par des virgules):", self)
        self.supplyEdit = QLineEdit(self)
        self.demandLabel = QLabel("Demandes(séparés par des virgules):", self)
        self.demandEdit = QLineEdit(self)
        self.transportCostLabel = QLabel("Coûts de transport(séparés par des virgules):", self)
        self.transportCostEdit = QTextEdit(self)

        self.optimizeButton = QPushButton("Optimiser", self)

        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        self.totalCostLabel = QLabel("Coût total:", self)
        self.totalCostValueLabel = QLabel(self)


        self.applyStyles()

        layout = QVBoxLayout()
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_description)
        layout.addWidget(self.centralLabel)
        layout.addWidget(self.centralEdit)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.cityEdit)
        layout.addWidget(self.supplyLabel)
        layout.addWidget(self.supplyEdit)
        layout.addWidget(self.demandLabel)
        layout.addWidget(self.demandEdit)
        layout.addWidget(self.transportCostLabel)
        layout.addWidget(self.transportCostEdit)
        layout.addWidget(self.optimizeButton)
        layout.addWidget(self.resultTextEdit)
        layout.addWidget(self.totalCostLabel)
        layout.addWidget(self.totalCostValueLabel)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.optimizeButton.clicked.connect(self.optimize)

    def applyStyles(self):
        font = QFont("Trebuchet MS", 14, QFont.Bold)

        label_color = "#FFFFFF"
        label_style = f"color: {label_color};"
        label_font = font
        self.centralLabel.setStyleSheet(label_style)
        self.centralLabel.setFont(label_font)
        self.cityLabel.setStyleSheet(label_style)
        self.cityLabel.setFont(label_font)
        self.supplyLabel.setStyleSheet(label_style)
        self.supplyLabel.setFont(label_font)
        self.demandLabel.setStyleSheet(label_style)
        self.demandLabel.setFont(label_font)
        self.transportCostLabel.setStyleSheet(label_style)
        self.transportCostLabel.setFont(label_font)
        self.totalCostLabel.setStyleSheet(label_style)
        self.totalCostLabel.setFont(label_font)

        # Apply styles to LineEdits
        lineedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        lineedit_font = font
        self.centralEdit.setStyleSheet(lineedit_style)
        self.centralEdit.setFont(lineedit_font)
        self.cityEdit.setStyleSheet(lineedit_style)
        self.cityEdit.setFont(lineedit_font)
        self.supplyEdit.setStyleSheet(lineedit_style)
        self.supplyEdit.setFont(lineedit_font)
        self.demandEdit.setStyleSheet(lineedit_style)
        self.demandEdit.setFont(lineedit_font)

        # Apply styles to QTextEdit
        textedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        textedit_font = font
        self.transportCostEdit.setStyleSheet(textedit_style)
        self.transportCostEdit.setFont(textedit_font)
        self.resultTextEdit.setStyleSheet(textedit_style)
        self.resultTextEdit.setFont(textedit_font)

        # Apply styles to QPushButton
        button_style = f"color: #FFFFFF; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 5px;"
        button_font = font
        self.optimizeButton.setStyleSheet(button_style)
        self.optimizeButton.setFont(button_font)

        # Apply styles to result labels
        result_label_style = f"color: #FFD700;"  # Gold color
        result_label_font = QFont("Trebuchet MS", 14)  # Remove bold for result values
        self.totalCostValueLabel.setStyleSheet(result_label_style)
        self.totalCostValueLabel.setFont(result_label_font)

    def optimize(self):
        # Retrieve input data
        centrales = self.centralEdit.text().split(',')
        villes = self.cityEdit.text().split(',')

        offres_list = [float(x) for x in self.supplyEdit.text().split(',')]
        demandes_list = [float(x) for x in self.demandEdit.text().split(',')]

        text = self.transportCostEdit.toPlainText().strip()
        lines = text.split('\n')
        all_couts = []

        for line in lines:
            values = line.split(',')
            row = [float(value.strip()) for value in values]
            all_couts.append(row)

        offres = dict(zip(centrales, offres_list))
        demandes = dict(zip(villes, demandes_list))
        couts_transport = {}
        for i, c in enumerate(centrales):
            for j, v in enumerate(villes):
                couts_transport[(c, v)] = all_couts[i][j]

        # Solve problem
        total_cost, resultat = optimal_electricity_supply(centrales, villes, offres, demandes,
                                                                              couts_transport)

        self.resultTextEdit.setPlainText(resultat)
        self.totalCostValueLabel.setText(f"{total_cost:.2f} millions d'euros")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ElectricitySupplyApp()
    ex.show()
    sys.exit(app.exec_())