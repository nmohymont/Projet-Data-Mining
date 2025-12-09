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


# --- Accident_Severity ---
mapping = {
    "Slight": 1,
    "Serious": 2,
    "Fatal": 3,
    #"Missing": 4
}

# --- Application du mapping (avec sécurité si colonne manquante) ---
col = "Accident_Severity"
if col not in df.columns:
    print(f"Attention : la colonne '{col}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{col}_numeric"] = df[col].map(mapping).astype("Int64")
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(col) + 1, cols.pop(cols.index(f"{col}_numeric")))
    df = df[cols]


# --- Light_Conditions ---
light_mapping = {
    "Daylight": 1,
    "Darkness - lights lit": 2,
    "Darkness - no lighting": 3,
    "Darkness - lighting unknown": 3,
    "Darkness - lights unlit": 3,
    #"Missing": 4
}
# --- Application du mapping ---
Light = "Light_Conditions"
if Light not in df.columns:
    print(f"Attention : la colonne '{Light}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{Light}_numeric"] = df[Light].map(light_mapping).astype("Int64")
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(Light) + 1, cols.pop(cols.index(f"{Light}_numeric")))
    df = df[cols]


# --- Road_Surface_Conditions ---
road_surface_mapping = {
    "Dry": 1,
    "Wet or damp": 2,
    "Frost or ice": 5,
    "Snow": 4,
    "Flood over 3cm. deep": 3,
    "Missing": 6
}

# --- Application du mapping ---
Road = "Road_Surface_Conditions"
if Road not in df.columns:
    print(f"Attention : la colonne '{Road}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{Road}_numeric"] = df[Road].map(road_surface_mapping).astype("Int64")
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(Road) + 1, cols.pop(cols.index(f"{Road}_numeric")))
    df = df[cols]
    

# --- Time_cat --- 

Time_cat_mapping = {
    "Daytime": 2,
    "Night": 3,
    "Morning": 1,
    "Missing": 4
}

# --- Application du mapping ---
TimeCat = "Time_cat"
if TimeCat not in df.columns:
    print(f"Attention : la colonne '{TimeCat}' n'existe pas dans le CSV.", file=sys.stderr)
else:
    # Créer une nouvelle colonne avec le suffixe _numeric pour éviter de remplacer l'original
    df[f"{TimeCat}_numeric"] = df[TimeCat].map(Time_cat_mapping).astype("Int64")
    # Réorganiser pour placer la colonne numeric juste après l'originale
    cols = list(df.columns)
    cols.insert(cols.index(TimeCat) + 1, cols.pop(cols.index(f"{TimeCat}_numeric")))
    df = df[cols]



# --- Sauvegarde du nouveau CSV ---
#df.to_csv(output_csv, index=False)
#print("")
#print("")
#print("Fichier modifié sauvegardé sous :", output_csv)




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
print(f'Taille  dataset après retrait des speed_limit 10 et 15: {df.shape[0]} lignes, {df.shape[1]} colonnes')


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

###créer des valeurs ordinales numériques pour réussir à faire des corrélations de Spearman et Kendall
numeric_mask ={
    'Slight' :1.0,
    'Serious' :2.0,
    'Fatal' :3.0
}

df['severity_numeric'] = df['Accident_Severity'].replace(numeric_mask)

print(df[['severity_numeric','Accident_Severity']].head(5))

# --- Sauvegarde du CSV final avec toutes les modifications ---
df.to_csv('Append_Time_cat_Road_Accident_Data.csv', index=False)
print("\nFichier sauvegardé : Append_Time_cat_Road_Accident_Data.csv")
