import csv
import random
import os
from datetime import datetime

# Les données fictives qu'on va utiliser
clients = ["Jean", "Marie", "Paul", "Sophie", "Lucas", "Emma", "Luc", ""]
produits = ["Téléphone", "Laptop", "Tablette", "Casque", "Montre", ""]
villes = ["Paris", "Lyon", "Marseille", "Douala", "Yaoundé", ""]
prix = {
    "Téléphone": 500,
    "Laptop": 1200,
    "Tablette": 300,
    "Casque": 150,
    "Montre": 250,
    "": 0
}

# On génère 20 commandes aléatoires
# Certaines seront incorrectes — c'est voulu !
# C'est la réalité des données brutes
commandes = []
for i in range(1, 21):
    client = random.choice(clients)
    produit = random.choice(produits)
    quantite = random.randint(1, 5)
    ville = random.choice(villes)
    prix_unitaire = prix[produit]

    commandes.append({
        "commande_id": f"CMD{i:03d}",
        "client": client,
        "produit": produit,
        "quantite": quantite,
        "prix_unitaire": prix_unitaire,
        "ville": ville,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

# On sauvegarde les commandes dans raw.csv
# dans le dossier data/
os.makedirs("/app/data", exist_ok=True)

with open("/app/data/raw.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=commandes[0].keys())
    writer.writeheader()
    writer.writerows(commandes)

print("Extract terminé !")
print(f" {len(commandes)} commandes générées dans data/raw.csv")