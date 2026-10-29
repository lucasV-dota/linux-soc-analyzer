# 🛡️ Linux SOC Analyzer & Active Defense System

Un analizador de logs SOC (Security Operations Center) y motor de defensa activa automatizado de nivel industrial, escrito en Python y empaquetado en contenedores Docker. 

Este sistema monitorea en tiempo real los registros de autenticación del sistema (`/var/log/auth.log`), detecta e identifica intentos de ataques por fuerza bruta mediante expresiones regulares (Regex), aplica bloqueos automáticos en el cortafuegos de Linux (UFW) y despacha alertas en tiempo real a Telegram con persistencia anti-spam.

---

## 📐 Arquitectura del Sistema

El proyecto implementa el patrón de diseño **Wrapper/Daemon** para garantizar disponibilidad 24/7 y ejecución resiliente sin interrupción del servicio:

```text
 [/var/log/auth.log] 
          │
          ▼ (Lectura sólo lectura :ro)
  ┌───────────────┐
  │  Docker Cont. │ ───► daemon_soc.py (Bucle Daemon 24/7)
  └───────────────┘           │
                              ▼ (Ejecuta cada 30s)
                     soc_integrador.py (Motor Regex)
                              │
                              ├─► Evalúa estado / Anti-Spam (memoria_ips.txt)
                              ├─► Aplica Bloqueo Firewall (UFW via NET_ADMIN)
                              └─► Despacha Alerta (Telegram Bot API via .env)


✨ Características Principales


Análisis de Logs mediante Regex: Extracción precisa de direcciones IPv4, puertos, servicios atacados y fechas relativas desde eventos del sistema.

Defensa Activa Automatizada: Bloqueo de direcciones IP atacantes directamente en el firewall ufw del host con privilegios mínimos (NET_ADMIN).

Patrón Wrapper Daemon: Bucle de control independiente en Python (daemon_soc.py) que ejecuta escaneos periódicos garantizando tolerancia a fallos.

Persistencia y Anti-Spam: Sistema de memoria de estado local (memoria_ips.txt) que evita re-procesar alertas sobre incidentes ya mitigados.

Notificaciones en Tiempo Real: Integración con la API de Bots de Telegram para enviar reportes formateados de eventos críticos de seguridad.

DevOps & Security First: Manejo estricto de secretos mediante variables de entorno (.env), archivos excluidos en .gitignore y ejecución aislada mediante Docker.



🛠️ Tecnologías Utilizadas


Lenguaje: Python 3.10+ (re, os, urllib, subprocess, datetime)

Contenedores: Docker (Dockerfile, aislamientos de red y capacidades de kernel)

Seguridad & Red: Linux UFW (Uncomplicated Firewall), Regex Log Analysis, Telegram API

Control de Versiones: Git / GitHub



📂 Estructura del Proyecto

.
├── Dockerfile              # Configuración de empaquetado de la imagen Docker
├── daemon_soc.py          # Wrapper Daemon de ejecución continua 24/7
├── soc_integrador.py      # Motor principal de parsing, bloqueo y alertas
├── .env.example           # Plantilla genérica para variables de entorno
├── .gitignore             # Exclusión de credenciales y registros locales
└── README.md              # Documentación del proyecto


👤 Autor
Lucas Matias Villalobo - DevOps & Security Operations Enthusiast
