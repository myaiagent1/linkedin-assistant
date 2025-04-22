#!/bin/bash

# Débogage - affiche les commandes exécutées
set -x

echo "Installation des dépendances système..."
apt-get update
apt-get install -y wget gnupg libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libfontconfig1

echo "Installation des navigateurs Playwright..."
python -m playwright install --with-deps chromium

echo "Vérification de l'installation..."
ls -la /home/appuser/.cache/ms-playwright/ || echo "Dossier ms-playwright non trouvé"

echo "Configuration des permissions..."
chmod -R 755 /home/appuser/.cache/ || echo "Impossible de modifier les permissions"

echo "Setup terminé"
