from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func

from sqlalchemy.orm import DeclarativeBase, relationship


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
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    site = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    # maybe set enc_key to True for beginning?
    # encryption_key = Column(
    #     String,
    #     nullable=False
    #     )
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", backref="credential")
