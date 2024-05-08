import sys
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PL import optimal_transportation_supply

def exit_program():
    app.quit()

class TransportSupplyApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('sus.png'))
        self.setWindowTitle("Optimisation de l'approvisionnement de transport")

    def initUI(self):
        window_width = 1000
        window_height = 1000
        screen_geometry = app.primaryScreen().geometry()
        x_coordinate = int((screen_geometry.width() / 2) - (window_width / 2))
        y_coordinate = int((screen_geometry.height() / 2) - (window_height / 2))
        self.resize(window_width, window_height)
        self.move(x_coordinate, y_coordinate)

        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("bg.jpg").scaledToWidth(self.width()).scaledToHeight(self.height())  # Scale pixmap to window width
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.project_name = QLabel("Optimisation de l'approvisionnement de transport", self)
        self.project_name.setStyleSheet(
            "color: #FFD700; font-family: Trebuchet MS; font-size: 28px;")  # Gold color, Impact font
        self.project_name.setAlignment(Qt.AlignCenter)

        self.project_description = QLabel("Saisir les données", self)
        self.project_description.setStyleSheet(
            "color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")  # White color, Arial font
        self.project_description.setAlignment(Qt.AlignCenter)
        self.materialLabel = QLabel("Matière à transporter :", self)
        self.materialEdit = QLineEdit(self)
        self.materialUnitLabel = QLabel("Unité de la matière :", self)
        self.materialUnitEdit  = QLineEdit(self)
        self.currencyLabel = QLabel("Monnaie :", self)
        self.currencyEdit = QLineEdit(self)
        self.centralLabel = QLabel("Centrales(séparés par des virgules):", self)
        self.centralEdit = QLineEdit(self)
        self.centralEdit.setPlaceholderText("Centrale 1,Centrale 2, ...")
        self.cityLabel = QLabel("Villes(séparés par des virgules):", self)
        self.cityEdit = QLineEdit(self)
        self.cityEdit.setPlaceholderText("Ville 1,Ville 2, ...")
        self.supplyLabel = QLabel("Offres(séparés par des virgules):", self)
        self.supplyEdit = QLineEdit(self)
        self.supplyEdit.setPlaceholderText("123,123, ...")
        self.demandLabel = QLabel("Demandes(séparés par des virgules):", self)
        self.demandEdit = QLineEdit(self)
        self.demandEdit.setPlaceholderText("123,123, ...")
        self.transportCostLabel = QLabel("Coûts de transport :", self)
        self.matrixTable = QTableWidget()
        self.matrixTable.setRowCount(1)  # Default size
        self.matrixTable.setColumnCount(1)

        self.optimizeButton = QPushButton("Optimiser", self)

        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        self.totalCostLabel = QLabel("Coût total :", self)
        self.totalCostValueLabel = QLabel(self)

        self.centralEdit.editingFinished.connect(self.setupMatrix)
        self.cityEdit.editingFinished.connect(self.setupMatrix)

        self.applyStyles()

        # Group 1: Matière à transporter
        material_layout = QVBoxLayout()
        material_layout.addWidget(self.materialLabel)
        material_layout.addWidget(self.materialEdit)

        # Group 2: Unité de la matière
        material_unit_layout = QVBoxLayout()
        material_unit_layout.addWidget(self.materialUnitLabel)
        material_unit_layout.addWidget(self.materialUnitEdit)

        # Group 3: Monnaie
        currency_layout = QVBoxLayout()
        currency_layout.addWidget(self.currencyLabel)
        currency_layout.addWidget(self.currencyEdit)

        # Row layout for the first three groups
        top_row_layout = QHBoxLayout()
        top_row_layout.addLayout(material_layout)
        top_row_layout.addSpacing(20)  # Add spacing between groups
        top_row_layout.addLayout(material_unit_layout)
        top_row_layout.addSpacing(20)  # Add spacing between groups
        top_row_layout.addLayout(currency_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_description)
        layout.addLayout(top_row_layout)
        layout.addWidget(self.centralLabel)
        layout.addWidget(self.centralEdit)
        layout.addWidget(self.cityLabel)
        layout.addWidget(self.cityEdit)
        layout.addWidget(self.supplyLabel)
        layout.addWidget(self.supplyEdit)
        layout.addWidget(self.demandLabel)
        layout.addWidget(self.demandEdit)
        layout.addWidget(self.transportCostLabel)
        layout.addWidget(self.matrixTable)
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
        self.materialLabel.setStyleSheet(label_style)
        self.materialLabel.setFont(label_font)
        self.materialUnitLabel.setStyleSheet(label_style)
        self.materialUnitLabel.setFont(label_font)
        self.currencyLabel.setStyleSheet(label_style)
        self.currencyLabel.setFont(label_font)
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

        lineedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        lineedit_font = font
        self.materialEdit.setStyleSheet(lineedit_style)
        self.materialEdit.setFont(lineedit_font)
        self.materialUnitEdit.setStyleSheet(lineedit_style)
        self.materialUnitEdit.setFont(lineedit_font)
        self.currencyEdit.setStyleSheet(lineedit_style)
        self.currencyEdit.setFont(lineedit_font)

        self.centralEdit.setStyleSheet(lineedit_style)
        self.centralEdit.setFont(lineedit_font)
        self.cityEdit.setStyleSheet(lineedit_style)
        self.cityEdit.setFont(lineedit_font)
        self.supplyEdit.setStyleSheet(lineedit_style)
        self.supplyEdit.setFont(lineedit_font)
        self.demandEdit.setStyleSheet(lineedit_style)
        self.demandEdit.setFont(lineedit_font)

        textedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        textedit_font = font

        self.resultTextEdit.setStyleSheet(textedit_style)
        self.resultTextEdit.setFont(textedit_font)

        button_style = f"color: #FFFFFF; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 5px;"
        button_font = font
        self.optimizeButton.setStyleSheet(button_style)
        self.optimizeButton.setFont(button_font)

        result_label_style = f"color: #FFD700;"
        result_label_font = QFont("Trebuchet MS", 14)
        self.totalCostValueLabel.setStyleSheet(result_label_style)
        self.totalCostValueLabel.setFont(result_label_font)

        # Styles for the matrix table
        table_style = """
                QTableWidget {
                    background-color: #2E2E2E;
                    border: 2px solid #808080;
                    border-radius: 5px;
                    color: #FFFFFF;
                }
                QTableWidget::item {
                }
                QHeaderView::section {
                    background-color: #4CAF50;
                    color: #FFFFFF;
                    border: none;
                    font-weight: bold;
                }
            """
        self.matrixTable.setStyleSheet(table_style)
        self.matrixTable.setFont(font)

    def setupMatrix(self):
        centrales = self.centralEdit.text().split(',')
        villes = self.cityEdit.text().split(',')  # Including depot

        self.matrixTable.setRowCount(len(centrales))
        self.matrixTable.setColumnCount(len(villes))
        self.matrixTable.setHorizontalHeaderLabels(villes)
        self.matrixTable.setVerticalHeaderLabels(centrales)
        for i in range(len(centrales)):
            for j in range(len(villes)):
                if self.matrixTable.item(i, j) is None:
                    self.matrixTable.setItem(i, j, QTableWidgetItem("0"))

    def optimize(self):
        try:
            centrales = self.centralEdit.text().split(',')
            villes = self.cityEdit.text().split(',')
            monnaie = self.currencyEdit.text()
            matiere = self.materialEdit.text()
            unite_matiere = self.materialUnitEdit.text()

            offres_list = [float(x) for x in self.supplyEdit.text().split(',')]
            demandes_list = [float(x) for x in self.demandEdit.text().split(',')]

            all_couts = []

            for i in range(len(centrales)):
                row = []
                for j in range(len(villes)):
                    row.append(float(self.matrixTable.item(i, j).text()))
                all_couts.append(row)

            offres = dict(zip(centrales, offres_list))
            demandes = dict(zip(villes, demandes_list))
            couts_transport = {}
            for i, c in enumerate(centrales):
                for j, v in enumerate(villes):
                    couts_transport[(c, v)] = all_couts[i][j]

            total_cost, resultat = optimal_transportation_supply(centrales, villes, offres, demandes,
                                                                 couts_transport, matiere, unite_matiere, monnaie)

            self.resultTextEdit.setPlainText(resultat)
            self.totalCostValueLabel.setText(f"{total_cost:.2f} {monnaie}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Le modèle est irréalisable. Vérifiez les contraintes.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TransportSupplyApp()
    ex.show()
    sys.exit(app.exec_())