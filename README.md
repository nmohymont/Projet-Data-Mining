# Analyse des facteurs d'accidents routier au Royaume Uni

Auteurs : 

MOHYMONT Nicolas : nicolas.mohymont@student.uclouvain.be

VANABELLE Antoine : antoine.vanabelle@student.uclouvain.be


Ce projet s’inscrit dans une démarche d’analyse prédictive des accident routier en cherchant à classifier la gravité des accidents de la route au Royaume-Uni à partir d'une base de données Kaggle: intitulé _Road Accident Dataset_ et publié par l'utilisateur **Xavier Berge**. Le déséquilibrage massif des classes a introduit un défi technique que nous avons essayé de relever via les modèles mis en avant. 

La procédure complète pour récupérer la base de données et réalisées le prétraitement nécessite d'éxécuter :
* ```import_dataset_road_accident.py``` pour récupérer la base de donnée
* ```modify_csv.py``` pour réaliser le nettoyage des données brutes

Pour faciliter l'utilisation de ce Github, l'ensemble des fichiers CSV nécessaire au fonctionne sont pré-installé lors du clonage. 

Voici la liste des modifications réalisés pour le fichier final nettoyé ```Output_Road_Accident_Data.csv``` :
* filtrage des valeurs extrêmes
* enrichissement de données par transformation de variable
* encodage des variables ordinales au format numérique
* discrétisation de la variable Time en 3 catégories Matin/Journée/Nuit
* remplacement des valeurs manquantes

Un second fichier ```sample_balanced_9000.csv``` a été généré pour appliquer la règle de *Undersampling* de la variable cible.

Ensuite un dossier ```MODEL & ASSESSMENT``` permet d'éxécuter les modèles d'apprentissage supervisé :
* ```decision_tree_random_forest.ipynb``` applique des modèles d'arbres de décisions, de forêt aléatoire et de _Gradient Boosting_ sur les données fortement déséquilibrées.
* ```Neural_Networks.ipynb```différents jeux de tests afin d'obtenir les combinaisons proposant les meilleurs solutions (présente dans la partie "Assessment"). 
