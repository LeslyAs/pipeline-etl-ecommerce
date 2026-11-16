import csv
import os
import psycopg2

print(" Transform démarré...")

input_file = "/app/data/raw.csv"

if not os.path.exists(input_file):
    print(" raw.csv introuvable !")
    print(" Assure-toi qu'Extract a bien tourné.")
    exit(1)

commandes_propres = []
commandes_supprimees = 0

# On lit et on nettoie les données
# (cette partie ne change pas)
with open(input_file, "r") as f:
    reader = csv.DictReader(f)

    for commande in reader:

        if not commande["client"]:
            commandes_supprimees += 1
            continue

        if not commande["produit"]:
            commandes_supprimees += 1
            continue

        if not commande["ville"]:
            commandes_supprimees += 1
            continue

        if int(commande["prix_unitaire"]) == 0:
            commandes_supprimees += 1
            continue

        total = int(commande["quantite"]) * int(commande["prix_unitaire"])
        commande["total"] = total
        commande["client"] = commande["client"].upper()

        commandes_propres.append(commande)

print(f" {len(commandes_propres)} commandes nettoyées")
print(f"  {commandes_supprimees} commandes supprimées car incorrectes")

# ─────────────────────────────────────────
# NOUVELLE PARTIE — Connexion à PostgreSQL
# ─────────────────────────────────────────

print(" Connexion à PostgreSQL...")

connexion = psycopg2.connect(
    host="database",        # nom du service dans docker-compose.yml
    dbname="ecommerce_db",
    user="admin",
    password="admin123"
)

curseur = connexion.cursor()

# On crée la table si elle n'existe pas encore
# C'est important pour que le script puisse
# tourner plusieurs fois sans erreur
curseur.execute("""
    CREATE TABLE IF NOT EXISTS commandes (
        id SERIAL PRIMARY KEY,
        commande_id TEXT,
        client TEXT,
        produit TEXT,
        quantite INTEGER,
        prix_unitaire INTEGER,
        ville TEXT,
        date TEXT,
        total INTEGER
    )
""")

# On vide la table avant d'insérer
# (pour éviter les doublons si on relance le pipeline)
curseur.execute("TRUNCATE TABLE commandes")

# On insère chaque commande propre dans la table
for commande in commandes_propres:
    curseur.execute("""
        INSERT INTO commandes
        (commande_id, client, produit, quantite, prix_unitaire, ville, date, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        commande["commande_id"],
        commande["client"],
        commande["produit"],
        int(commande["quantite"]),
        int(commande["prix_unitaire"]),
        commande["ville"],
        commande["date"],
        commande["total"]
    ))

# On valide les changements (très important !)
connexion.commit()

curseur.close()
connexion.close()

print(" Transform terminé !")
print(f" {len(commandes_propres)} commandes enregistrées dans PostgreSQL")