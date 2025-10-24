from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel
from start_menu import login_window,register_window

class welcome_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Leitner Box')
        self.setGeometry(500,200,300,100)
        layout=QVBoxLayout()
        self.title_label=QLabel('Welcome to digital leitner box!')
        self.login_btn=QPushButton('Login')
        self.register_btn=QPushButton('Register')
        layout.addWidget(self.title_label)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)
        self.login_btn.clicked.connect(self.open_login)
        self.register_btn.clicked.connect(self.open_register)

    def open_login(self):
        self.login=login_window.login_window()
        self.login.show()

    def open_register(self):
        self.register=register_window.register_window()
        self.register.show()