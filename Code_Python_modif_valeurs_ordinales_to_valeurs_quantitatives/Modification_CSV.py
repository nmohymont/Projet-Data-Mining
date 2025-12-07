"""
OBJECTIF DU SCRIPT :
Ce script lit un fichier CSV de données d'accidents routiers (Road Accident Data.csv),
transforme les valeurs de la colonne "Accident_Severity" (Slight → 1, Serious → 2, Fatal → 3, Missing → 4),
et sauvegarde le fichier modifié dans un dossier de sortie avec numérotation automatique.
"""

import pandas as pd          # Bibliothèque pour manipuler des données tabulaires (CSV, Excel, etc.)
from pathlib import Path     # Gestion sécurisée des chemins de fichiers (Windows/Linux)
import glob                  # Recherche de fichiers avec motifs (wildcards)
import os                    # Opérations système (non utilisé ici mais importé)
import sys                   # Accès aux arguments système et gestion d'erreurs

# =====================================================
# ÉTAPE 1 : DÉFINITION DES CHEMINS
# =====================================================

# Use repository/workspace-relative paths so the script works on any machine
# `base_folder` is the directory containing this script; input CSV is expected
# to be next to this script (same folder). This avoids hard-coded local OneDrive paths.
base_folder = Path(__file__).resolve().parent

# Chemin vers le fichier CSV d'entrée (attendu dans le même dossier que ce script)
input_csv = base_folder / "Road Accident Data.csv"

# Nom du sous-dossier de sortie (sans accents pour éviter les problèmes de compatibilité)
output_subfolder_name = "Nouvelles_donnees"

# Construction du chemin complet du dossier de sortie (base_folder + sous-dossier)
output_folder = base_folder / output_subfolder_name


# =====================================================
# ÉTAPE 2 : DIAGNOSTIC - Afficher l'état avant création
# =====================================================
# Cela aide à déboguer en cas de problème : on voit exactement les chemins utilisés

print("########")
print("Base folder:", base_folder)                      # Affiche le dossier parent
print("Output folder (voulu):", output_folder)          # Affiche le chemin du sous-dossier souhaité
print("Existe déjà ?", output_folder.exists())          # Vérifie si le dossier existe déjà
print("############")

# =====================================================
# ÉTAPE 3 : CRÉATION DU DOSSIER DE SORTIE (avec gestion d'erreurs)
# =====================================================
# Le script crée le dossier s'il n'existe pas, et gère les erreurs possibles
try:
    # mkdir() crée le dossier
    # parents=True : crée aussi les dossiers parents si nécessaire
    # exist_ok=True : ne lève pas d'erreur si le dossier existe déjà
    output_folder.mkdir(parents=True, exist_ok=True)
    print("Dossier créé (ou déjà existant) :", output_folder)
except PermissionError:
    # L'utilisateur n'a pas les droits de créer le dossier
    print("Erreur : permission refusée pour créer le dossier :", output_folder, file=sys.stderr)
    sys.exit(1)  # Arrête le script (code d'erreur = 1)
    


# Calcul du nom du fichier de sortie avec numérotation automatique
# --- Nom de base et extension ---
base_name = "Road_Accident_Data_modified"
extension = ".csv"

# --- Trouver le prochain numéro disponible ---
pattern = str(output_folder / (base_name + "_*" + extension))
existing_files = glob.glob(pattern)

numbers = []
for f in existing_files:
    name = Path(f).stem  # e.g. Road_Accident_Data_modified_3
    # extraire la partie après le dernier underscore
    try:
        num_str = name.split("_")[-1]
        num = int(num_str)
        numbers.append(num)
    except ValueError:
        # ignore les fichiers sans numéro à la fin
        pass

next_num = max(numbers) + 1 if numbers else 1
output_csv = output_folder / f"{base_name}_{next_num}{extension}"


# =====================================================
# Partie analyse et modification du CSV


# --- Lecture du CSV ---
if not input_csv.exists():
    print("Erreur : le fichier d'entrée n'existe pas :", input_csv, file=sys.stderr)
    sys.exit(1)

df = pd.read_csv(input_csv)
print("")
print(f"Lecture du fichier : {df.shape[0]} lignes et {df.shape[1]} colonnes")
print("")
print("Colonnes disponibles :", df.columns.tolist())

# --- Accident_Severity ---
mapping = {
    "Slight": 1,
    "Serious": 2,
    "Fatal": 3,
    "Missing": 4
}

# --- Application du mapping (avec sécurité si colonne manquante) ---
col = "Accident_Severity"
if col not in df.columns:
    print(f"Attention : la colonne '{col}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    df[col] = df[col].map(mapping)


# --- Light_Conditions ---
light_mapping = {
    "Daylight": 1,
    "Darkness - lights lit": 2,
    "Darkness - no lighting": 3,
    "Darkness - lighting unknown": 3,
    "Darkness - lights unlit": 3,
    "Missing": 4
}

df["Light_Conditions"] = df["Light_Conditions"].map(light_mapping)


# --- Sauvegarde du nouveau CSV ---
df.to_csv(output_csv, index=False)
print("")
print("")
print("Fichier modifié sauvegardé sous :", output_csv)
