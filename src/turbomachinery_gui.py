import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TurboGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turbomachinery Comparison")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon("icon.png"))  # You can place an icon file in the same directory

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Pages
        self.home_tab = QWidget()
        self.parameters_tab = QWidget()
        self.results_tab = QWidget()

        # Add pages to tab widget
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.parameters_tab, "Input Parameters")
        self.tabs.addTab(self.results_tab, "Performance Results")

        self.home_ui()
        self.parameters_ui()
        self.results_ui()

    def home_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to the Turbomachinery Comparison Tool Select a Tab to Begin")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.home_tab.setLayout(layout)

    def parameters_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Enter Fluid and Geometry Parameters")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter machine type, e.g. Compressor, Axial")
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_parameters)
        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_button)
        self.parameters_tab.setLayout(layout)

    def results_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Results will be displayed here after parameters are submitted.")
        layout.addWidget(label)

        # Placeholder for performance results plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.results_tab.setLayout(layout)

    def submit_parameters(self):
        machine_type = self.input_field.text()

        # Example plot after parameters are inputted (for illustration)
        self.ax.clear()
        self.ax.plot([1, 2, 3, 4], [1, 4, 9, 16], label="Example Data")
        self.ax.set_title(f"Performance Results for {machine_type}")
        self.ax.set_xlabel('Pressure Ratio')
        self.ax.set_ylabel('Mass Flow')
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TurboGUI()
    mainWin.show()
    sys.exit(app.exec_())
