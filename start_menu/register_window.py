from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QLineEdit,QCheckBox
from .def_register import register
from message.message import message_box

class register_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Register Window')
        self.setGeometry(600,250,350,200)
        layout=QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password2=QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password2.setEchoMode(QLineEdit.Password)
        self.show_password=QCheckBox('Show password')
        self.btn_register = QPushButton("Register")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.password2)
        layout.addWidget(self.show_password)
        layout.addWidget(self.btn_register)
        self.setLayout(layout)
        self.btn_register.clicked.connect(self.register_check)
        self.show_password.stateChanged.connect(self.check_box)

    def check_box(self,state):
        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
            self.password2.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.password2.setEchoMode(QLineEdit.Password)
            
    def register_check(self):
        user_name=self.username.text()
        password=self.password.text()
        password2=self.password2.text()
        status,message=register(user_name,password,password2)
        if status == False:
            message_box(message)
        else:
            message_box(message)
            