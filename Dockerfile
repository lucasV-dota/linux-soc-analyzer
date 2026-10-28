# 1. Traer un Linux ultraligero que ya tenga Python instalado
FROM python:3.9-slim

# 2. Entrar a una carpeta llamada /app dentro del contenedor
WORKDIR /app

# 3. Instalar herramientas de red adentro del contenedor por si las necesita
RUN apt-get update && apt-get install -y ufw sudo

# 4. Copiar tu script desde tu PC real hacia el interior de la caja
COPY soc_integrador.py daemon_soc.py ./

# 5. El comando que se ejecutará al encender el contenedor
CMD ["python3", "daemon_soc.py"]
