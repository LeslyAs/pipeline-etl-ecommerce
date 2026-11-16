FROM python:3.11-slim

WORKDIR /app

# On copie d'abord requirements.txt SEUL
# Pourquoi ? Pour profiter du cache Docker :
# si on modifie main.py plus tard,
# Docker n'aura pas besoin de réinstaller
# toutes les bibliothèques à chaque fois
COPY requirements.txt .

# On installe toutes les bibliothèques
# listées dans requirements.txt d'un coup
RUN pip install -r requirements.txt

# Maintenant on copie le code de l'API
COPY main.py .

# On expose le port 8000
# (le port standard pour les APIs FastAPI)
EXPOSE 8000

# La commande qui lance le serveur
# --host 0.0.0.0 : accepte les connexions
#                  venant de l'extérieur du conteneur
# --port 8000    : écoute sur le port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]