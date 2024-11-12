import serial

try:
    s = serial.Serial(
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
            res = s.readline().strip()
            if res:
                peso = res.decode('ascii').strip()
                print(f"Peso leído: {peso}")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

except serial.SerialException as e:
    print(f"Error de conexión: {e}")

finally:
    if s.is_open:
        s.close()
        print("Conexión cerrada.")
