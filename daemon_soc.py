import time
import subprocess

print("Iniciando el Servicio Jefe del SOC...")

while True:
    print("\n--- Ejecutando escaneo ---")
    # Aquí mandamos a ejecutar tu código original sin tocarlo
    subprocess.run(["python3", "soc_integrador.py"])
    
    print("--- Escaneo terminado. Durmiendo 30s ---")
    time.sleep(30)
