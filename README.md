# 🛡️ Linux Mini-SOC: Analizador de Logs y Defensa Automatizada

Este proyecto es un motor de defensa automatizado (Security Operations Center) diseñado para servidores Ubuntu. Monitorea registros del sistema en tiempo real, detecta patrones de ataques de fuerza bruta mediante Expresiones Regulares (Regex) y aísla a los atacantes interactuando directamente con el firewall UFW.

## 🚀 Características Principales
* **Análisis Forense con Regex:** Filtra cientos de líneas de logs para extraer únicamente los intentos fallidos de autenticación (SSH).
* **Defensa Activa (IPS):** Si una dirección IP supera el umbral de intentos fallidos, el script se comunica con el sistema operativo para crear una regla de bloqueo total en UFW.
* **Tolerancia a Fallos:** Manejo de excepciones en Python para evitar que el script colapse ante logs corruptos o vacíos.
* **Automatización Invisible:** Operación autónoma en segundo plano como un demonio de sistema utilizando `Cron` (ejecución cada 5 minutos).
* **Hardening de SSH:** El servidor de despliegue cuenta con bloqueo de usuario root, autenticación exclusiva por llaves criptográficas (Ed25519) y ofuscación de puerto.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Sistema Operativo:** Ubuntu 26.04 LTS
* **Seguridad:** UFW (Uncomplicated Firewall), OpenSSH
* **Automatización:** Crontab (Linux Daemon)

## 📋 Arquitectura del Flujo
1. `Cron` despierta el script silenciosamente.
2. Python lee y procesa `/var/log/auth.log`.
3. El motor de Expresiones Regulares identifica patrones anómalos.
4. Se extrae la IP hostil.
5. Se invoca al sistema (`subprocess`) para inyectar la regla en UFW.

---
*Proyecto desarrollado por Lucas como laboratorio práctico de Ciberseguridad y Administración de Sistemas Linux.*
