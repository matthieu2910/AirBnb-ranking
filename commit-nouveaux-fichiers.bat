@echo off
echo ========================================
echo Commit des nouveaux fichiers vers GitHub
echo ========================================
echo.

echo Ajout des fichiers API et Analyse...
git add api_analyse.py
git add analyse_airbnb_ameliore.py
git add analyse_airbnb.py
git add analyse_airbnb_selenium.py
git add requirements_api.txt
git add requirements_analyse.txt

echo.
echo Ajout des pages web...
git add resultats_analyse.html

echo.
echo Ajout de la configuration...
git add .netlifyignore
git add .gitignore

echo.
echo Ajout de la documentation...
git add README-INTEGRATION.md
git add DEMARRAGE-API.md
git add RESUME-INTEGRATION.md
git add RAPPORT-TEST-ANALYSE.md
git add README-ANALYSE-AIRBNB.md
git add QUICK-START-NETLIFY.md
git add DEPLOIEMENT-NETLIFY.md
git add test_analyse.py
git add AJOUTER-AU-REPO.md
git add VERIFIER-REPO-GITHUB.md

echo.
echo Mise a jour de la maquette...
git add maquette-airbnb-ranking.html

echo.
echo ========================================
echo Statut des fichiers...
echo ========================================
git status

echo.
echo ========================================
echo Creation du commit...
echo ========================================
git commit -m "Add API d'analyse Airbnb et integration complete

- API Flask pour l'analyse d'annonces Airbnb
- Scripts d'analyse ameliore avec cache et validation
- Page de resultats HTML
- Documentation complete
- Integration dans la maquette"

echo.
echo ========================================
echo Push vers GitHub...
echo ========================================
git push origin main

echo.
echo ========================================
echo Termine!
echo ========================================
echo.
echo Verifiez sur: https://github.com/matthieu2910/AirBnb-ranking
pause

