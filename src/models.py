from sqlalchemy import Column, Integer, String, Date, Text
from .db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    extra_data = Column(Text, nullable=True)

    