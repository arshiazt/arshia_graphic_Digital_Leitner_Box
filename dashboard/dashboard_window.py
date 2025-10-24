from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton
from .show_box_window import show_box
from .add_card_window import add_card
from .modify_card import modify
from .review_card_window import review

class dashboard(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id=user_id
        self.setWindowTitle('Dashboard')
        self.setGeometry(500,200,300,100)
        layout=QVBoxLayout()
        self.show_box_btn=QPushButton('Show Box')
        self.add_card_btn=QPushButton('Add Card')
        self.modify_card_btn=QPushButton('Modify Card')
        self.review_btn=QPushButton('Review Cards')
        layout.addWidget(self.show_box_btn)
        layout.addWidget(self.add_card_btn)
        layout.addWidget(self.modify_card_btn)
        layout.addWidget(self.review_btn)
        self.setLayout(layout)
        self.show_box_btn.clicked.connect(self.show_box)
        self.add_card_btn.clicked.connect(self.add_card)
        self.modify_card_btn.clicked.connect(self.modify_card)
        self.review_btn.clicked.connect(self.review)

    def show_box(self):
        self.list_show_box=show_box(self.user_id)
        self.list_show_box.show()

    def add_card(self):
        self.add=add_card(self.user_id)
        self.add.show()

    def modify_card(self):
        self.modify=modify(self.user_id)
        self.modify.show()

    def review(self):
        self.review_card=review(self.user_id)
        self.review_card.show()  