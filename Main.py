import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import subprocess

def exit_program():
    app.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('sus.png'))
        self.setWindowTitle("PL et PLNE avec Gurobi")

        # Set window size and position
        window_width = 1000
        window_height = 800
        screen_geometry = app.primaryScreen().geometry()
        x_coordinate = int((screen_geometry.width() / 2) - (window_width / 2))
        y_coordinate = int((screen_geometry.height() / 2) - (window_height / 2))
        self.setGeometry(x_coordinate, y_coordinate, window_width, window_height)

        # Apply background image to window using stylesheet
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("bg.jpg").scaledToWidth(self.width()).scaledToHeight(self.height())  # Scale pixmap to window width
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        # Project Name in the middle at the top
        self.project_name = QLabel("PL et PLNE avec Gurobi", self)
        self.project_name.setStyleSheet("color: #FFD700; font-family: Trebuchet MS; font-size: 36px;")  # Gold color, Impact font
        self.project_name.setAlignment(Qt.AlignCenter)

        # Description of the project
        self.project_description = QLabel("Choisir un type de problème", self)
        self.project_description.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")  # White color, Arial font
        self.project_description.setAlignment(Qt.AlignCenter)

        # Layout to contain exercise buttons
        self.exercise_layout = QHBoxLayout()
        self.exercise_frame = QWidget(self)
        self.exercise_frame.setLayout(self.exercise_layout)

        # Example buttons for exercises
        Exercise_names = [
            "Optimisation de l'approvisionnement en électricité",
            "Problème de sac à dos",
        ]
        for exercise_name in Exercise_names:
            exercise_button = QPushButton(exercise_name, self)
            exercise_button.setFont(QFont("Trebuchet MS", 14, QFont.Bold))
            exercise_button.setStyleSheet("background-color: #4CAF50; color: white; border: 2px solid #007BFF; border-radius: 10px;")
            exercise_button.setFixedHeight(50)
            exercise_button.setFixedWidth(600)

            exercise_button.clicked.connect(lambda checked, btn=exercise_button: self.select_exercise(btn))
            self.exercise_layout.addWidget(exercise_button)

        # Exit Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(QFont("Trebuchet MS", 16, QFont.Bold))
        self.exit_button.setStyleSheet("background-color: #DC3545; color: white; border: 2px solid #DC3545; border-radius: 10px;")
        self.exit_button.clicked.connect(exit_program)
        self.exit_button.setFixedHeight(50)

        # Collaborators listed under each other
        self.collaborators = QLabel("Présenté par:\nAhmed Karray\nAmine Affi\nElyes Belgouthi\nOmar Maalej", self)
        self.collaborators.setStyleSheet("color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")
        self.collaborators.setAlignment(Qt.AlignCenter)  # Center-align the collaborators

        # Arrange widgets
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_description)
        layout.addWidget(self.exercise_frame)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.collaborators)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins around the layout
        layout.setSpacing(20)  # Add spacing between widgets
        self.setCentralWidget(central_widget)

    def select_exercise(self, exercise_button):
        case = exercise_button.text()
        if case == "Optimisation de l'approvisionnement en électricité":
            command = [sys.executable, "./ElectricitySupplyApp.py"]
            subprocess.run(command)
        elif case == "Problème de sac à dos":
            command = [sys.executable, "./Knapsack.py"]
            subprocess.run(command)
        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
