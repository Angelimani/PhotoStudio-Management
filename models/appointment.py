from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import db

class Appointment(db.Model):
    __tablename__ = 'appointments'  # Ensure the table name is 'appointments'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)  # ForeignKey points to clients.id
    appointment_date = Column(String(50))  # Replace with your actual date field type

    # Define the relationship to Client
    client = relationship('Client', backref='appointments')

    def __init__(self, client_id, appointment_date):
        self.client_id = client_id
        self.appointment_date = appointment_date
