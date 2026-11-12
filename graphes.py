"""
Données des graphes étudiés dans les TP de théorie des graphes.
Chaque graphe est représenté par un dictionnaire dont les clés sont les sommets sources,
et les valeurs sont les listes de leurs arcs sortants (avec 'to', 'capacite' et optionnellement 'enabled').
"""

# ============================================================
# Graphes du TP1
# ============================================================

# Graphe de départ (Étape 1 et 2 du TP1)
graph_data_etape1 = {
    "DC-A": [
        {"to": "R1", "capacite": 120},
        {"to": "R2", "capacite": 100}
    ],
    "R1": [
        {"to": "R3", "capacite": 70},
        {"to": "Zone-X", "capacite": 40}
    ],
    "R2": [
        {"to": "R3", "capacite": 90},
        {"to": "Zone-X", "capacite": 30}
    ],
    "R3": [
        {"to": "Zone-X", "capacite": 140}
    ]
}

# Graphe complet du TP1 (Partie C)
graph_data_C = {
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

# Variantes de réflexion TP1 (Étape 6)
graph_data_C_add100_REItoEST = {
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

graph_data_C_add100_ROUtoREI = {
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
# Graphes du TP3
# ============================================================

# Graphe de base TP3
graph_data = {
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

# TP3 : Graphe avec liaison R1-R3 désactivée
graph_data_R1R3disable = {
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

# TP3 : Graphe avec liaison R3-Clients désactivée
graph_data_R3Clidisable = {
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

# TP3 : Réseau multi-datacenters et multi-zones (Partie D)
graph_data_datacenter = {
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
