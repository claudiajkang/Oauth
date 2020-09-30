from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )

    user = relationship('User')
