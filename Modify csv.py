import pandas as pd 

df = pd.read_csv('Road Accident Data.csv')

#~ prend la négation ceux qui ne respecte pas le format HH:MM
#isna() retourne True pour les valeurs non convertibles en datetime
invalid_time_mask = ~pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').isna()
#print(df[invalid_time_mask]) # rien n'est affiché, toutes les valeurs sont valides

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
print(df[['Time','Time_cat','Num_Time']].head())

#df.to_csv('Append_Time_cat_Road_Accident_Data.csv', index=False)

#calcul de boxlpots a titre indicatif

def calcul_boxplot():



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

    print(lower_bound_latitude,Q1_latitude, Q3_latitude, upper_bound_latitude)
    print(df['Latitude'].min(),df['Latitude'].max())

# regroupement des valeurs aberrantes dans des catégories NaN aussi Autre 

#créer indice accident severity
numeric_mask ={
    'Slight' :1.0,
    'Serious' :2.0,
    'Fatal' :3.0
}

df['severity_numeric'] = df['Accident_Severity'].replace(numeric_mask)

print(df[['severity_numeric','Accident_Severity']].head(5))
df.to_csv('Append_Time_cat_Road_Accident_Data.csv', index=False)