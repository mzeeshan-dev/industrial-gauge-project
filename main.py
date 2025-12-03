from PyQt5.QtWidgets import QApplication
from dashboard import Dashboard


def main():
    app = QApplication([])
    window = Dashboard()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
