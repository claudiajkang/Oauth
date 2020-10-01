import time
from app import db
from sqlalchemy.orm import relationship
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin
)
from sqlalchemy import Column, Integer, ForeignKey


class OAuth2ClientModel(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )

    user = relationship('UserModel')


class OAuth2AuthorizationCodeModel(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )

    user = relationship('UserModel')


class OAuth2TokenModel(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE')
    )

    user = relationship('UserModel')

    def is_refresh_token_active(self):
        if self.revoked:
            return False

        expires_at = self.issued_at + self.expires_in * 2

        return expires_at >= time.time()
