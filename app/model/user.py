from app import db
from sqlalchemy import Column, String, Integer


class User(db.Model):
    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String(40),
        unique=True
    )

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        return password == 'valid'
