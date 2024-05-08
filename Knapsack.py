import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PLNE import solve_knapsack

class KnapsackApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('sus.png'))
        self.setWindowTitle("Problème de sac à dos")

    def initUI(self):
        self.setWindowTitle("Problème de sac à dos")

        window_width = 1000
        window_height = 900
        screen_geometry = app.primaryScreen().geometry()
        x_coordinate = int((screen_geometry.width() / 2) - (window_width / 2))
        y_coordinate = int((screen_geometry.height() / 2) - (window_height / 2))
        self.resize(window_width, window_height)
        self.move(x_coordinate, y_coordinate)

        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("bg.jpg").scaledToWidth(self.width()).scaledToHeight(
            self.height())
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.project_name = QLabel("Problème de sac à dos", self)
        self.project_name.setStyleSheet("color: #FFD700; font-family: Trebuchet MS; font-size: 24px;")  # Dark gray color, Arial font
        self.project_name.setAlignment(Qt.AlignCenter)

        self.project_description = QLabel("Saisir les données:", self)
        self.project_description.setStyleSheet(
            "color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")
        self.project_description.setAlignment(Qt.AlignCenter)
        self.productsLabel = QLabel("Produits (séparés par des virgules):", self)
        self.productsEdit = QLineEdit(self)
        self.valuesLabel = QLabel("Valeurs (séparés par des virgules):", self)
        self.valuesEdit = QLineEdit(self)
        self.weightsLabel = QLabel("Poids (séparés par des virgules):", self)
        self.weightsEdit = QLineEdit(self)
        self.nameOfSacksLabel = QLabel("Noms des contenaires (séparés par des virgules):", self)
        self.nameOfSacksEdit = QLineEdit(self)
        self.capacityLabel = QLabel("Capacités des contenaires (séparés par des virgules):", self)
        self.capacityEdit = QLineEdit(self)

        self.solveButton = QPushButton("Optimiser", self)

        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_description)
        layout.addWidget(self.productsLabel)
        layout.addWidget(self.productsEdit)
        layout.addWidget(self.valuesLabel)
        layout.addWidget(self.valuesEdit)
        layout.addWidget(self.weightsLabel)
        layout.addWidget(self.weightsEdit)
        layout.addWidget(self.nameOfSacksLabel)
        layout.addWidget(self.nameOfSacksEdit)
        layout.addWidget(self.capacityLabel)
        layout.addWidget(self.capacityEdit)
        layout.addWidget(self.solveButton)
        layout.addWidget(self.resultTextEdit)

        self.solveButton.clicked.connect(self.solveKnapsack)

        self.applyStyles()

    def center(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = self.frameGeometry()
        x_coordinate = (screen_geometry.width() - window_geometry.width()) / 2
        y_coordinate = (screen_geometry.height() - window_geometry.height()) / 2
        self.move(x_coordinate, y_coordinate)

    def applyStyles(self):
        font = QFont("Trebuchet MS", 14, QFont.Bold)
        label_color = "#FFFFFF"
        label_style = f"color: {label_color};"
        label_font = font

        self.productsLabel.setStyleSheet(label_style)
        self.productsLabel.setFont(label_font)
        self.valuesLabel.setStyleSheet(label_style)
        self.valuesLabel.setFont(label_font)
        self.weightsLabel.setStyleSheet(label_style)
        self.weightsLabel.setFont(label_font)
        self.nameOfSacksLabel.setStyleSheet(label_style)
        self.nameOfSacksLabel.setFont(label_font)
        self.capacityLabel.setStyleSheet(label_style)
        self.capacityLabel.setFont(label_font)

        lineedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        lineedit_font = font
        self.productsEdit.setStyleSheet(lineedit_style)
        self.productsEdit.setFont(lineedit_font)
        self.valuesEdit.setStyleSheet(lineedit_style)
        self.valuesEdit.setFont(lineedit_font)
        self.weightsEdit.setStyleSheet(lineedit_style)
        self.weightsEdit.setFont(lineedit_font)
        self.nameOfSacksEdit.setStyleSheet(lineedit_style)
        self.nameOfSacksEdit.setFont(lineedit_font)
        self.capacityEdit.setStyleSheet(lineedit_style)
        self.capacityEdit.setFont(lineedit_font)

        textedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        textedit_font = font
        self.resultTextEdit.setStyleSheet(textedit_style)
        self.resultTextEdit.setFont(textedit_font)

        button_style = f"color: #FFFFFF; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 5px;"
        button_font = font
        self.solveButton.setStyleSheet(button_style)
        self.solveButton.setFont(button_font)

    def solveKnapsack(self):
        try:
            products = self.productsEdit.text().split(',')
            values = [float(x) for x in self.valuesEdit.text().split(',')]
            weights = [float(x) for x in self.weightsEdit.text().split(',')]
            nameOfSacks = self.nameOfSacksEdit.text().split(',')
            capacities = [float(x) for x in self.capacityEdit.text().split(',')]
            result_str = "Solution: \n\n"
            for i in range(len(capacities)):

                total_value, selected_items = solve_knapsack(values, weights, capacities[i])
                result_str += f"Contenaire : {nameOfSacks[i]}\n"
                result_str += f"Valeur Totale: {int(total_value)}\n"
                result_str += "Les produits choisis:\n"
                result_str += "\n".join(f"{value} de {products[key]}" for key, value in selected_items.items())
                result_str += "\n\n"
                self.resultTextEdit.setPlainText(result_str)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KnapsackApp()
    ex.show()
    sys.exit(app.exec_())
