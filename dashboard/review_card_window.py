from data_base.db import get_connection
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QLabel,QMessageBox,QComboBox
from message.message import message_box
import random
import datetime

def update_time_card(user_id):
    today=datetime.date.today()
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,slot_id,next_review  FROM cards WHERE user_id=%s AND slot_id<6 AND next_review<%s - INTERVAL '2 days'"
    cur.execute(query,(user_id,today))
    result=cur.fetchall()
    if not result:
        return
    time={1:0,2:3,3:7,4:14,5:30}
    for i in result:
        card_id,slot_id,next_review=i
        if slot_id>1:
            new_slot_id=slot_id-1
        else:
            new_slot_id=slot_id
        next_review=today+datetime.timedelta(time[new_slot_id])
        cur.execute("UPDATE cards SET slot_id=%s,next_review=%s WHERE id=%s",(new_slot_id,next_review,card_id))
    conn.commit()
    conn.close()

def review_show(user_id,slot_id):
    update_time_card(user_id)
    today=datetime.date.today()
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,question,answer,slot_id FROM cards WHERE user_id=%s AND slot_id=%s AND next_review<=%s"
    cur.execute(query,(user_id,slot_id,today))
    cards=cur.fetchall()
    if not cards:
        return False,'No cards to review today.'
    random.shuffle(cards)
    return True,cards

def update_review(card_id,slot_id,next_review):
    today=datetime.date.today()
    conn=get_connection()
    cur=conn.cursor()
    next_review=today+datetime.timedelta(next_review)
    query="UPDATE cards SET slot_id=%s,last_review=%s,next_review=%s WHERE id=%s"
    if next_review == today:
        cur.execute(query,(slot_id,today,None,card_id))
    else:
        cur.execute(query,(slot_id,today,next_review,card_id))
    conn.commit()
    conn.close()
    
class review(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id=user_id
        self.setWindowTitle('Review Card')
        self.setGeometry(600,250,300,100)
        layout=QVBoxLayout()
        self.slot_id=QComboBox()
        self.slot_id.addItems(['Slot 1','Slot 2','Slot 3','Slot 4','Slot 5'])
        self.review_btn=QPushButton('Review Card')
        layout.addWidget(QLabel('Slot Id : '))
        layout.addWidget(self.slot_id)
        layout.addWidget(self.review_btn)
        self.setLayout(layout)
        self.review_btn.clicked.connect(self.review_from_box)
    
    def review_from_box(self):
        status,message=review_show(self.user_id,self.slot_id.currentText()[-1])
        if status == False:
           message_box(message)
        else:
            for card in message:
                ans = QMessageBox.question(self, 'Question Box',f"Question: {card[1]}\nAnswer: {card[2]}\n\nDid you learn it?", QMessageBox.Yes | QMessageBox.No)
                new_slot=card[3]
                if ans == QMessageBox.Yes :
                    new_slot+=1
                day=[1, 3, 7, 14, 30, 0]
                next_days =day[new_slot - 1]
                update_review(card[0],new_slot,next_days)