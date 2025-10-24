from data_base.db import get_connection
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QLineEdit
from message.message import message_box
import datetime

def def_add_card(user_id,question,answer):
    conn=get_connection()
    cur=conn.cursor()
    today=datetime.date.today()
    next_review=today
    query="INSERT INTO cards (user_id,question,answer,slot_id,last_review,next_review) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(query,(user_id,question,answer,1,today,next_review))
    conn.commit()
    conn.close()
    return 'Your card has been added to slot one.'

class add_card(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id=user_id
        self.setWindowTitle('Add card')
        self.setGeometry(600,250,300,150)
        layout=QVBoxLayout()
        self.question_input=QLineEdit()
        self.answer_input=QLineEdit()
        self.add_btn=QPushButton('Add card')
        layout.addWidget(QLabel('Question : '))
        layout.addWidget(self.question_input)
        layout.addWidget(QLabel('Answer : '))
        layout.addWidget(self.answer_input)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)
        self.add_btn.clicked.connect(self.add_card_to_box)

    def add_card_to_box(self):
        question=self.question_input.text().strip()
        answer=self.answer_input.text().strip()
        if question == '' or answer == '':
            message_box('Please fill in all fields.')
            return
        add=def_add_card(self.user_id,question,answer)
        message_box(add)
