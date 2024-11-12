from sqlalchemy import Column, Integer, Float, TIMESTAMP
from .database import Base

class Registro(Base):
    __tablename__ = "registros_gramaje"
    id = Column(Integer, primary_key=True, index=True)
    peso = Column(Float, nullable=False)
    fecha = Column(TIMESTAMP)
