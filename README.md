# SmartBetNaYo

<p align="center">
  <img src="./images/stats_predict.jpg" alt="Probalilité d'un match de football">
</p>

SmartBetNaYo est une application de prédiction de résultats de matches de football, qui utilise des statistiques historiques et l'analyse de Poisson pour fournir des probabilités sur les issues de matchs, spécialement conçue pour les parieurs sportifs. Cette solution aide à faire des paris informés en calculant les chances de différents résultats de match, y compris les scores exacts, les chances de victoire/défaite/nul et la probabilité que les deux équipes marquent.

## Fonctionnalités

- Récupération automatique des données de ligue via l'API-football.
- Calcul des probabilités basé sur la distribution de Poisson pour les scores exacts.
- Prédictions de "Both Teams to Score" (BTTS).
- Estimations des probabilités de sur/sous objectifs (Over/Under Goals).

## Technologies Utilisées

- Python 3
- Bibliothèques Python : `requests`, `matplotlib`, `numpy`, `scipy`
- API-football pour les données de match en temps réel.

## Comment Utiliser

1. Clonez le repository :
   ```bash
   git clone git@github.com:enzoforreal/SmartBetNaYo.git
   cd SmartBetNaYo


