from data_base.db import get_connection
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QComboBox
from message.message import message_box

def def_show_box(user_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT s.id,s.name,s.review_interval,COUNT(c.id) AS card_count" \
    " FROM slots s LEFT JOIN cards c ON s.id=c.slot_id" \
    " AND c.user_id=%s GROUP BY s.id,s.name ORDER BY s.id",(user_id,))
    rows=cur.fetchall()
    result=[]
    for i in rows:
        if i[0] == 1:
            result.append(f'* ({i[1]} : cards in it must be reviewed everyday) | Number of Cards : {i[3]}')
        elif i[0] != 6:
            result.append(f'* ({i[1]} : cards in it must be reviewed every {i[2]} days) | Number of Cards : {i[3]}')
        else:
            result.append(f'* ({i[1]} : Learned cards!) | Number of Cards: {i[3]}')
    conn.close()
    return result

def def_slot_show(user_id,slot_id): 
    conn=get_connection()
    cur=conn.cursor() 
    cur.execute("SELECT id,question,answer,next_review " \
    " FROM cards WHERE user_id=%s AND slot_id=%s ORDER BY id",(user_id,slot_id))
    cards=cur.fetchall()
    conn.close()
    if not cards:
        return False,'There is no card.'
    return True,cards

class show_box(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id=user_id
        self.setWindowTitle('Show Box')
        self.setGeometry(600,250,300,200)
        layout=QVBoxLayout()
        self.result=def_show_box(self.user_id)
        self.slot1=QLabel(self.result[0])
        self.slot2=QLabel(self.result[1])
        self.slot3=QLabel(self.result[2])
        self.slot4=QLabel(self.result[3])
        self.slot5=QLabel(self.result[4])
        self.slot6=QLabel(self.result[5])
        self.slot_id=QComboBox()
        self.slot_id.addItems(['Slot 1','Slot 2','Slot 3','Slot 4','Slot 5','Slot 6'])
        self.submit_btn=QPushButton('Submit')
        layout.addWidget(self.slot1)
        layout.addWidget(self.slot2)
        layout.addWidget(self.slot3)
        layout.addWidget(self.slot4)
        layout.addWidget(self.slot5)
        layout.addWidget(self.slot6)
        layout.addWidget(QLabel('Slot id : '))
        layout.addWidget(self.slot_id)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)
        self.submit_btn.clicked.connect(self.submit)
        
    def submit(self):
        value=self.slot_id.currentText()[-1]
        status,cards=def_slot_show(self.user_id,value)
        if status == False:
            message_box(cards)
        else:
            message=''
            if value == '6':
                for i in cards:
                    message=message+f'ID : {i[0]} | Question : {i[1]} | Answer : {i[2]}\n'
            else:
                for i in cards:
                    message=message+f'ID : {i[0]} | Question : {i[1]} | Answer : {i[2]} | Next review : {i[3]}\n'
            message_box(message)