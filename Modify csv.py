import pandas as pd 
import numpy as np
import sys


df = pd.read_csv('Road Accident Data.csv')
df_mapping_region = pd.read_csv('correspondance region et police_force.csv', sep =';')

#print(df.columns.tolist())
print(f'Taille initiale du dataset : {df.shape[0]} lignes, {df.shape[1]} colonnes')

#~ prend la négation ceux qui ne respecte pas le format HH:MM
#isna() retourne True pour les valeurs non convertibles en datetime
invalid_time_mask = ~pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').isna()
#print(df[invalid_time_mask]) # rien n'est affiché, toutes les valeurs sont valides

#print(df_mapping_region.head(5))
#print(df_mapping_region.columns)
#print(df['Police_Force'].unique ())

df_mapping_region = df_mapping_region.dropna(subset=["Region"])
#print(df_mapping_region.head(5))

paires = list(zip(df_mapping_region['\nList of police forces of the United Kingdom'], df_mapping_region['Region']))
mapping_police_force = dict(paires)

df['Region'] = df['Police_Force'].map(mapping_police_force)

#print(df[["Police_Force", "Region"]]) #check result
#print(df[df["Region"].isna()]) #check the NaN values but it matches exaclty the inital missing value

def duration_to_numeric(duration):
    try:
        h, m = map(int, duration.split(':'))
        return round(h + m / 60, 2)
    except:
        return None

df['Num_Time'] = df['Time'].apply(duration_to_numeric)

def categorize_time(hour):
    if (hour >= 18) or (hour < 5):
        return "Night"
    elif 5 <= hour < 9:
        return "Morning"
    elif 9 <= hour < 18:
        return "Daytime"
    else:
        return "Missing"

df['Time_cat'] = df['Num_Time'].apply(categorize_time)

#réorganiser les colonnes : placer Time_cat après Time
cols = list(df.columns)
time_index = cols.index('Time')
new_order = cols[:time_index + 1] + ['Num_Time'] + ['Time_cat'] + cols[time_index + 1:-2]
df = df[new_order]

#   Vérifier les colonnes supplémentaires
#print(df[['Time','Time_cat','Num_Time']].head())

#df.to_csv('Append_Time_cat_Road_Accident_Data.csv', index=False)



#------------------------------------------------------------
#Rajout partie Antoine 

#Code permettant de savoir combien de modalité "fatal" est présente dans le dataset
def test_count_fatal():
    fatal_count = df['Accident_Severity'].value_counts().get('Fatal', 0)
    print(f"Nombre d'occurrences de 'Fatal' dans 'Accident_Severity': {fatal_count}")

test_count_fatal()

# --- Accident_Severity ---
Range_acident_severity = 3

mapping = {
    # round(calcul, 1) arrondit le résultat à 1 chiffre après la virgule
    "Slight": round(1/Range_acident_severity, 1),   # Deviendra 0.3
    "Serious": round(2/Range_acident_severity, 1),  # Deviendra 0.7
    "Fatal": round(3/Range_acident_severity, 1),    # Deviendra 1.0
    #"Missing": 4
}

# --- Application du mapping ---
col = "Accident_Severity"
if col not in df.columns:
    print(f"Attention : la colonne '{col}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Application du mapping
    df[f"{col}_numeric"] = df[col].map(mapping)
    
    # Réorganiser les colonnes
    cols = list(df.columns)
    cols.insert(cols.index(col) + 1, cols.pop(cols.index(f"{col}_numeric")))
    df = df[cols]


# --- Light_Conditions ---
Range_light_conditions = 3

light_mapping = {
    "Daylight": round(1/Range_light_conditions, 1),          # Deviendra 0.3
    "Darkness - lights lit": round(2/Range_light_conditions, 1),      # Deviendra 0.7 
    "Darkness - no lighting": round(3/Range_light_conditions, 1),        # Deviendra 1.0
    "Darkness - lighting unknown": round(3/Range_light_conditions, 1), # Deviendra 1.0
    "Darkness - lights unlit": round(3/Range_light_conditions, 1)      # Deviendra 1.0
    #"Missing": 4
}
# --- Application du mapping ---
Light = "Light_Conditions"
if Light not in df.columns:
    print(f"Attention : la colonne '{Light}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{Light}_numeric"] = df[Light].map(light_mapping)
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(Light) + 1, cols.pop(cols.index(f"{Light}_numeric")))
    df = df[cols]


# --- Road_Surface_Conditions ---
Range_Road_surface = 5

road_surface_mapping = {
    "Dry": round(1/Range_Road_surface, 2),               # Deviendra 0.20
    "Wet or damp": round(2/Range_Road_surface, 2),        # Deviendra 0.40
    "Snow": round(4/Range_Road_surface, 2),               # Deviendra 0.80
    "Frost or ice": round(5/Range_Road_surface, 2),          # Deviendra 1.00
    "Flood over 3cm. deep": round(3/Range_Road_surface, 2),   # Deviendra 0.60
    #"Missing": round(6/Range_Road_surface, 2)               # drop les missing = 317 instances
}

# --- Application du mapping ---
Road = "Road_Surface_Conditions"
if Road not in df.columns:
    print(f"Attention : la colonne '{Road}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{Road}_numeric"] = df[Road].map(road_surface_mapping)
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(Road) + 1, cols.pop(cols.index(f"{Road}_numeric")))
    df = df[cols]

df = df.dropna(subset=[Road])


# --- Time_cat --- 
Range_Time_cat = 3

Time_cat_mapping = {
    "Daytime": round(2/Range_Time_cat, 2),      # Deviendra 0.66   
    "Night": round(3/Range_Time_cat, 2),        # Deviendra 1.00
    "Morning": round(1/Range_Time_cat, 2),      # Deviendra 0.33
    #"Missing": round(4/Range_Time_cat, 2)       # drop missing = 17 instances
}

# --- Application du mapping ---
TimeCat = "Time_cat"
if TimeCat not in df.columns:
    print(f"Attention : la colonne '{TimeCat}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{TimeCat}_numeric"] = df[TimeCat].map(Time_cat_mapping)
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(TimeCat) + 1, cols.pop(cols.index(f"{TimeCat}_numeric")))
    df = df[cols]

df = df.dropna(subset=[TimeCat])

# --- Sauvegarde du nouveau CSV ---
#df.to_csv(output_csv, index=False)
#print("")
#print("")
#print("Fichier modifié sauvegardé sous :", output_csv)

df = df.drop(columns=['Carriageway_Hazards'])
df = df.dropna()

#------------------------------------------------------------------

####calcul de boxlpots a titre indicatif

def test_calcul_boxplot():



    Q1_casualties = df['Number_of_Casualties'].quantile(0.25)
    Q3_casualties = df['Number_of_Casualties'].quantile(0.75)
    IQR_casualties = Q3_casualties - Q1_casualties

    #print(Q1_casualties, Q3_casualties, IQR_casualties)

    Q1_vehicle =df['Number_of_Vehicles'].quantile(0.25)
    Q3_vehicle = df['Number_of_Vehicles'].quantile(0.75)
    IQR_vehicle = Q3_vehicle - Q1_vehicle

    #print(Q1_vehicle, Q3_vehicle, IQR_vehicle)

    Q1_time =df['Num_Time'].quantile(0.25)
    Q3_time = df['Num_Time'].quantile(0.75)
    IQR_time = Q3_time - Q1_time

    upper_bound_time = Q3_time + 1.5 * IQR_time
    lower_bound_time = Q1_time - 1.5 * IQR_time 

    #print(lower_bound_time,Q1_time, Q3_time, upper_bound_time)

    Q1_latitude =df['Latitude'].quantile(0.25)
    Q3_latitude = df['Latitude'].quantile(0.75)
    IQR_latitude = Q3_latitude - Q1_latitude

    x=1.5 

    upper_bound_latitude = Q3_latitude + x* IQR_latitude
    lower_bound_latitude = Q1_latitude - x* IQR_latitude 

    #print(lower_bound_latitude,Q1_latitude, Q3_latitude, upper_bound_latitude)
    #print(df['Latitude'].min(),df['Latitude'].max())

### regroupement des valeurs aberrantes dans des catégories NaN aussi Autre 

treshold_casualties = 7 #seuil equivalent à minimum 0.1%

df.loc[df['Number_of_Casualties'] >treshold_casualties, "Number_of_Casualties"] = treshold_casualties

#print(df['Number_of_Casualties'].unique(),  df['Number_of_Casualties'].count() ) #vérification des valeurs enregistrées et compter le nombre de rows 

treshold_number_vehicle = 6 #seuil equivalent à minimum 0.1%

df.loc[df['Number_of_Vehicles'] >treshold_number_vehicle, "Number_of_Vehicles"] = treshold_number_vehicle
#print(df['Number_of_Vehicles'].unique(), df['Number_of_Vehicles'].count())

df = df[~df["Speed_limit"].isin([10, 15])] #~ df["Speed_limit"].isin([10, 15]) ou ~ prend la négation de la sélection des lignes ou la valeur vaut 10 ou 15
print(f'Taille  dataset après retrait des speed_limit 10 et 15 et des NA ordinale->numérique: {df.shape[0]} lignes, {df.shape[1]} colonnes')


###modification attributs Data missing or out of range vers Not a junction or within 20 metres

#print('Avant changement')
#print(df["Junction_Control"].unique())#check attributs de junction_control

junction_control_mask={
    'Data missing or out of range' : 'Not at junction or within 20 metres'
} 

df['Junction_Control'] = df['Junction_Control'].replace(junction_control_mask)

#print('Après changement')
#print(df["Junction_Control"].unique())

###modifier attributs vehicle types l'idée est de remplacer toutes les catégories ayant une fréquence inférieur à 1% dans une classe Autre

#print('Avant changement')
#print(df["Vehicle_Type"].unique())#check attributs de junction_control

vehicle_mask ={ #seuil équivalent au fréquence inférieur à 1%
    'Goods over 3.5t. and under 7.5t' : 'Other',
    'Other vehicle' : 'Other',
    'Minibus (8 - 16 passenger seats)' : 'Other',
    'Agricultural vehicle' : 'Other',
    'Pedal cycle' : 'Other',
    'Ridden horse' :'Other'
}

df['Vehicle_Type'] = df['Vehicle_Type'].replace(vehicle_mask)

#print('Après changement')
#print(df["Vehicle_Type"].unique()) #vérification bonne


# --- Sauvegarde du CSV final avec toutes les modifications ---
df.to_csv('Output_Road_Accident_Data.csv', index=False)
#print("\nFichier sauvegardé : Append_Time_cat_Road_Accident_Data.csv")

#----------------------------------------------------------------
#Création d'un échantillon équilibré à partir du dataset modifié


# 1. Chargement des données
file_path = 'Output_Road_Accident_Data.csv' 
df = pd.read_csv(file_path)

print(f"Nombre total de lignes chargées : {len(df)}")

# --- NETTOYAGE CIBLÉ ---
# Liste des colonnes critiques qui ne DOIVENT PAS être vides
colonnes_critiques = [
    'Accident_Severity',      # Indispensable pour l'équilibrage
    'Road_Surface_Conditions', 
    'Road_Type', 
    'Time', 
    'Weather_Conditions'

]

# On supprime les lignes qui ont un "NaN" (vide) dans l'une de ces colonnes
df_clean = df.dropna(subset=colonnes_critiques).copy()

lignes_supprimees = len(df) - len(df_clean)
print(f"Lignes supprimées (données manquantes dans les colonnes critiques) : {lignes_supprimees}")
print(f"Lignes restantes pour l'échantillonnage : {len(df_clean)}")
# -----------------------

# 2. Configuration de l'échantillonnage
nbr_echantillon_fatal = 3000
target_col = 'Accident_Severity'
total_target = 3 * nbr_echantillon_fatal 
unique_classes = df_clean[target_col].nunique() 
samples_per_class = total_target // unique_classes 

print(f"\nCible par classe : {samples_per_class} enregistrements")

# 3. Échantillonnage équilibré
# On utilise df_clean (le dataset nettoyé)
df_sample = df_clean.groupby(target_col, group_keys=False).apply(
    lambda x: x.sample(n=min(len(x), samples_per_class), random_state=42)
)

# Mélange final
df_sample = df_sample.sample(frac=1, random_state=42).reset_index(drop=True)

# 4. Résultats
print("\n--- Répartition finale ---")
print(df_sample[target_col].value_counts())
print(f"Taille totale : {len(df_sample)}")

# 5. Sauvegarde
#Je n'ai pas activé la sauvegarde automatique pour éviter d'écraser des fichiers existants sans confirmation

#output_name = f'sample_balanced_{len(df_sample)}.csv'
#df_sample.to_csv(output_name, index=False)
#print(f"Fichier '{output_name}' généré.")



#----------------------------------------------
#Création d'un nouveau fichier csv ne contenant pas les valeurs d'échantillonage équilibré de "sample_balanced_9000.csv"
#Cela sera utile pour l'apprentissage par la suite. 
import pandas as pd

# 1. Chargement
df_full = pd.read_csv("Output_road_accident_data.csv")
df_sample = pd.read_csv("sample_balanced_9000.csv")

print("-------------------------")
print("Suppression des lignes d'échantillonage équilibré du dataset complet")
print(f"Total avant : {len(df_full)}")
print(f"A retirer : {len(df_sample)}")

# 2. La méthode "Merge avec Indicateur"
# On fusionne les deux tables sur TOUTES les colonnes pour trouver les lignes exactes
# indicator=True crée une colonne '_merge' qui dit si la ligne est dans 'left_only', 'right_only' ou 'both'
df_merged = df_full.merge(df_sample, how='left', indicator=True)

# 3. On ne garde que ce qui est "left_only" (présent dans full, mais PAS dans sample)
df_remaining = df_merged[df_merged['_merge'] == 'left_only']

# On nettoie la colonne temporaire
df_remaining = df_remaining.drop(columns=['_merge'])

# 4. Vérification
print(f"Reste : {len(df_remaining)}")
diff = len(df_full) - len(df_remaining)
print(f"Lignes supprimées réellement : {diff}")

if diff == len(df_sample):
    print("Le compte est bon ! Exactement 9000 lignes supprimées.")
else:
    print(f"Toujours une différence de {diff - len(df_sample)} lignes. (Peut être dû à des doublons parfaits dans les données brutes)")

# 5. Sauvegarde
df_remaining.to_csv("Output_road_accident_data_TEST_SET.csv", index=False)