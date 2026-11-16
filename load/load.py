import psycopg2
from collections import Counter

print(" Load démarré...")

# ─────────────────────────────────────
# Connexion à PostgreSQL
# ─────────────────────────────────────

print(" Connexion à PostgreSQL...")

connexion = psycopg2.connect(
    host="database",
    dbname="ecommerce_db",
    user="admin",
    password="admin123"
)

curseur = connexion.cursor()

# On récupère toutes les commandes de la table
curseur.execute("""
    SELECT client, produit, quantite, prix_unitaire, ville, total
    FROM commandes
""")

lignes = curseur.fetchall()

curseur.close()
connexion.close()

# Si la table est vide
if not lignes:
    print(" Aucune commande trouvée dans la base !")
    exit(1)

# ─────────────────────────────────────
# Reconstruire des dictionnaires
# (comme avant avec le CSV, pour ne pas
#  changer la logique de calcul)
# ─────────────────────────────────────

commandes = []
for ligne in lignes:
    commandes.append({
        "client": ligne[0],
        "produit": ligne[1],
        "quantite": ligne[2],
        "prix_unitaire": ligne[3],
        "ville": ligne[4],
        "total": ligne[5]
    })

# ── CALCUL DES STATISTIQUES ──────────────────
# (cette partie ne change pas du tout)

ca_total = sum(c["total"] for c in commandes)
nb_commandes = len(commandes)
panier_moyen = ca_total / nb_commandes

produits = [c["produit"] for c in commandes]
produit_top = Counter(produits).most_common(1)[0][0]
top3_produits = Counter(produits).most_common(3)

villes = [c["ville"] for c in commandes]
ville_top = Counter(villes).most_common(1)[0][0]

ca_par_ville = {}
for c in commandes:
    ville = c["ville"]
    if ville not in ca_par_ville:
        ca_par_ville[ville] = 0
    ca_par_ville[ville] += c["total"]

# ── AFFICHAGE DU RAPPORT ─────────────────────

print("\n")
print("=" * 45)
print("  RAPPORT DES VENTES DU JOUR")
print("   (données issues de PostgreSQL)")
print("=" * 45)
print(f" Chiffre d'affaires total : {ca_total}€")
print(f" Nombre de commandes      : {nb_commandes}")
print(f" Panier moyen             : {panier_moyen:.2f}€")
print(f" Produit le plus vendu    : {produit_top}")
print(f" Ville qui achète le plus : {ville_top}")
print("-" * 45)
print(" TOP 3 DES PRODUITS :")
for i, (produit, count) in enumerate(top3_produits, 1):
    print(f"   {i}. {produit} → {count} commandes")
print("-" * 45)
print(" CHIFFRE D'AFFAIRES PAR VILLE :")
for ville, ca in sorted(ca_par_ville.items(),
                         key=lambda x: x[1],
                         reverse=True):
    print(f"   {ville} → {ca}€")
print("=" * 45)
print(" Load terminé !")