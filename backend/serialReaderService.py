from fastapi import HTTPException
import serial
import os
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import String, func, cast, Date, Float
from database.models import Registro
from sqlalchemy.orm import Session
from typing import List

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = int(os.getenv("BAUD_RATE"))


def leer_peso_automatico(db: Session):
    s = None
    try:
        s = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        # s.write(b"P")
        print("Conectado a la báscula...")

        while True:
            try:
                res = s.readline().strip()
                if res:
                    peso = res.decode('ascii').strip()
                    peso_float = float(peso)
                    print(f"Peso leído: {peso_float}")
                    nuevo_registro = Registro(
                        peso=peso_float,
                        fecha=datetime.now()
                    )
                    db.add(nuevo_registro)
                    db.commit()
                    print("Registro guardado en la base de datos.")
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break
    except serial.SerialException as e:
        print(f"Error de conexión: {e}")
    finally:
        if s and s.is_open:
            s.close()
            print("Conexión cerrada.")

def obtener_total_registros_fecha(fecha: str, db: Session):
    try:
        # Convertimos la fecha ingresada en un objeto datetime
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        print("fecha_dt", fecha_dt)
        print("fecha", fecha)

        # Filtramos registros solo por la fecha usando cast para asegurar comparación
        registros_query = (
            db.query(Registro)
            .filter(func.to_char(Registro.fecha, 'YYYY-MM-DD').like(f'%{fecha_dt}%'))
        )
        
        # Obtenemos los registros y el peso total en una sola consulta
        registros = registros_query.all()
        peso_total = db.query(func.sum(Registro.peso)).filter(func.to_char(Registro.fecha, 'YYYY-MM-DD').like(f'%{fecha_dt}%')).scalar()

        print("Registros", registros)
        # Verificamos si hay registros para la fecha especificada
        if not registros:
            raise HTTPException(status_code=404, detail="No se encontraron registros para la fecha especificada")

        # Construimos la lista de registros con el peso y la fecha formateada
        listado_registros = [
            {"peso": f"{registro.peso} gr", "fecha": registro.fecha}
            for registro in registros
        ]

        return {
            "registros": listado_registros,
            "peso_total": f"{peso_total} gr" if peso_total is not None else 0
        }

    except ValueError as ve:
        print(f"Error de formato de fecha: {ve}")
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use 'YYYY-MM-DD'")
    except Exception as e:
        print(f"Error durante la consulta: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")