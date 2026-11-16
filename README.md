# Pipeline ETL E-commerce — Docker, PostgreSQL, FastAPI, Next.js

## Objectif du projet

Ce projet simule un pipeline de traitement de données e-commerce complet,
depuis la génération des données brutes jusqu'à leur visualisation dans
un dashboard interactif.

Il illustre une architecture **ETL (Extract, Transform, Load)** conteneurisée
avec Docker, exposée via une API REST et consommée par une interface web moderne.

## Architecture

```
Extract (Python) → Transform (Python) → PostgreSQL → Backend FastAPI → Frontend Next.js
```

- **Extract** : génère des commandes e-commerce (simulant une source de données)
- **Transform** : nettoie les données, supprime les valeurs incorrectes, calcule les totaux
- **PostgreSQL** : stocke les données nettoyées de façon persistante
- **Backend (FastAPI)** : expose les données via une API REST avec calcul de statistiques
- **Frontend (Next.js)** : dashboard visuel affichant les KPIs clés

## Technologies utilisées

| Catégorie | Technologie |
|---|---|
| Conteneurisation | Docker, Docker Compose |
| Base de données | PostgreSQL 16 |
| Backend / API | Python, FastAPI |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Langage pipeline | Python |

## Indicateurs calculés

- Chiffre d'affaires total
- Nombre de commandes
- Panier moyen
- Produit le plus vendu
- Top 3 des produits
- Chiffre d'affaires par ville

## Lancer le projet

```bash
# Lancer le pipeline + API + base de données
docker compose up --build

# Lancer le frontend (dans un autre terminal)
cd frontend
npm install
npm run dev
```

Accès :
- Frontend : http://localhost:3000
- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

##  Compétences démontrées

- Conception d'un pipeline de données structuré (ETL)
- Orchestration de services avec Docker Compose (healthchecks, dépendances)
- Modélisation et requêtage de données avec PostgreSQL
- Exposition de données via API REST
- Visualisation de KPIs métier dans un dashboard

##  Auteur

**Lesly Ashley** — Master Spécialisé Expert Big Data Engineer, UTT