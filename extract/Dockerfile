# On part de l'image officielle Python 3.11
FROM python:3.11-slim

# On définit le dossier de travail dans le conteneur
WORKDIR /app

# On copie notre script extract.py dans le conteneur
# Le point "." signifie "dans le dossier de travail /app"
COPY extract.py .

# La commande qui lance notre script quand le conteneur démarre
CMD ["python", "extract.py"]