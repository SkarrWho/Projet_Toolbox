# 🛠️ Cybersecurity Pentest Toolbox

Projet d’étude M1 Cybersécurité - ESI (2025)  
Outil de pentest automatisé pour la détection, l’exploitation et le suivi de vulnérabilités sur des systèmes autorisés.

## 📦 Description

Cette toolbox propose une suite de scripts Python automatisant :

- Le scan réseau (via `nmap`)
- La détection de vulnérabilités (via `Searchsploit`)
- L’exploitation automatique des failles identifiées (via `Metasploit`)
- Une interface web conviviale pour exécuter et suivre les actions

## ⚙️ Fonctionnalités

- Scan réseau ciblé (`scanner.py`)
- Recherche de vulnérabilités (`vuln_finder.py`)
- Exploits spécifiques (EternalBlue, Heartbleed, MS08-067, Shellshock, Drupalgeddon)
- Exploitation conditionnelle basée sur les vulnérabilités détectées
- Interface web (`web_app/`) avec Flask
- Résultats stockés dans des fichiers CSV
- Exécution via `ToolBox.py` (script principal)
- Conteneurisation et gestion via **Exegol**

## 🐳 Infrastructure via Exegol

Le projet repose sur **Exegol**, un environnement dockerisé de pentest.  
Exegol permet :

- Une installation rapide d’outils de pentest
- La persistance de l’environnement
- La gestion simplifiée de conteneurs
- La génération automatique de logs

## 📁 Arborescence

/workspace
├── ToolBox.py
├── scanner.py
├── vuln_finder.py
├── csv_results/
│ ├── scan_results.csv
│ └── vuln_results.csv
├── every_exploits/
│ ├── eternalblue.py
│ ├── heartbleed.py
│ ├── ms08_067.py
│ └── ...
└── web_app/
├── app.py
├── index.html
└── templates/

bash
Copier
Modifier

## 🚀 Lancer l’interface web

```bash
cd web_app
flask run --host=0.0.0.0 --port=5000
✅ Prérequis
Python 3.11+

Docker & Exegol

Flask

Metasploit Framework

Searchsploit (exploitdb)

⚠️ Avertissement
Utilisation autorisée uniquement sur des systèmes que vous possédez ou avez le droit de tester. Toute utilisation non autorisée est illégale.

👥 Auteurs
LOS POLLOS
SDV CYBER M1 (2025)
