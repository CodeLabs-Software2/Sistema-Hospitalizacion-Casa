from sqlalchemy import Table, Column, Integer, String,DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class PacienteModel(Base):
    __tablename__ = 'paciente'  #poner cuidado cuando se ponga el nombre de las talbas
    id = Column(Integer, primary_key=True)
    familiar_id = Column(Integer, ForeignKey("familiardesignado.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
