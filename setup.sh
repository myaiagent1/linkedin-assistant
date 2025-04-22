#!/bin/bash

# Afficher les commandes pour le débogage
set -x

# Installation des dépendances requises
apt-get update
apt-get install -y wget gnupg

# Installer Playwright avec les dépendances et le navigateur
echo "Installation des navigateurs Playwright..."
python -m playwright install --with-deps chromium

# Vérifier si l'installation a réussi
echo "Vérification du chemin des navigateurs installés..."
ls -la /home/appuser/.cache/ms-playwright/

# Corriger les permissions du dossier Playwright
echo "Mise à jour des permissions..."
chmod -R 755 /home/appuser/.cache/ms-playwright/
