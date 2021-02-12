# GrosData
Project BigData

Groupe 6

### Authors
Arnaud Guibert, Rémi Huguenot, Valentin Moreau

### Détails Sujet

Score F1 :
- score F1 donné par classe via sklearn.metrics.classification_report

Score de fairness :
- calcul à la main du "disparate_impact" sur les données test

### Structure du répertoire 

- Dossier scripts : rassemblement des scripts créés 
- Dossier scripts/AWS : scripts de traitement à mettre dans l'instance EC2 
- Dossier scripts/AWS/models : fichier de Sauvegarde du modele entrainé
- Dossier scripts/Hadoop : scripts lancés depuis la machine utilisateur pour la connection et communication à la VM Hadoop ainsi qu'aux instances AWS
- Dossier scripts/MongoDB : description de la base mongoDB et scripts de sauvegarde des données

- Fichier machineLearning/build_model_saves.py : (ré)entraînement et scores de test pour les différents modèles (en jonglant avec les paramètres en fin de script)
- Fichier machineLearning/predict.py : production du results.csv en fonction du modèle et du predict.py
