from PyQt5.QtWidgets import QApplication,QMainWindow
from myForm import myForm

if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    w = myForm()
    w.show()
    try:
        sys.exit(a.exec())
    except :
        pass