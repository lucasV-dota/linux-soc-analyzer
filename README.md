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


---

<Sequence>
  <Step subtitle="Crear la plantilla de credenciales" title="Crear .env.example para GitHub">
    Es un estándar en la industria dejar un archivo de ejemplo público en GitHub para que otros sepan qué variables utiliza el proyecto.
    Crea el archivo `.env.example`:
    ```bash
    nano .env.example
    ```
    Agrega estas dos líneas y guarda (`Ctrl+O`, `Enter`, `Ctrl+X`):
    ```env
    TELEGRAM_TOKEN=TU_TOKEN_DE_TELEGRAM_AQUI
    TELEGRAM_CHAT_ID=TU_CHAT_ID_AQUI
    ```
  </Step>

  <Step subtitle="Guardar la documentación" title="Subir el README y la plantilla a GitHub">
    Empaqueta y sube la nueva documentación a tu repositorio:
    ```bash
    git add README.md .env.example
    git commit -m "docs(readme): agrega documentacion profesional del proyecto y plantilla .env.example"
    git push origin main
    ```
  </Step>
</Sequence>

<ElicitationsGroup message="Con la documentación completa y tu perfil de GitHub destacado, ¿qué paso sigue en tu entrenamiento?">
  <Elicitation label="Aprender Docker Compose" query="Quiero aprender a crear un archivo docker-compose.yml para levantar el SOC y sus variables de entorno con un solo comando simplificado."/>
  <Elicitation label="Simular ataque y probar alertas" query="Quiero realizar una prueba real de ataque desde otra máquina o contenedor para verificar el flujo de bloqueo y la alerta de Telegram."/>
</ElicitationsGroup>
