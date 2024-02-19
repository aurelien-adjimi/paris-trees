import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime

path = 'travaux_arbres.csv'

df = pd.read_csv(path, sep=";")
# print(df)

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Fonction pour trouver l'itinéraire utilisant l'heuristique du plus proche voisin
def closer_neighbor_path(departure, points):
    itinerary = [departure]
    remaining_points = points.copy()
    current_point = departure
    
    while remaining_points:
        # Trouver le point le plus proche
        closer = min(remaining_points, key=lambda x: euclidean_distance(current_point, x))
        remaining_points.remove(closer)
        itinerary.append(closer)
        current_point = closer
    
    return itinerary

city_hall = [48.87118967150428, 2.3473884741729503]

df['Type_travaux'] = df['Type_travaux'].replace(['Taille PR', 'Taille R', 'Elagage'], 'Taille & Elagage')

works_type = df['Type_travaux']

coord_by_type = {work_type: [] for work_type in works_type}

for work_type in works_type:
    df_filtered = df[df['Type_travaux'] == work_type]
    coord_by_type[work_type] = list(zip(df_filtered['latitude'], df_filtered['longitude']))


colors_by_type = {
    'Plantation': 'red',
    'Abattage': 'blue',
    'Taille & Elagage': 'green' 
}

# plt.figure(figsize=(10, 6))

# for work_type, coordinates in coord_by_type.items():
#     if work_type in colors_by_type:
#         latitudes, longitudes = zip(*coordinates)
#         plt.scatter(longitudes, latitudes, color=colors_by_type[work_type], label=work_type, alpha=0.7)
# plt.scatter(city_hall[1], city_hall[0], color='black', label='Mairie', s=100, marker='*')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Répartition des travaux par type')
# plt.legend()
# plt.show()

city_hall_coord = (48.87118967150428, 2.3473884741729503)

# for work_type, points in coord_by_type.items():
#     teams_itineraries = closer_neighbor_path(city_hall_coord, points)
    
#     plt.figure(figsize=(10, 6))

#     for idx, point in enumerate(teams_itineraries, start=1):
#         plt.text(point[1], point[0], str(idx), color=colors_by_type[work_type], fontsize=5, ha='center', va='center')

#     plt.ylim(48.725, 48.900)
    
#     plt.scatter([], [], color=colors_by_type[work_type], label=work_type)  # Astuce pour afficher la légende avec la couleur correcte
#     plt.scatter(city_hall_coord[1], city_hall_coord[0], color='black', label='Mairie', s=100, marker='*')
#     plt.xlabel('Longitude')
#     plt.ylabel('Latitude')
#     plt.title(f'Itinéraire pour l\'équipe {work_type}')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# Calcul du temps en minutes pour la plage d'intervention
date_start = datetime.strptime("29/01/2024 08:00", "%d/%m/%Y %H:%M")
date_end = datetime.strptime("09/02/2024 17:00", "%d/%m/%Y %H:%M")

difference = (date_end - date_start).total_seconds() / 60

print(f"Les équipes ont un temps de travail théorique de {difference} minutes")


# Calcul du temps de travail moyen par équipe
total_time_by_team = {}

for work_type in works_type.unique():
    df_team = df[df['Type_travaux'] == work_type]
    
    total_time = (df_team['nb_arbres'] * df_team['tps_par_arbre']).sum()
    
    total_time_by_team[work_type] = total_time

for equipe, temps in total_time_by_team.items():
    print(f"L'équipe {equipe} doit travailler {temps} minutes pour terminer sa tournée.")