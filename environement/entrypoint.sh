#!/bin/bash

set -e

echo "[*] Initialisation de Metasploit Framework..."

# Aller dans le dossier Metasploit
cd /opt/metasploit-framework

# Nettoyer les configurations précédentes (optionnel)
echo "[*] Nettoyage des anciennes configurations bundle..."
rm -rf .bundle vendor/bundle

# Configurer bundler pour utiliser un chemin local
echo "[*] Configuration locale de bundler..."
bundle config set --local path 'vendor/bundle'

# Installer les gems manquants
echo "[*] Installation des dépendances Ruby..."
bundle install --gemfile /opt/metasploit-framework/Gemfile

echo "[*] Démarrage de la ToolBox"
rm -r /toolbox
git clone https://github.com/SkarrWho/Projet_Toolbox /toolbox
cd /

python3 /toolbox/workspace/web_app/app.py

