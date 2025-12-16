@echo off
echo ========================================
echo Commit et Push vers GitHub
echo ========================================
echo.

echo Ajout des fichiers...
git add index.html
git add netlify-demo.toml
git add .netlifyignore
git add DEPLOIEMENT-NETLIFY.md
git add QUICK-START-NETLIFY.md
git add README-AIRBNB-RANKING.md

echo.
echo Fichiers ajoutes. Statut:
git status

echo.
echo ========================================
echo Creation du commit...
echo ========================================
git commit -m "Add Netlify deployment configuration and documentation"

echo.
echo ========================================
echo Push vers GitHub...
echo ========================================
git push

echo.
echo ========================================
echo Termine!
echo ========================================
pause


