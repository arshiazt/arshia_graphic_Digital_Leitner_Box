from data_base.db import get_connection
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QLineEdit,QMessageBox,QComboBox
from PyQt5.QtGui import QIntValidator
from message.message import message_box

def modify_card(user_id,slot_id,card_id):
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,question,answer FROM cards WHERE user_id=%s AND slot_id=%s AND id=%s ORDER BY id"
    cur.execute(query,(user_id,slot_id,card_id))
    list_card=cur.fetchone()
    if not list_card:
        return False,'There is no such card in this slot.'
    return True,list_card

def delete_card(user_id,card_id):
    conn=get_connection()
    cur=conn.cursor()
    query="DELETE FROM cards WHERE id=%s AND user_id=%s"
    cur.execute(query,(card_id,user_id))
    conn.commit()
    conn.close()
    return f'Card id : {card_id} ===> Delete.'

def edit_card(user_id,card_id,new_q,old_q,new_a,old_a):
    conn=get_connection()
    cur=conn.cursor()
    question,answer=new_q.strip(),new_a.strip()
    if question == '':
        question = old_q
    if answer == '':
        answer=old_a
    query="UPDATE cards SET question=%s,answer=%s WHERE id=%s AND user_id=%s"
    cur.execute(query,(question,answer,card_id,user_id))
    conn.commit()
    conn.close()
    return f'Card id : {card_id} ===> Changed.'

class second_modify(QWidget):
    def __init__(self,user_id,slot_id,card_id,message):
        super().__init__()
        self.setWindowTitle('Edit Or Delete')
        self.setGeometry(600,250,300,150)
        layout=QVBoxLayout()
        self.user_id=user_id
        self.slot_id=slot_id
        self.card_id=card_id
        self.message=message
        self.question=QLineEdit()
        self.answer=QLineEdit()
        self.delete_btn=QPushButton('Delete')
        self.edit_btn=QPushButton('Edit')
        layout.addWidget(QLabel('The delete button removes the card from the box.'))
        layout.addWidget(QLabel('Leave blank if you do not want to change.'))
        layout.addWidget(QLabel(f'Old question : {self.message[1]} | Old answer : {self.message[2]}'))
        layout.addWidget(QLabel('New question : '))
        layout.addWidget(self.question)
        layout.addWidget(QLabel('New answer : '))
        layout.addWidget(self.answer)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.edit_btn)
        self.setLayout(layout)
        self.delete_btn.clicked.connect(self.delete)
        self.edit_btn.clicked.connect(self.edit)

    def delete(self):
        result=delete_card(self.user_id,self.card_id.text())
        message_box(result)

    def edit(self):
        new_q=self.question.text()
        new_a=self.answer.text()
        result=edit_card(self.user_id,self.card_id.text(),new_q,self.message[1],new_a,self.message[2])
        message_box(result)

class modify(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id=user_id
        self.setWindowTitle('Modify Card')
        self.setGeometry(600,250,300,150)
        layout=QVBoxLayout()
        self.slot_id=QComboBox()
        self.slot_id.addItems(['Slot 1','Slot 2','Slot 3','Slot 4','Slot 5'])
        self.card_id=QLineEdit()
        self.card_id.setValidator(QIntValidator())
        self.submit_btn=QPushButton('Submit')
        layout.addWidget(QLabel('Slot Id : '))        
        layout.addWidget(self.slot_id)
        layout.addWidget(QLabel('Card Id : '))
        layout.addWidget(self.card_id)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)
        self.submit_btn.clicked.connect(self.submit)
        
    def submit(self):
        slot=self.slot_id.currentText()[-1]
        card=self.card_id.text()
        if not card.isdigit():
            message_box('Please fill in all fields.')
            return
        status,message=modify_card(self.user_id,slot,card)
        if status == False:
            message_box(message)
        else:
            self.second_modi=second_modify(self.user_id,self.slot_id,self.card_id,message)
            self.second_modi.show()