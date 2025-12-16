# Instructions pour créer un nouveau repo GitHub et pousser le code

## Étape 1 : Créer le repo sur GitHub

1. Allez sur [GitHub.com](https://github.com) et connectez-vous
2. Cliquez sur le bouton **"+"** en haut à droite → **"New repository"**
3. Remplissez les informations :
   - **Repository name** : `airbnb-ranking-valais` (ou le nom de votre choix)
   - **Description** : "Maquette HTML pour Airbnb Ranking Valais"
   - **Visibility** : Public ou Private (selon votre choix)
   - **NE PAS** cocher "Initialize this repository with a README"
4. Cliquez sur **"Create repository"**

## Étape 2 : Initialiser Git localement (si pas déjà fait)

Ouvrez un terminal (Git Bash, PowerShell, ou CMD) dans le dossier du projet et exécutez :

```bash
# Initialiser git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Faire le premier commit
git commit -m "Initial commit: Maquette Airbnb Ranking Valais"
```

## Étape 3 : Connecter au repo GitHub

```bash
# Ajouter le remote (remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub)
git remote add origin https://github.com/VOTRE_USERNAME/airbnb-ranking-valais.git

# Ou si vous utilisez SSH :
# git remote add origin git@github.com:VOTRE_USERNAME/airbnb-ranking-valais.git
```

## Étape 4 : Pousser le code

```bash
# Renommer la branche principale en main (si nécessaire)
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

## Alternative : Utiliser GitHub Desktop

Si vous préférez une interface graphique :

1. Téléchargez [GitHub Desktop](https://desktop.github.com/)
2. Installez-le et connectez-vous avec votre compte GitHub
3. File → Add Local Repository → Sélectionnez ce dossier
4. Cliquez sur "Publish repository" pour créer le repo sur GitHub

## Fichiers importants à inclure

- ✅ `maquette-airbnb-ranking.html` - La maquette principale
- ✅ `ouvrir-maquette.bat` - Script pour ouvrir la maquette
- ✅ `README-AIRBNB-RANKING.md` - Documentation
- ✅ `.gitignore` - Fichiers à ignorer


