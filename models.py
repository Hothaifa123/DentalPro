from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(String(20))
    address = Column(Text)
    allergies = Column(Text)
    chronic = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class Drug(Base):
    __tablename__ = 'drugs'
    id = Column(Integer, primary_key=True)
    trade_name = Column(String(300))
    category = Column(String(100))
    admin_route = Column(String(50))
    dosage = Column(String(200))
    frequency = Column(String(200))
    duration = Column(String(200))
    scientific_name = Column(String(300))

class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    diagnosis = Column(Text)
    notes = Column(Text)
    items_json = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    patient = relationship('Patient')
