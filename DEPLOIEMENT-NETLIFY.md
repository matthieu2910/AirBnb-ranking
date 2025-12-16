# 🚀 Déploiement sur Netlify - Version Demo

Guide pour déployer la maquette Airbnb Ranking Valais sur Netlify.

## 📋 Prérequis

- Un compte GitHub avec le repo contenant la maquette
- Un compte Netlify (gratuit) : [netlify.com](https://www.netlify.com)

## 🎯 Méthode 1 : Déploiement via GitHub (Recommandé)

### Étape 1 : Connecter Netlify à GitHub

1. Allez sur [app.netlify.com](https://app.netlify.com)
2. Cliquez sur **"Add new site"** → **"Import an existing project"**
3. Choisissez **"Deploy with GitHub"**
4. Autorisez Netlify à accéder à vos repos GitHub
5. Sélectionnez le repo `airbnb-ranking-valais` (ou le nom de votre repo)

### Étape 2 : Configuration du build

Dans les paramètres de déploiement :

- **Build command** : Laissez vide (ou `echo 'No build needed'`)
- **Publish directory** : `.` (point = racine du repo)
- **Base directory** : Laissez vide

### Étape 3 : Fichier de configuration

Netlify utilisera automatiquement le fichier `netlify-demo.toml` si présent, ou vous pouvez :

1. Cliquez sur **"Show advanced"**
2. Ajoutez un fichier `netlify.toml` à la racine avec :
   ```toml
   [build]
     publish = "."
   ```

### Étape 4 : Déployer

1. Cliquez sur **"Deploy site"**
2. Netlify va déployer votre site
3. Vous recevrez une URL automatique (ex: `random-name-123.netlify.app`)

### Étape 5 : Configuration du domaine (optionnel)

1. Dans les paramètres du site → **Domain settings**
2. Cliquez sur **"Options"** → **"Edit site name"**
3. Choisissez un nom personnalisé (ex: `airbnb-ranking-valais-demo`)
4. Votre site sera accessible sur : `airbnb-ranking-valais-demo.netlify.app`

## 🎯 Méthode 2 : Déploiement par glisser-déposer

### Étape 1 : Préparer les fichiers

1. Créez un dossier temporaire
2. Copiez-y ces fichiers :
   - `maquette-airbnb-ranking.html`
   - `index.html` (redirection)
   - `ouvrir-maquette.bat` (optionnel)

### Étape 2 : Déployer

1. Allez sur [app.netlify.com/drop](https://app.netlify.com/drop)
2. Glissez-déposez le dossier dans la zone
3. Netlify déploiera automatiquement
4. Vous recevrez une URL

⚠️ **Note** : Cette méthode ne se connecte pas à GitHub, les mises à jour devront être faites manuellement.

## 🎯 Méthode 3 : Netlify CLI (Pour développeurs)

### Installation

```bash
npm install -g netlify-cli
```

### Déploiement

```bash
# Se connecter à Netlify
netlify login

# Initialiser le site
netlify init

# Déployer
netlify deploy --prod
```

## ⚙️ Configuration avancée

### Variables d'environnement

Si vous ajoutez des fonctionnalités backend plus tard, vous pouvez configurer des variables dans :
- Site settings → Build & deploy → Environment variables

### Headers et redirects

Le fichier `netlify-demo.toml` contient déjà :
- Redirection automatique vers la maquette
- Headers de sécurité
- Cache pour les assets

### Build settings

Pour un site statique HTML, les paramètres sont :
- **Build command** : (vide)
- **Publish directory** : `.`
- **Node version** : (non nécessaire)

## 🔄 Mises à jour automatiques

Avec la méthode GitHub :
- Chaque push sur la branche `main` déclenche un nouveau déploiement
- Les déploiements sont automatiques
- Vous pouvez voir l'historique dans l'onglet "Deploys"

## 📝 Checklist avant déploiement

- [ ] Le fichier `maquette-airbnb-ranking.html` est à la racine
- [ ] Le fichier `index.html` est présent (redirection)
- [ ] Le fichier `netlify-demo.toml` est présent (optionnel)
- [ ] Tous les fichiers sont commités et poussés sur GitHub

## 🎨 Personnalisation de l'URL

1. Allez dans **Site settings** → **Domain settings**
2. Cliquez sur **"Options"** à côté du domaine `.netlify.app`
3. Choisissez **"Edit site name"**
4. Entrez un nom personnalisé (ex: `airbnb-ranking-valais-demo`)
5. Votre site sera sur : `airbnb-ranking-valais-demo.netlify.app`

## 🔒 HTTPS

Netlify fournit automatiquement un certificat SSL gratuit. Votre site sera accessible en HTTPS automatiquement.

## 📊 Analytics (optionnel)

Netlify propose des analytics gratuits :
- Site settings → Analytics
- Activez "Netlify Analytics" pour voir les statistiques de visite

## 🆘 Support

- Documentation Netlify : [docs.netlify.com](https://docs.netlify.com)
- Support Netlify : [support.netlify.com](https://support.netlify.com)

---

**🎉 Une fois déployé, votre maquette sera accessible publiquement sur une URL Netlify !**


