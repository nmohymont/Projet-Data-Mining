# Analyse des facteurs d'accidents routier au Royaume Uni

Ce projet s’inscrit dans une démarche d’analyse prédictive des accident routier en cherchant à classifier la gravité des accidents de la route au Royaume-Uni à partir d'une base de données Kaggle: intitulé _Road Accident Dataset_ et publié par l'utilisateur **Xavier Berge**. Le déséquilibrage massif des classes a introduit un défi technique que nous avons essayé de relever via les modèles mis en avant. 

La procédure complète pour récupérer la base de données et réalisées le prétraitement nécessite d'éxécuter :
* ```import_dataset_road_accident.py``` pour récupérer la base de donnée
* ```modify_csv.py``` pour réaliser le nettoyage des données brutes

Pour faciliter l'utilisation de ce Github, l'ensemble des fichiers CSV nécessaire au fonctionne sont pré-installé lors du clonage. 

Voici la liste des modifications réalisés pour les différents fichiers nettoyées :
* 

Ensuite un dossier ```MODEL & ASSESSMENT``` permet d'éxécuter les modèles d'apprentissage supervisé :
* ```decision_tree_random_forest.py``` applique des modèles d'arbres de décisions, de forêt aléatoire et de _Gradient Boosting_ sur les données fortement déséquilibrées.
* ```ajouter non du fichier réseau neurone.py```

To use this code, we just need to have the file 'Road Accident Data.csv' and 'correspondance region et police_force.csv'.

When launching the code, a 'Append_Time_cat_Road_Accident_Data.csv' file will be created with the changes.

The modifications are as follows:
- Sort modalities of certain variables (elimination of exceptional values abérantes)
- Transformations of ordinal variables into numerical variables (creation of new columns for them)
- Creation of new categories (EX: the hour and classified according to the time of day morning/afternoon/evening) 
- Box plot creation for information purposes 