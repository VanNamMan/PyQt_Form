import sys
from helloworld import HelloWorld
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = HelloWorld()
    w.show()
    # sys.exit(a.exec_())

    try:
        sys.exit(a.exec_())
    except SystemExit:
        pass
    except:
        pass