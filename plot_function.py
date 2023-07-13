import sys
import re
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QDoubleSpinBox, QPushButton
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plot_Function")

        # Create the main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Create the function input widget
        self.function_label = QLabel("Enter function (use x as the variable):")
        self.function_input = QLineEdit()
        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_input)

        # Create the min and max x value widgets
        self.min_x_label = QLabel("Min x value:")
        self.min_x_input = QDoubleSpinBox()
        self.max_x_label = QLabel("Max x value:")
        self.max_x_input = QDoubleSpinBox()
        self.layout.addWidget(self.min_x_label)
        self.layout.addWidget(self.min_x_input)
        self.layout.addWidget(self.max_x_label)
        self.layout.addWidget(self.max_x_input)

        # Create the plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_function)
        self.layout.addWidget(self.plot_button)

        # Create the error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")
        self.layout.addWidget(self.error_label)

        # Create the Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot_function(self):
        # Clear any previous error message
        self.error_label.setText("")

        # Get the function input and min/max x values
        function_text = self.function_input.text()
        min_x = self.min_x_input.value()
        max_x = self.max_x_input.value()

        # Validate the function input
        if not re.match(r"^[x0-9+\-*/^()\s]+$", function_text):
            self.error_label.setText("Invalid function input")
            return

        # Validate the min/max x values
        if max_x <= min_x:
            self.error_label.setText("Max x value must be greater than min x value")
            return

        # Generate x values
        x = np.linspace(min_x, max_x, 100).astype(int)

        try:
            # Evaluate the function for the given x values
            y = eval(function_text)

            # Clear the previous plot
            self.figure.clear()

            # Create a new plot
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)

            # Redraw the canvas
            self.canvas.draw()

        except Exception as e:
            self.error_label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    del app 