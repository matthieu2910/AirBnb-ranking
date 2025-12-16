# 📝 Commandes pour committer les fichiers Netlify

## Option 1 : Utiliser GitHub Desktop

1. Ouvrez **GitHub Desktop**
2. Vous verrez les nouveaux fichiers dans la colonne de gauche
3. Ajoutez un message de commit : `Add Netlify deployment configuration and documentation`
4. Cliquez sur **"Commit to main"**
5. Cliquez sur **"Push origin"**

## Option 2 : Utiliser Git Bash ou Terminal

Ouvrez Git Bash (ou un terminal avec Git) dans ce dossier et exécutez :

```bash
# Ajouter tous les nouveaux fichiers
git add index.html
git add netlify-demo.toml
git add .netlifyignore
git add DEPLOIEMENT-NETLIFY.md
git add QUICK-START-NETLIFY.md
git add README-AIRBNB-RANKING.md

# Vérifier les fichiers ajoutés
git status

# Créer le commit
git commit -m "Add Netlify deployment configuration and documentation"

# Pousser vers GitHub
git push
```

## Option 3 : Utiliser le script batch

Double-cliquez sur `commit-et-push.bat` (si Git est installé et dans le PATH)

## 📋 Fichiers à committer

- ✅ `index.html` - Redirection vers la maquette
- ✅ `netlify-demo.toml` - Configuration Netlify
- ✅ `.netlifyignore` - Fichiers à exclure
- ✅ `DEPLOIEMENT-NETLIFY.md` - Guide complet
- ✅ `QUICK-START-NETLIFY.md` - Guide rapide
- ✅ `README-AIRBNB-RANKING.md` - Documentation

## ✅ Après le commit

Une fois les fichiers poussés sur GitHub, vous pouvez :
1. Aller sur [app.netlify.com](https://app.netlify.com)
2. Connecter votre repo GitHub
3. Déployer la maquette en suivant `QUICK-START-NETLIFY.md`


