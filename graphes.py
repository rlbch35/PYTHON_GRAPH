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


# Panne du Datacenter principal DC-PARIS (toutes ses arêtes entrantes et sortantes désactivées)
graph_data_TP3_datacenter_DCPARIS_disable = {
    "S*": [
        {"to": "DC-LILLE", "capacite": 350, "enabled": True},
        {"to": "DC-PARIS", "capacite": 500, "enabled": False},
        {"to": "DC-LYON", "capacite": 420, "enabled": True}
    ],
    "DC-LILLE": [
        {"to": "LIL", "capacite": 350, "enabled": True}
    ],
    "DC-PARIS": [
        {"to": "PAR", "capacite": 500, "enabled": False}
    ],
    "DC-LYON": [
        {"to": "LYO", "capacite": 420, "enabled": True}
    ],
    "LIL": [
        {"to": "REI", "capacite": 240, "enabled": True},
        {"to": "PAR", "capacite": 180, "enabled": True}
    ],
    "PAR": [
        {"to": "REI", "capacite": 320, "enabled": True},
        {"to": "STR", "capacite": 260, "enabled": True},
        {"to": "LYO", "capacite": 230, "enabled": True}
    ],
    "LYO": [
        {"to": "STR", "capacite": 230, "enabled": True}
    ],
    "REI": [
        {"to": "NORD", "capacite": 250, "enabled": True},
        {"to": "IDF", "capacite": 350, "enabled": True}
    ],
    "STR": [
        {"to": "Sud-Est", "capacite": 350, "enabled": True},
        {"to": "IDF", "capacite": 180, "enabled": True}
    ],
    "NORD": [
        {"to": "T*", "capacite": 250, "enabled": True}
    ],
    "IDF": [
        {"to": "T*", "capacite": 530, "enabled": True}
    ],
    "Sud-Est": [
        {"to": "T*", "capacite": 350, "enabled": True}
    ]
}

