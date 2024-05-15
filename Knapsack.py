import sys
from PyQt5.QtWidgets import (QHBoxLayout, QMessageBox, QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QVBoxLayout, QScrollArea, QSizePolicy,
                             QFrame, QTableWidget, QHeaderView)
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PLNE import solve_knapsack

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
        pixmap = QPixmap("bg.jpg").scaledToWidth(self.width()).scaledToHeight(self.height())
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.project_name = QLabel("Problème de sac à dos", self)
        self.project_name.setStyleSheet("color: #FFD700; font-family: Trebuchet MS; font-size: 24px;")
        self.project_name.setAlignment(Qt.AlignCenter)

        self.project_description = QLabel("Saisir les données:", self)
        self.project_description.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")
        self.project_description.setAlignment(Qt.AlignCenter)

        # Initialize the columns with add buttons
        self.addProductButton = QPushButton('+ Ajouter Produit', self)
        self.addProductButton.clicked.connect(self.addProductInput)

        self.addValueButton = QPushButton('+ critères de valeurs', self)
        self.addValueButton.clicked.connect(self.addValueInput)

        self.addWeightButton = QPushButton('+ critères de poids', self)
        self.addWeightButton.clicked.connect(self.addWeightInput)

        # Product, Value, and Weight column layouts
        self.product_col_layout = QVBoxLayout()
        self.value_col_layout = QVBoxLayout()
        self.weight_col_layout = QVBoxLayout()

        self.matrixTable = QTableWidget()
        self.matrixTable.setRowCount(1)  # Default size
        self.matrixTable.setColumnCount(1)
        self.matrixTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.matrixTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.capacityLabel = QLabel("Capacité :", self)
        self.capacityEdit = QLineEdit(self)

        # Titles for each column
        product_title = QLabel("Produits", self)
        product_title.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 16px; font-weight: bold;")
        product_title.setAlignment(Qt.AlignCenter)

        value_title = QLabel("Valeurs", self)
        value_title.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 16px; font-weight: bold;")
        value_title.setAlignment(Qt.AlignCenter)

        weight_title = QLabel("Poids", self)
        weight_title.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 16px; font-weight: bold;")
        weight_title.setAlignment(Qt.AlignCenter)

        # Layouts for products, values, and weights with their add buttons at the top
        products_column_layout = QVBoxLayout()
        products_column_layout.addWidget(product_title)
        products_column_layout.addWidget(self.addProductButton)
        products_column_layout.addLayout(self.product_col_layout)

        values_column_layout = QVBoxLayout()
        values_column_layout.addWidget(value_title)
        values_column_layout.addWidget(self.addValueButton)
        values_column_layout.addLayout(self.value_col_layout)

        weights_column_layout = QVBoxLayout()
        weights_column_layout.addWidget(weight_title)
        weights_column_layout.addWidget(self.addWeightButton)
        weights_column_layout.addLayout(self.weight_col_layout)

        # Styling for columns with borders
        products_column_frame = QFrame()
        products_column_frame.setLayout(products_column_layout)
        products_column_frame.setFrameShape(QFrame.StyledPanel)
        products_column_frame.setFrameShadow(QFrame.Raised)
        products_column_frame.setStyleSheet("""
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #333;
            padding: 5px;
        """)

        values_column_frame = QFrame()
        values_column_frame.setLayout(values_column_layout)
        values_column_frame.setFrameShape(QFrame.StyledPanel)
        values_column_frame.setFrameShadow(QFrame.Raised)
        values_column_frame.setStyleSheet("""
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #333;
            padding: 5px;
        """)

        weights_column_frame = QFrame()
        weights_column_frame.setLayout(weights_column_layout)
        weights_column_frame.setFrameShape(QFrame.StyledPanel)
        weights_column_frame.setFrameShadow(QFrame.Raised)
        weights_column_frame.setStyleSheet("""
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #333;
            padding: 5px;
        """)

        # Layouts for main columns
        columns_layout = QVBoxLayout()
        columns_layout.addWidget(products_column_frame)
        columns_layout.addSpacing(20)

        inputs_row_layout = QHBoxLayout()
        inputs_row_layout.addWidget(values_column_frame)
        inputs_row_layout.addSpacing(20)
        inputs_row_layout.addWidget(weights_column_frame)
        columns_layout.addLayout(inputs_row_layout)

        self.solveButton = QPushButton("Optimiser", self)
        self.solveButton.clicked.connect(self.solveKnapsack)

        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.project_name)
        main_layout.addWidget(self.project_description)
        main_layout.addLayout(columns_layout)
        main_layout.addWidget(self.capacityLabel)
        main_layout.addWidget(self.capacityEdit)
        main_layout.addWidget(self.matrixTable)
        main_layout.addWidget(self.solveButton)
        main_layout.addWidget(self.resultTextEdit)

        # Scroll area to make the window scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Main widget for the scroll area
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.scroll_area.setWidget(main_widget)

        # Set the scroll area as the central layout
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(self.scroll_area)

        self.applyStyles()
        self.product_fields = {}
        self.value_fields = {}
        self.value_coeff = {}
        self.weight_fields = {}
        self.weight_coeff = {}

    def addProductInput(self):
        index = len(self.product_fields) + 1
        product_input_field = QLineEdit(self)

        # Apply the defined styles
        font = QFont("Trebuchet MS", 10, QFont.Bold)
        product_input_field.setFont(font)
        product_input_field.setStyleSheet(
            "color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;")

        # Layout for product input
        product_input_layout = QVBoxLayout()
        product_input_layout.addWidget(product_input_field)

        self.product_col_layout.addLayout(product_input_layout)
        self.product_fields[index] = product_input_field

        product_input_field.editingFinished.connect(self.setupMatrix)

        product_input_field.editingFinished.connect(self.setupMatrix)

    def addValueInput(self):
        index = len(self.value_fields) + 1
        criteria_label = QLabel(f'Critère {index}:', self)
        criteria_input_field = QLineEdit(self)

        coeff_label = QLabel(f'Coefficient {index}:', self)
        coeff_input_field = QLineEdit(self)

        # Apply the defined styles
        font = QFont("Trebuchet MS", 10, QFont.Bold)
        criteria_label.setFont(font)
        criteria_label.setStyleSheet("color: #FFFFFF;")
        coeff_label.setFont(font)
        coeff_label.setStyleSheet("color: #FFFFFF;")

        lineedit_style = "color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        criteria_input_field.setStyleSheet(lineedit_style)
        criteria_input_field.setFont(font)
        coeff_input_field.setStyleSheet(lineedit_style)
        coeff_input_field.setFont(font)

        criteria_input_layout = QVBoxLayout()
        criteria_input_layout.addWidget(criteria_label)
        criteria_input_layout.addWidget(criteria_input_field)

        coeff_input_layout = QVBoxLayout()
        coeff_input_layout.addWidget(coeff_label)
        coeff_input_layout.addWidget(coeff_input_field)

        value_input_layout = QHBoxLayout()
        value_input_layout.addLayout(criteria_input_layout)
        value_input_layout.addSpacing(10)
        value_input_layout.addLayout(coeff_input_layout)

        self.value_col_layout.addLayout(value_input_layout)

        self.value_fields[index] = criteria_input_field
        self.value_coeff[index] = coeff_input_field
        criteria_input_field.editingFinished.connect(self.setupMatrix)

    def addWeightInput(self):
        index = len(self.weight_fields) + 1
        criteria_label = QLabel(f'Critère {index}:', self)
        criteria_input_field = QLineEdit(self)

        coeff_label = QLabel(f'Coefficient {index}:', self)
        coeff_input_field = QLineEdit(self)

        # Apply the defined styles
        font = QFont("Trebuchet MS", 10, QFont.Bold)
        criteria_label.setFont(font)
        criteria_label.setStyleSheet("color: #FFFFFF;")
        coeff_label.setFont(font)
        coeff_label.setStyleSheet("color: #FFFFFF;")

        lineedit_style = "color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        criteria_input_field.setStyleSheet(lineedit_style)
        criteria_input_field.setFont(font)
        coeff_input_field.setStyleSheet(lineedit_style)
        coeff_input_field.setFont(font)

        criteria_input_layout = QVBoxLayout()
        criteria_input_layout.addWidget(criteria_label)
        criteria_input_layout.addWidget(criteria_input_field)

        coeff_input_layout = QVBoxLayout()
        coeff_input_layout.addWidget(coeff_label)
        coeff_input_layout.addWidget(coeff_input_field)

        weight_input_layout = QHBoxLayout()
        weight_input_layout.addLayout(criteria_input_layout)
        weight_input_layout.addSpacing(10)
        weight_input_layout.addLayout(coeff_input_layout)

        self.weight_col_layout.addLayout(weight_input_layout)

        self.weight_fields[index] = criteria_input_field
        self.weight_coeff[index] = coeff_input_field

        criteria_input_field.editingFinished.connect(self.setupMatrix)


    def applyStyles(self):
        font = QFont("Trebuchet MS", 14, QFont.Bold)
        label_color = "#FFFFFF"
        label_style = f"color: {label_color};"
        label_font = font
        self.capacityLabel.setStyleSheet(label_style)
        self.capacityLabel.setFont(label_font)


        textedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #808080; border-radius: 5px;"
        textedit_font = font
        self.capacityEdit.setStyleSheet(textedit_style)
        self.capacityEdit.setFont(textedit_font)
        self.resultTextEdit.setStyleSheet(textedit_style)
        self.resultTextEdit.setFont(textedit_font)

        button_style = f"color: #FFFFFF; background-color: #4CAF50; border: 2px solid #4CAF50; border-radius: 5px;"
        button_font = font
        self.solveButton.setStyleSheet(button_style)
        self.solveButton.setFont(button_font)
        self.addValueButton.setStyleSheet(button_style)
        self.addValueButton.setFont(button_font)
        self.addWeightButton.setStyleSheet(button_style)
        self.addWeightButton.setFont(button_font)
        self.addProductButton.setStyleSheet(button_style)
        self.addProductButton.setFont(button_font)

        table_style = """
                        QTableWidget {
                            background-color: #2E2E2E;
                            border: 2px solid #808080;
                            border-radius: 5px;
                            color: #FFFFFF;
                            font-size: 14px;
                            gridline-color: #4CAF50;
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
       for i,p in self.product_fields.items() :
           print(p.text())
       self.matrixTable.setColumnCount(len(self.product_fields))
       self.matrixTable.setRowCount(len(self.value_fields) + len(self.weight_fields))
       self.matrixTable.setHorizontalHeaderLabels(
           [p.text() for p in self.product_fields.values()]
       )
       self.matrixTable.setVerticalHeaderLabels(
           [p.text() for p in self.value_fields.values()] +
           [p.text() for p in self.weight_fields.values()]
       )
    def solveKnapsack(self):
        try:
            products = [p.text() for p in self.product_fields.values()]
            value_coefficients = [float(p.text()) for p in self.value_coeff.values()]
            weight_coefficients = [float(p.text()) for p in self.weight_coeff.values()]
            all_values = []
            all_weights = []
            capacity = float(self.capacityEdit.text())

            for i in range(len(products)):
                col = []
                for j in range(len(value_coefficients)):
                    col.append(float(self.matrixTable.item(j, i).text())*value_coefficients[j])
                all_values.append(sum(col))

            for i in range(len(products)):
                col = []
                for j in range(len(weight_coefficients)):
                    col.append(float(self.matrixTable.item(j + len(value_coefficients),i).text())*weight_coefficients[j])
                all_weights.append(sum(col))
            print("values: ")
            print(all_values)
            print("\nweights: ")
            print(all_weights)

            result_str = "Solution: \n"
            total_value, selected_items = solve_knapsack(all_values, all_weights, capacity)
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