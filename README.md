# SmartBetNaYo

<p align="center">
  <img src="./images/stats_predict.jpg" alt="Probabilité d'un match de football" width="500">
</p>

**SmartBetNaYo** est une application de prédiction de résultats de matches de football qui utilise des statistiques historiques et l'analyse de Poisson pour fournir des probabilités sur les issues de matchs. Conçue spécialement pour les parieurs sportifs, cette solution aide à faire des paris informés en calculant les chances de différents résultats de match, y compris les scores exacts, les chances de victoire/défaite/nul, et la probabilité que les deux équipes marquent.

## Fonctionnalités

- **Récupération automatique des données de ligue** via l'API-football.
- **Calcul des probabilités** basé sur la distribution de Poisson pour les scores exacts.
- **Prédictions de "Both Teams to Score" (BTTS)**.
- **Estimations des probabilités de sur/sous objectifs (Over/Under Goals)**.

## Technologies Utilisées

- **Python 3**
- **Bibliothèques Python** : `requests`, `matplotlib`, `numpy`, `scipy`
- **API-football** pour les données de match en temps réel.

## Comment Utiliser

Pour utiliser SmartBetNaYo, suivez les étapes suivantes :

```bash
git clone git@github.com:enzoforreal/SmartBetNaYo.git
cd SmartBetNaYo


## Installation

Ensuite, installez les dépendances nécessaires :
```bash
pip install -r requirements.txt



Contribuer
SmartBetNaYo est ouvert aux contributions de développeurs, statisticiens, et passionnés de paris sportifs. Si vous avez des idées pour améliorer les prédictions, intégrer l'intelligence artificielle, ou optimiser les algorithmes existants, votre aide est la bienvenue!

Comment contribuer ?
Fork le projet sur GitHub.
Clonez votre fork localement :
  ```bash
  git clone https://github.com/<your-username>/SmartBetNaYo.git


Créez une nouvelle branche pour vos modifications :

  ```bash
  git checkout -b votre_branche


Faites vos modifications et modifiez les fichiers nécessaires dans votre projet local.
Committez vos modifications :

  ```bash
  git add .
  git commit -m "Description des modifications"


Faites vos modifications et modifiez les fichiers nécessaires dans votre projet local.
Committez vos modifications :

  ```bash
  git push origin <nom_de_votre_branche>

Ouvrez une Pull Request pour merger vos modifications :
Accédez à votre fork sur GitHub, cliquez sur 'Pull Request' et ensuite sur 'New Pull Request'. Choisissez votre branche et validez en cliquant sur 'Create pull request'.

Nous apprécions vos idées et encouragements à améliorer SmartBetNaYo! :

Toute contribution est bienvenue et aide à rendre l'application plus efficace et utile pour tous.

