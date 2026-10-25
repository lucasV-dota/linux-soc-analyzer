
from datetime import datetime, timedelta
import subprocess
import re

LISTA_BLANCA = ["127.0.0.1", "192.168.1.1", "10.0.0.5"]

PUERTOS_SERVICIOS = {
    22: "SSH (Acceso Remoto) - CRITICO",
    80: "HTTP (Web no segura)",
    443: "HTTPS (Web segura)",
    3389: "RDP (Escritorio remoto de Windows) - CRITICO",
    7777: "Trafico L2 / Posible Troyano",
    27015: "Trafico CS2 / Escaneo UDP"
}

fecha_actual = datetime.now().strftime("%Y-%m-%d")

ARCHIVOS_LOGS = "server_logs.txt"
ARCHIVO_REPORTE = f"reporte_amenazas_{fecha_actual}.txt"
ARCHIVO_ERRORES = "errores_script.txt"

def obtener_timestamp():
	"""Devuelve la fecha y hora actual para el reporte"""
	return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
def extraer_ip(texto):
	"""Extrae de forma segura una IPv4 usando Expresiones Regulares."""
	patron_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
	resultado = re.search(patron_ip, texto)
	if resultado:
		return resultado.group()
	else:
		raise ValueError("No se encontro ninguna IP en la linea.")

def traducir_puerto(puerto_raw):
	"""Limpia la etiqueta del puerto y lo convierte a numero entero."""
	limpio = puerto_raw.replace("Puerto:", "").replace("puerto:", "").strip()
	puerto_num = int(limpio)
	return PUERTOS_SERVICIOS.get(puerto_num, f"Servicio desconocido ({puerto_num})")

def evaluar_reciente(texto_fecha):
	"""Convierte texto de fecha y verifica si ocurrio en los ultimos 15 min."""
	fecha_log = datetime.strptime(texto_fecha, "%Y-%m-%d %H:%M:%S")
	diferencia= datetime.now() - fecha_log
	es_reciente = diferencia <= timedelta(minutes=15)
	minutos_transcurridos = int(diferencia.total_seconds() / 60)
	return es_reciente, minutos_transcurridos

def bloquear_en_ufw(ip):
	"""Ejecuta la regla de bloqueo en UFW previa validacion de la Lista Blanca."""
	if ip in LISTA_BLANCA:
		print(f"[PROTEGIDO] IP {ip} en Lista Blanca. Omitiendo Bloqueo.")
	return "OMITIDO_LISTA_BLANCA"


	comando = ["sudo", "ufw", "deny", "from", ip]
	try:
		resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
		print(f"[BLOQUEADO] IP {ip} aislada en UFW.")
		return f"EXITO: {resultado.stdout.strip()}"
	except subprocess.CalledProcessError as err:
		print(f"[ERROR UFW] No se pudo aplicar la regla a {ip}.")
		return f"FALLO:UFW: {err.stderr.strip()}"

open(ARCHIVO_REPORTE, "a").close()
open(ARCHIVO_ERRORES, "a").close()

print("====================================")
print(" ANALIZADOR SOC INTEGRADO CON REGEX ")
print("====================================")

try:
	with open(ARCHIVOS_LOGS, "r") as f_in, \
	open(ARCHIVO_REPORTE, "a") as f_rep, \
	open(ARCHIVO_ERRORES, "a") as f_err:
		f_rep.write(f"\n--- SESION DE DEFENSA ACTIVA {obtener_timestamp()} ---\n")
		for num_linea, linea_cruda in enumerate(f_in, 1):
			linea = linea_cruda.strip()
			if "[ALERTA]" in linea:
				try:
					texto_fecha = linea[1:20]
					es_reciente, minutos_transcurridos = evaluar_reciente(texto_fecha) 
					pedazos = linea.split(" - ")
					tipo_ataque = pedazos[1].strip( )
					ip_atacante = extraer_ip(linea)
					servicio_atacado = traducir_puerto(pedazos[3])

					if es_reciente:
                            			estado_firewall = bloquear_en_ufw(ip_atacante)
                            			nota_tiempo = f"RECIENTE ({minutos_transcurridos} min)"
					else:
                            			print(f"[OMITIDO] Ataque de {ip_atacante} ocurrio hace {minutos_transcurridos} min (> 15 min).")
                            			estado_firewall = "OMITIDO_ATAQUE_ANTIGUO"
                            			nota_tiempo = f"ANTIGUO ({minutos_transcurridos} min)"

					f_rep.write(
                                        	f"{obtener_timestamp()} Linea {num_linea} | ATACANTE: {ip_atacante} | "
                                        	f"TIPO: {tipo_ataque} | TIEMPO: {nota_tiempo} | "
                                        	f"ESTADO: {estado_firewall}\n"
					)
				except (IndexError, ValueError) as err_datos:
                                        mensaje_error = (
						f"{obtener_timestamp()} Linea {num_linea} corrupta -> '{linea}' | "
						f"Causa: {type(err_datos).__name__}\n"
					)
                                        f_err.write(mensaje_error)
                                        print(f"[LOG CORRUPTO] Registrado en [ARCHIVO_ERRORES] (Linea {num_linea})")
except FileNotFoundError:
    print(f"[FALLO CRITICO] No se encontro el archivo de logs '{ARCHIVO_LOGS}'.")

print("====================================")
print(" Procesamiento Finalizado       ")
print(f"REPORTE GENERADO: '{ARCHIVO_REPORTE}'")
print(f"Registro de fallas: '{ARCHIVO_ERRORES}'")
print("====================================")
