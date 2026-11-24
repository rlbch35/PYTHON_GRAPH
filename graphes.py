#### ============================================================
#### FICHIER DÉDIÉ AUX GRAPHES (TP1 & TP3)
#### ============================================================

# ============================================================
# GRAPHES POUR LE TP1
# ============================================================

# Structure du graphe pour la PARTIE C
graph_data_TP1 = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 420},
        {"to": "DC-PARIS", "capacite": 650}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350},
        {"to": "ROU", "capacite": 220}
    ],
    "DC-PARIS": [
        {"to": "ROU", "capacite": 250},
        {"to": "PAR", "capacite": 500}
    ],
    "LIL": [
        {"to": "NORD-250", "capacite": 160},
        {"to": "ROU", "capacite": 240}
    ],
    "PAR": [
        {"to": "IDF-430", "capacite": 400},
        {"to": "REI", "capacite": 320}
    ],
    "ROU": [
        {"to": "PAR", "capacite": 280},
        {"to": "REI", "capacite": 180}
    ],
    "REI": [
        {"to": "IDF-430", "capacite": 100},
        {"to": "EST-280", "capacite": 260}
    ],
    "NORD-250": [
        {"to": "T*", "capacite": 250}
    ],
    "IDF-430": [
        {"to": "T*", "capacite": 430}
    ],
    "EST-280": [
        {"to": "T*", "capacite": 280}
    ]
}

pos_TP1 = {
    'S*': (0, 1),    
    'DC-LILLE': (2, 2),      
    'DC-PARIS': (2, 0),      
    'LIL': (4, 2),    
    'ROU': (4, 1),      
    'PAR': (6, 1),
    'REI': (6, 0),
    'NORD-250': (8, 2),      
    'IDF-430': (8, 1),
    'EST-280': (8, 0),
    'T*': (10, 1) 
}
# ÉTAPE 6 : Scénario réflexion (+100 sur REI -> EST)
graph_data_TP1_add100_REItoEST = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 420},
        {"to": "DC-PARIS", "capacite": 650}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350},
        {"to": "ROU", "capacite": 220}
    ],
    "DC-PARIS": [
        {"to": "ROU", "capacite": 250},
        {"to": "PAR", "capacite": 500}
    ],
    "LIL": [
        {"to": "NORD-250", "capacite": 160},
        {"to": "ROU", "capacite": 240}
    ],
    "PAR": [
        {"to": "IDF-430", "capacite": 400},
        {"to": "REI", "capacite": 320}
    ],
    "ROU": [
        {"to": "PAR", "capacite": 280},
        {"to": "REI", "capacite": 180}
    ],
    "REI": [
        {"to": "IDF-430", "capacite": 100},
        {"to": "EST-280", "capacite": 360}
    ],
    "NORD-250": [
        {"to": "T*", "capacite": 250}
    ],
    "IDF-430": [
        {"to": "T*", "capacite": 430}
    ],
    "EST-280": [
        {"to": "T*", "capacite": 280}
    ]
}

# ÉTAPE 6 : Scénario réflexion (+100 sur ROU -> REI)
graph_data_TP1_add100_ROUtoREI = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 420},
        {"to": "DC-PARIS", "capacite": 650}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350},
        {"to": "ROU", "capacite": 220}
    ],
    "DC-PARIS": [
        {"to": "ROU", "capacite": 250},
        {"to": "PAR", "capacite": 500}
    ],
    "LIL": [
        {"to": "NORD-250", "capacite": 160},
        {"to": "ROU", "capacite": 240}
    ],
    "PAR": [
        {"to": "IDF-430", "capacite": 400},
        {"to": "REI", "capacite": 320}
    ],
    "ROU": [
        {"to": "PAR", "capacite": 280},
        {"to": "REI", "capacite": 280}
    ],
    "REI": [
        {"to": "IDF-430", "capacite": 100},
        {"to": "EST-280", "capacite": 260}
    ],
    "NORD-250": [
        {"to": "T*", "capacite": 250}
    ],
    "IDF-430": [
        {"to": "T*", "capacite": 430}
    ],
    "EST-280": [
        {"to": "T*", "capacite": 280}
    ]
}


# ============================================================
# GRAPHES POUR LE TP2
# ============================================================
# Structure du graphe

graph_data_TP2 = {
    "S*": [
        {"to": "DC-A", "capacite": 200, "latence": 0},
        {"to": "DC-B", "capacite": 250, "latence": 0}
    ],
    "DC-A": [
        {"to": "R1", "capacite": 200, "latence": 5}
    ],
    "DC-B": [
        {"to": "R2", "capacite": 250, "latence": 7}
    ],
    "R1": [
        {"to": "R3", "capacite": 160, "latence": 6},
        {"to": "LIVE", "capacite": 100, "latence": 18}
    ],
    "R2": [
        {"to": "R3", "capacite": 220, "latence": 12},
        {"to": "BACKUP", "capacite": 100, "latence": 25}
    ],
    "R3": [
        {"to": "LIVE", "capacite": 220, "latence": 8},
        {"to": "BACKUP", "capacite": 250, "latence": 10}
    ],
    "LIVE": [
        {"to": "T*", "capacite": 220, "latence": 0}
    ],
    "BACKUP": [
        {"to": "T*", "capacite": 200, "latence": 0}
    ]
}

graph_data_TP2_ajout_latenceR1 = {
    "S*": [
        {"to": "DC-A", "capacite": 200, "latence": 0},
        {"to": "DC-B", "capacite": 250, "latence": 0}
    ],
    "DC-A": [
        {"to": "R1", "capacite": 200, "latence": 5}
    ],
    "DC-B": [
        {"to": "R2", "capacite": 250, "latence": 7}
    ],
    "R1": [
        {"to": "R3", "capacite": 160, "latence": 32},
        {"to": "LIVE", "capacite": 100, "latence": 18}
    ],
    "R2": [
        {"to": "R3", "capacite": 220, "latence": 12},
        {"to": "BACKUP", "capacite": 100, "latence": 25}
    ],
    "R3": [
        {"to": "LIVE", "capacite": 220, "latence": 8},
        {"to": "BACKUP", "capacite": 250, "latence": 10}
    ],
    "LIVE": [
        {"to": "T*", "capacite": 220, "latence": 0}
    ],
    "BACKUP": [
        {"to": "T*", "capacite": 200, "latence": 0}
    ]
}
# Positionnement du graphe pour l'affichage Matplotlib
pos_TP2 = {
    'S*': (-2, 1),
    'DC-A': (0, 2),
    'DC-B': (0, 0),
    'R1': (4, 2),
    'R2': (4, 0),
    'R3': (6, 1),
    'LIVE': (8, 2),
    'BACKUP': (8, 0),
    'T*': (10, 1),
}



graph_data_TP2cout = {
    "S*": [
        {"to": "DC-A", "capacite": 200, "latence": 0,'cout':0},
        {"to": "DC-B", "capacite": 250, "latence": 0,'cout':0}
    ],
    "DC-A": [
        {"to": "R1", "capacite": 200, "latence": 5,'cout':3}
    ],
    "DC-B": [
        {"to": "R2", "capacite": 250, "latence": 7,'cout':1}
    ],
    "R1": [
        {"to": "R3", "capacite": 160, "latence": 6,'cout':1},
        {"to": "LIVE", "capacite": 100, "latence": 18,'cout':1}
    ],
    "R2": [
        {"to": "R3", "capacite": 220, "latence": 12,'cout':1},
        {"to": "BACKUP", "capacite": 100, "latence": 25,'cout':3}
    ],
    "R3": [
        {"to": "LIVE", "capacite": 220, "latence": 8,'cout':1},
        {"to": "BACKUP", "capacite": 250, "latence": 10,'cout':3}
    ],
    "LIVE": [
        {"to": "T*", "capacite": 220, "latence": 0,'cout':0}
    ],
    "BACKUP": [
        {"to": "T*", "capacite": 200, "latence": 0,'cout':0}
    ]
}


# Graphe simple initial de démonstration TP3
graph_data_TP3 = {
    "DC": [
        {"to": "R1", "capacite": 180},
        {"to": "R2", "capacite": 180}
    ],
    "R1": [
        {"to": "R3", "capacite": 140},
        {"to": "R4", "capacite": 80}
    ],
    "R2": [
        {"to": "R3", "capacite": 80},
        {"to": "R4", "capacite": 140}
    ],
    "R3": [
        {"to": "Clients", "capacite": 160}
    ],
    "R4": [
        {"to": "Clients", "capacite": 160}
    ]
}

# Débits initiaux pour TP3
debits_TP3 = {
    ("DC", "R1"): 70,
    ("DC", "R2"): 50,
    ("R1", "R3"): 30,
    ("R1", "R5"): 40,
    ("R2", "R3"): 20,
    ("R2", "R4"): 30,
    ("R3", "Clients"): 50,
    ("R4", "Clients"): 50
}

# Graphe TP3 avec l'arc R1 -> R3 désactivé
graph_data_TP3_R1R3disable = {
    "DC": [
        {"to": "R1", "capacite": 180, "enabled": True},
        {"to": "R2", "capacite": 180, "enabled": True}
    ],
    "R1": [
        {"to": "R3", "capacite": 140, "enabled": False},
        {"to": "R4", "capacite": 80, "enabled": True}
    ],
    "R2": [
        {"to": "R3", "capacite": 80, "enabled": True},
        {"to": "R4", "capacite": 140, "enabled": True}
    ],
    "R3": [
        {"to": "Clients", "capacite": 160, "enabled": True}
    ],
    "R4": [
        {"to": "Clients", "capacite": 160, "enabled": True}
    ]
}

# Graphe TP3 avec l'arc R3 -> Clients désactivé
graph_data_TP3_R3Clidisable = {
    "DC": [
        {"to": "R1", "capacite": 180, "enabled": True},
        {"to": "R2", "capacite": 180, "enabled": True}
    ],
    "R1": [
        {"to": "R3", "capacite": 140, "enabled": False},
        {"to": "R4", "capacite": 80, "enabled": True}
    ],
    "R2": [
        {"to": "R3", "capacite": 80, "enabled": True},
        {"to": "R4", "capacite": 140, "enabled": True}
    ],
    "R3": [
        {"to": "Clients", "capacite": 160, "enabled": False}
    ],
    "R4": [
        {"to": "Clients", "capacite": 160, "enabled": True}
    ]
}

# Réseau multi-datacenter complet (Partie D TP3)
graph_data_TP3_datacenter = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 350},
        {"to": "DC-PARIS", "capacite": 500},
        {"to": "DC-LYON", "capacite": 420}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350}
    ],
    "DC-PARIS": [
        {"to": "PAR", "capacite": 500}
    ],
    "DC-LYON": [
        {"to": "LYO", "capacite": 420}
    ],
    "LIL": [
        {"to": "REI", "capacite": 240},
        {"to": "PAR", "capacite": 180}
    ],
    "PAR": [
        {"to": "REI", "capacite": 320},
        {"to": "STR", "capacite": 260},
        {"to": "LYO", "capacite": 230}
    ],
    "LYO": [
        {"to": "STR", "capacite": 230}
    ],
    "REI": [
        {"to": "NORD", "capacite": 250},
        {"to": "IDF", "capacite": 350}
    ],
    "STR": [
        {"to": "Sud-Est", "capacite": 350},
        {"to": "IDF", "capacite": 180}
    ],
    "NORD": [
        {"to": "T*", "capacite": 250}
    ],
    "IDF": [
        {"to": "T*", "capacite": 530}
    ],
    "Sud-Est": [
        {"to": "T*", "capacite": 350}
    ]
}
# StreamFlow-Enterprise complet
graph_data_Streamflow_exemple = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 570},
        {"to": "DC-PARIS", "capacite": 760},
        {"to": "DC-LYON", "capacite": 630}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350, "latence": 2, "cout": 4.5},     # Très rapide mais cher
        {"to": "ROU", "capacite": 220, "latence": 18, "cout": 0.4}     # Lien lent "low-cost"
    ],
    "DC-PARIS": [
        {"to": "ROU", "capacite": 250, "latence": 6, "cout": 2.2},
        {"to": "PAR", "capacite": 500, "latence": 15, "cout": 0.5},    # Gros tuyau économique mais congestionné
        {"to": "REI", "capacite": 260, "latence": 3, "cout": 8.0},     # Fibre dédiée ultra-rapide mais chère
    ],
    "DC-LYON": [
        {"to": "LYO", "capacite": 420, "latence": 4, "cout": 1.5},
        {"to": "STR", "capacite": 210, "latence": 28, "cout": 0.3}     # Chemin direct vers STR très lent et économique
    ],
    "LIL": [
        {"to": "ROU", "capacite": 240, "latence": 3, "cout": 1.2}
    ],
    "ROU": [
        {"to": "PAR", "capacite": 280, "latence": 4, "cout": 3.5}
    ],
    "PAR": [
        {"to": "REI", "capacite": 320, "latence": 5, "cout": 1.1},
        {"to": "T*", "capacite": 650, "latence": 2, "cout": 7.5}       # Sortie 1 : Ultra-rapide mais très coûteuse
    ],
    "REI": [
        {"to": "LYO", "capacite": 260, "latence": 22, "cout": 0.6},
        {"to": "STR", "capacite": 190, "latence": 4, "cout": 6.5}
    ],
    "LYO": [
        {"to": "STR", "capacite": 230, "latence": 6, "cout": 1.8},
        {"to": "T*", "capacite": 700, "latence": 14, "cout": 0.8}      # Sortie 2 : Gros débit pas cher mais latence moyenne
    ],
    "STR": [
        {"to": "T*", "capacite": 610, "latence": 7, "cout": 2.5}       # Sortie 3 : Équilibrée
    ]
}

graph_data_Streamflow = {

"S*": [

{"to": "DC-LILLE", "capacite": 570},

{"to": "DC-PARIS", "capacite": 760},

{"to": "DC-LYON", "capacite": 630}

],

"DC-LILLE": [

{"to": "LIL", "capacite": 350,"latence":4,"cout":1},

{"to": "ROU", "capacite": 220,"latence":6,"cout":1.1}

],

"DC-PARIS": [

{"to": "ROU", "capacite": 250,"latence":8,"cout":1.3},

{"to": "PAR", "capacite": 500,"latence":3,"cout":0.9},

{"to": "REI", "capacite": 260,"latence":7,"cout":1.2},

],

"DC-LYON": [

{"to": "LYO", "capacite": 420,"latence":4,"cout":1},

{"to": "STR", "capacite": 210,"latence":9,"cout":210.4}

],

"LIL": [

{"to": "ROU", "capacite": 240,"latence":5,"cout":0.8}

],

"ROU": [

{"to": "PAR", "capacite": 280,"latence":7,"cout":0.9}

],

"PAR": [

{"to": "REI", "capacite": 320,"latence":6,"cout":0.8}

],

"REI": [

{"to": "LYO", "capacite": 260,"latence":10,"cout":1.1},

{"to": "STR", "capacite": 190,"latence":7,"cout":1}

],

"LYO": [

{"to": "STR", "capacite": 230,"latence":8,"cout":0.9}

],

"STR": [

{"to": "T*", "capacite": 1960}

]

} 
pos_Streamflow = {
    'S*':       (0, 7),
    
    # On passe de x=0 à x=8 pour que "0/760/0ms" tienne largement entre S* et DC-PARIS
    'DC-LILLE': (8, 13),
    'DC-PARIS': (8, 7),
    'DC-LYON':  (8, 1),
    
    # Cascade diagonale bien espacée
    'LIL':      (14, 15),
    'ROU':      (19, 11.5),
    'PAR':      (24, 8),
    'REI':      (29, 4.5),
    'LYO':      (34, 1),
    
    # On passe de x=40 à x=48 pour que "0/1960/0ms" tienne largement entre STR et T*
    'STR':      (40, 4),
    'T*':       (48, 4),
}