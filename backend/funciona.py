import serial
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

backend_router = APIRouter()

@backend_router.get("/peso")
def leer_peso_funcional():
    sexample = None

    try:
        sexample = serial.Serial(
            port="COM5",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        print("Conectado a la báscula...")
        
        while True:
            try:
                res = sexample.readline().strip()
                if res:
                    peso = res.decode('ascii').strip()
                    fecha = datetime.now()
                    print(f"Peso leído: {peso}")
                    return {"peso": peso, "fecha": datetime.now()}
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break

    except serial.SerialException as e:
        print(f"Error de conexión: {e}")

    # finally:
    #     if sexample and sexample.is_open:
    #         # sexample.close()
    #         print("Conexión cerrada.")

# leer_peso_funcional()