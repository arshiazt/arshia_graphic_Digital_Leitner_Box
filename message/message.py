from  PyQt5.QtWidgets import QMessageBox

def message_box(message):
    msg=QMessageBox()
    msg.setWindowTitle('Message Box')
    msg.setGeometry(600,250,150,100)
    msg.setText(message)
    msg.exec_()
