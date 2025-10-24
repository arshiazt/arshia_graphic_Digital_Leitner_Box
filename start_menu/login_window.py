from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QLineEdit,QCheckBox
from PyQt5.QtGui import QIntValidator
import random
from .def_login import login
from message.message import message_box
from dashboard.dashboard_window import dashboard

class login_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Window')
        self.setGeometry(600,250,300,200)
        layout=QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.number=QLineEdit()
        self.random_number=random.randint(10000,99999)
        self.num=QLabel(str(f'CAPTCHA : {self.random_number}'))
        self.number.setValidator(QIntValidator())
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton("Login")
        self.show_password=QCheckBox('Show password')
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(self.show_password)
        layout.addWidget(self.num)
        layout.addWidget(self.number)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)
        self.btn_login.clicked.connect(self.login_check)
        self.show_password.stateChanged.connect(self.check_box)

    def check_box(self,state):
        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def login_check(self):
        user_name=self.username.text()
        password=self.password.text()
        user_number=self.number.text()
        status,user_id,message=login(user_name,password,self.random_number,user_number)
        if status == False:
            message_box(message)
        else:
            message_box(message)
            self.dash=dashboard(user_id)
            self.dash.show()