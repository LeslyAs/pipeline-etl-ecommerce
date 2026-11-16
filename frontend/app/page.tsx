"use client";

import { useState, useEffect } from "react";

// On définit la structure des données qu'on attend
// (TypeScript nous aide à éviter les erreurs)
type Statistiques = {
  chiffre_affaires_total: number;
  nombre_commandes: number;
  panier_moyen: number;
  produit_top: string;
  ville_top: string;
  top3_produits: [string, number][];
  ca_par_ville: Record<string, number>;
};

export default function Home() {
  // On crée une "boîte" pour stocker les statistiques
  // Au départ elle est vide (null)
  const [stats, setStats] = useState<Statistiques | null>(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState<string | null>(null);

  // useEffect se déclenche automatiquement
  // dès que la page s'affiche
  useEffect(() => {
    fetch("http://localhost:8000/statistiques")
      .then((reponse) => reponse.json())
      .then((donnees) => {
        setStats(donnees);
        setChargement(false);
      })
      .catch((err) => {
        setErreur("Impossible de contacter l'API");
        setChargement(false);
      });
  }, []);

  if (chargement) {
    return <div style={{ padding: 40 }}>Chargement des données...</div>;
  }

  if (erreur) {
    return <div style={{ padding: 40, color: "red" }}>{erreur}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
         Dashboard des Ventes
      </h1>

      {/* Cartes de statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
          <p className="text-gray-500 text-sm">Chiffre d'affaires total</p>
          <h2 className="text-3xl font-bold text-blue-600 mt-2">
            {stats?.chiffre_affaires_total}€
          </h2>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
          <p className="text-gray-500 text-sm">Nombre de commandes</p>
          <h2 className="text-3xl font-bold text-green-600 mt-2">
            {stats?.nombre_commandes}
          </h2>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
          <p className="text-gray-500 text-sm">Panier moyen</p>
          <h2 className="text-3xl font-bold text-purple-600 mt-2">
            {stats?.panier_moyen}€
          </h2>
        </div>
      </div>

      {/* Infos principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-md p-6">
          <p className="text-gray-500 text-sm"> Produit le plus vendu</p>
          <h3 className="text-xl font-semibold text-gray-800 mt-1">
            {stats?.produit_top}
          </h3>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <p className="text-gray-500 text-sm"> Ville qui achète le plus</p>
          <h3 className="text-xl font-semibold text-gray-800 mt-1">
            {stats?.ville_top}
          </h3>
        </div>
      </div>

      {/* Top 3 produits + CA par ville */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">
             Top 3 des produits
          </h3>
          <ul className="space-y-2">
            {stats?.top3_produits.map(([produit, count], index) => (
              <li
                key={produit}
                className="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg"
              >
                <span className="font-medium text-gray-700">
                  {index + 1}. {produit}
                </span>
                <span className="text-blue-600 font-bold">
                  {count} commandes
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">
             Chiffre d'affaires par ville
          </h3>
          <ul className="space-y-2">
            {stats &&
              Object.entries(stats.ca_par_ville)
                .sort((a, b) => b[1] - a[1])
                .map(([ville, ca]) => (
                  <li
                    key={ville}
                    className="flex justify-between items-center bg-gray-50 px-4 py-2 rounded-lg"
                  >
                    <span className="font-medium text-gray-700">{ville}</span>
                    <span className="text-green-600 font-bold">{ca}€</span>
                  </li>
                ))}
          </ul>
        </div>
      </div>
    </div>
  );
}