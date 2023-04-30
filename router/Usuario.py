import sys
sys.path.append("..")
import psycopg2

from fastapi import APIRouter, HTTPException
from schema.Usuario import Usuario
from utils.db import DataBaseConnection, run_query

#--------
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn = DataBaseConnection()


user = APIRouter()


@user.get("/all/")
def listar_allUsers():
    """
    cur = run_query("SELECT * FROM Usuario")
    for data in cur:
        print(data)   """
    engine = create_engine('postgresql://postgres:1234@localhost:5432/HospitalizacionenCasa')
    Session = sessionmaker(bind=engine)
    session = Session()
    print(session)

    Base = declarative_base()

    class Usuario(Base):
        __tablename__ = 'usuario'
        id = Column(Integer, primary_key=True)
        nombre = Column(String)
        apellido = Column(String)
        cedula = Column(Integer)
        edad = Column(Integer)
        telefono = Column(String)
        email = Column(String)
        password = Column(String)
        direccion = Column(String)

    usuarios = session.query(Usuario).all()

    for usuario in usuarios:
        print(usuario.nombre, usuario.apellido,usuario.email, usuario.telefono)


@user.post("/usuarios/{id}")
def actualizar_usuario(id: int, Usuario_Actualizar: Usuario):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Usuario SET nombre=%(nombre)s, apellido=%(apellido)s, cedula=%(cedula)s, edad=%(edad)s, telefono=%(telefono)s, email=%(email)s, direccion=%(direccion)s WHERE id = %(id)s", {"id":Usuario_Actualizar.id,"nombre":Usuario_Actualizar.nombre, "apellido":Usuario_Actualizar.apellido, "cedula":Usuario_Actualizar.cedula, "edad": Usuario_Actualizar.edad, "telefono": Usuario_Actualizar.telefono, "email":Usuario_Actualizar.email, "direccion":Usuario_Actualizar.direccion})
        conn.commit()
        conn.close()
        return {"id":id, **Usuario_Actualizar.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





