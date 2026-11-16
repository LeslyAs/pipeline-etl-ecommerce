from fastapi import FastAPI
import psycopg2
from collections import Counter

# On crée l'application FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# On autorise le Frontend (localhost:3000)
# à venir parler à notre API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Fonction qui ouvre une connexion à PostgreSQL
# On la met dans une fonction car on va
# l'utiliser plusieurs fois (éviter de répéter le code)
def get_connexion():
    return psycopg2.connect(
        host="database",
        dbname="ecommerce_db",
        user="admin",
        password="admin123"
    )


# ─────────────────────────────────────
# ROUTE 1 — Page d'accueil (test simple)
# ─────────────────────────────────────

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API e-commerce !"}


# ─────────────────────────────────────
# ROUTE 2 — Liste de toutes les commandes
# ─────────────────────────────────────

@app.get("/commandes")
def lister_commandes():
    connexion = get_connexion()
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT commande_id, client, produit, quantite,
               prix_unitaire, ville, date, total
        FROM commandes
    """)

    lignes = curseur.fetchall()
    curseur.close()
    connexion.close()

    # On transforme chaque ligne en dictionnaire
    # pour que ce soit facile à lire en JSON
    commandes = []
    for ligne in lignes:
        commandes.append({
            "commande_id": ligne[0],
            "client": ligne[1],
            "produit": ligne[2],
            "quantite": ligne[3],
            "prix_unitaire": ligne[4],
            "ville": ligne[5],
            "date": ligne[6],
            "total": ligne[7]
        })

    return commandes


# ─────────────────────────────────────
# ROUTE 3 — Statistiques calculées
# ─────────────────────────────────────

@app.get("/statistiques")
def obtenir_statistiques():
    connexion = get_connexion()
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT produit, ville, total
        FROM commandes
    """)

    lignes = curseur.fetchall()
    curseur.close()
    connexion.close()

    if not lignes:
        return {"erreur": "Aucune commande trouvée"}

    produits = [ligne[0] for ligne in lignes]
    villes = [ligne[1] for ligne in lignes]
    totaux = [ligne[2] for ligne in lignes]

    ca_total = sum(totaux)
    nb_commandes = len(lignes)
    panier_moyen = ca_total / nb_commandes

    produit_top = Counter(produits).most_common(1)[0][0]
    ville_top = Counter(villes).most_common(1)[0][0]
    top3_produits = Counter(produits).most_common(3)

    ca_par_ville = {}
    for ligne in lignes:
        ville = ligne[1]
        total = ligne[2]
        if ville not in ca_par_ville:
            ca_par_ville[ville] = 0
        ca_par_ville[ville] += total

    return {
        "chiffre_affaires_total": ca_total,
        "nombre_commandes": nb_commandes,
        "panier_moyen": round(panier_moyen, 2),
        "produit_top": produit_top,
        "ville_top": ville_top,
        "top3_produits": top3_produits,
        "ca_par_ville": ca_par_ville
    }