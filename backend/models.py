from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship
import uuid


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
    # Disallow credentials with duplicate usernames if for the exact same site (different sites can use duplicate usernames)
    __table_args__ = (
        UniqueConstraint("user_id", "site", "username", name="uq_credential_user_site_username"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="credential")
