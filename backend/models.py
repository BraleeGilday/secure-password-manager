from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)

from sqlalchemy.orm import DeclarativeBase, relationship

# UUID import (added to both User and Credential classes for generating unique string IDs)
import uuid


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    User table in database
    """

    __tablename__ = "user"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # date created? modified?
    # log in attempts?
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
    # maybe set enc_key to True for beginning?
    # encryption_key = Column(
    #     String,
    #     nullable=False
    #     )
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", backref="credential")
