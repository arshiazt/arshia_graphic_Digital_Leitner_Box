from data_base.db import create_database,create_tables
from PyQt5.QtWidgets import QApplication
from welcome.welcome_window import welcome_window
import sys

def main():
    app=QApplication(sys.argv)
    window=welcome_window()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    create_database()
    create_tables()
    main()
