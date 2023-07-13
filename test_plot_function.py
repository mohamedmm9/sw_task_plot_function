import sys
import pytest
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from pytestqt.qtbot import QtBot
from plot_function import MainWindow
@pytest.fixture
def app(qtbot):
    test_app = QApplication(sys.argv)
    window = MainWindow()
    qtbot.addWidget(MainWindow)
    yield test_app
    window.close()


def test_plot_function_valid_input(app, qtbot):
    window = app.activeWindow()
    qtbot.keyClicks(window.function_input, "x**2")
    window.min_x_input.setValue(-10)
    window.max_x_input.setValue(10)
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert window.error_label.text() == ""
    assert window.figure.axes[0].lines[0].get_ydata().tolist() == [100, 81, 64, 49, 36, 25, 16, 9, 4, 1, 0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


def test_plot_function_invalid_input(app, qtbot):
    window = app.activeWindow()
    qtbot.keyClicks(window.function_input, "x**2 +")
    window.min_x_input.setValue(-10)
    window.max_x_input.setValue(10)
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert window.error_label.text() == "Invalid function input"
    assert not window.figure.axes[0].lines


def test_plot_function_invalid_range(app, qtbot):
    window = app.activeWindow()
    qtbot.keyClicks(window.function_input, "x**2")
    window.min_x_input.setValue(10)
    window.max_x_input.setValue(-10)
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert window.error_label.text() == "Max x value must be greater than min x value"
    assert not window.figure.axes[0].lines
del app
