from fastapi import APIRouter
from schema.Usuario import Usuario
from utils.db import DataBaseConnection

conn = DataBaseConnection()
historialDiagnostico = APIRouter()
cur = conn.cursor()


@historialDiagnostico.get("/all/{id}")
def listar_diagnostico(id:int):
    listaHistorialDiagnostico = []
     # Obtener los datos de la base de datos
                
    cur.execute("""SELECT hd.fecha, us.nombre, us.apellido, pm.tarjeta_profesional, pm.especialidad, pm.tipo_personal,
                          uspa.nombre, usfd.nombre, di.nombre_diagnostico, di.descripcion FROM historialDiagnostico hd
                   INNER JOIN personalMedico pm on hd.medico_Id = pm.id 
                   INNER JOIN usuario us on pm.usuario_Id = us.id
                   INNER JOIN paciente pa on hd.paciente_Id = pa.id
                   INNER JOIN usuario uspa on pa.usuario_id = uspa.id
                   INNER JOIN familiarDesignado fd on pa.familiar_Id = fd.id
                   INNER JOIN usuario usfd on fd.usuario_Id = usfd.id
                   INNER JOIN diagnostico di on hd.diagnostico_Id = di.id
                   where paciente_id='%s'; """% id)
    rows = cur.fetchall()

    # Crear un nuevo archivo Excel
    wb = openpyxl.Workbook()

    # Agregar los datos a una hoja de cálculo
    sheet = wb.active
    sheet.title = "Historial de Diagnósticos"

    # Agregar encabezados a la tabla
    sheet.append(["fecha", "usuario_nombre", "usuario_apellido", "tarjeta_profesinoal", "especialidad", "tipo_personal",
                  "usuario_paciente", "usuario_familiar", "nombre_diagnostico", "diagnostico_descripcion"])

    # Agregar filas a la tabla
    for row in rows:
        sheet.append(row)

    # Guardar el archivo Excel
    wb.save("resultados.xlsx")

    for data in rows:
        listaHistorialDiagnostico.append(data)
    return  {"message": listaHistorialDiagnostico}


def html_styler(html, styles):
    """Aplica estilos CSS a una tabla HTML"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for style in styles:
        selector = style["selector"]
        props = style["props"]
        for tag in soup.select(selector):
            for prop in props:
                tag[prop[0]] = prop[1]
    return str(soup.table)

def obtenerHistorialClinica():
    pass
    
