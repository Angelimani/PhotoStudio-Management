# models/client.py
from sqlalchemy import Column, Integer, String

def init_db():
    from models.app import db  # Import here to avoid circular import
    class Client(db.Model):
        __tablename__ = 'clients'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        email = Column(String(100), nullable=False)
        phone = Column(String(20), nullable=False)
    
    return Client
