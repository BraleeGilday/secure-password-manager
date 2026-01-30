from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, relationship
import uuid  # UUID import (added to Credential class for generating unique string IDs on creation of a credential)


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    User table in database
    """

    __tablename__ = "user"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    login_attempts = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # admin ?


class Credential(Base):
    """
    Credential Table in database
    """

    __tablename__ = "credential"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", backref="credential")
