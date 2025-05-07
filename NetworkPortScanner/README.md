# Projet Scanner de Ports Nmap

## Description
Application web de scan de ports réseau utilisant Flask et Nmap.

## Prérequis
- Python 3.7 ou supérieur
- Flask
- Nmap installé sur le système

## Installation
1. Cloner ce dépôt
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'application : `python main.py`

## Utilisation
1. Accéder à la page d'accueil
2. Sélectionner le scanner de ports Nmap
3. Remplir le formulaire avec l'adresse IP et le nom de domaine
4. Choisir le type de scan et lancer le scan

## Structure du projet
- `main.py` : Application principale Flask
- `templates/` : Fichiers HTML pour les pages web
- `static/` : Fichiers CSS et JavaScript

## Fonctionnalités
- Page d'accueil pour sélectionner les outils
- Scanner de ports Nmap avec interface web
- Scan des 1000 ports les plus courants ou ports personnalisés
- Affichage des résultats en temps réel
