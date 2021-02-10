# GrosData
Project BigData

Groupe 6

### Authors
Arnaud Guibert, Rémi Huguenot, Valentin Moreau

### Détails Sujet

Score F1 :
- construction matrice de confusion
- calcul via la matrice trouvée (peut-être le *score de base* de scikit-learn)

Score de fairness :
- comparaison entre les labels connus et les labels obtenus après prédiction (sur le jeu de test)
- pour plus de détails, on peut aussi comparer les scores de fairness pour chaque classe métier

### Structure du répertoire 

- Dossier in&out : fichiers de données des prédictions 
- Dossier models : fichier de Sauvegarde du modele entrainé
- Dossier scripts : rassemblement des scripts créés 
- Dossier scripts/AWS : scripts de traitement à mettre dans l'instance EC2 
- Dossier scripts/Hadoop : scripts lancés depuis la machine utilisateur pour la connection et communication à la VM Hadoop ainsi qu'aux instances AWS
- Dossier scripts/MongoDB : description de la base mongoDB et scripts de sauvegarde des données
