from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)

from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(DeclarativeBase):
    """
    User table in database
    """

    __tablename__ = "user"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Account(DeclarativeBase):
    """
    Account Table in database
    """

    __tablename__ = "account"
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    site = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    # maybe set enc_key to True for beginning?
    encryption_key = Column(
        String,
        nullable=False
        )
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", backref="account")