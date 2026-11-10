import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# Structure du graphe
graph_data = {
    "S*": [
            {"to":"DC-LILLE","capacite": 420},
            {"to":"DC-PARIS","capacite": 650}
        ],
    "DC-LILLE": [
            {"to":"LIL","capacite": 350},
            {"to":"ROU","capacite": 220}
    ],
    "DC-PARIS": [
            {"to":"ROU","capacite": 250},
            {"to":"PAR","capacite": 500}
        ],
    "LIL": [
            {"to":"NORD-250","capacite": 160},
            {"to":"ROU","capacite": 240}
    ],
    "PAR": [
            {"to":"IDF-430","capacite": 400},
            {"to":"REI","capacite": 320}
    ],
    "ROU": [
            {"to":"PAR","capacite": 280},
            {"to":"REI","capacite": 180}
    ],
    "REI": [
            {"to":"IDF-430","capacite": 100},
            {"to":"EST-280","capacite": 260}
    ],
    "NORD-250": [
            {"to":"T*","capacite": 250}
        ],
    "IDF-430": [
            {"to":"T*","capacite": 430}
        ],
    "EST-280": [
            {"to":"T*","capacite": 280}
        ]
}

# Fonctions utilisées par les étapes 3 et 4
def bfs_residual(graph, source, sink, residual):
    """
    Cherche un chemin entre source et sink avec une recherche en largeur.
    """
    parent = {source: None}
    queue = [source]
    while queue:
        node = queue.pop(0)
        voisins = graph.successors(node)
        for voisin in voisins:
            arc = (node, voisin)
            sommet_deja_visite = voisin in parent
            capacite_restante = residual.get(arc, 0)
            arc_utilisable = capacite_restante > 0
            if not sommet_deja_visite and arc_utilisable:
                parent[voisin] = node
                if voisin == sink:
                    return parent
                queue.append(voisin)
    return None


def reconstruct_path(parent, source, sink):
    """Reconstruit le chemin à partir du dictionnaire des prédécesseurs."""
    if parent is None or sink not in parent:
        return None
    path = []
    node = sink
    while node != source:
        precedent = parent[node]
        arc = (precedent, node)
        path.append(arc)
        node = precedent
    path.reverse()
    return path


def bottleneck(path, residual):
    """Retourne la plus petite capacité résiduelle du chemin."""
    if not path:
        return 0
    plus_petite_capacite = residual[path[0]]
    for arc in path:
        capacite = residual[arc]
        if capacite < plus_petite_capacite:
            plus_petite_capacite = capacite
    return plus_petite_capacite

# ============================================================
# ÉTAPE 1 - Représenter le graphe
# ============================================================
G = nx.DiGraph()

for source, targets in graph_data.items():
    for target in targets:
        G.add_edge(source, target["to"], capacite=target["capacite"])

# ============================================================
# ÉTAPE 2 - Écrire et vérifier les règles d'un flot valide
# ============================================================
# Initialisation dynamique de tous les débits à 0
debits = {edge: 0 for edge in G.edges}

# ============================================================
# ÉTAPE 3 - Chercher un chemin disponible avec BFS
# ÉTAPE 4 - Augmenter le flot
# ============================================================
sources = [sommet for sommet in G.nodes if G.in_degree(sommet) == 0]
sinks = [sommet for sommet in G.nodes if G.out_degree(sommet) == 0]

if len(sources) != 1 or len(sinks) != 1:
    raise ValueError("Le graphe doit contenir exactement 1 source et 1 puits.")

source = sources[0]
sink = sinks[0]

# Création du réseau résiduel initial
residual = {}
for source_arc, cible_arc in G.edges:
    arc = (source_arc, cible_arc)
    capacite_totale = G[source_arc][cible_arc]["capacite"]
    residual[arc] = capacite_totale - debits[arc]

numero_chemin = 1

while True:
    print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")

    parent = bfs_residual(G, source, sink, residual)
    path = reconstruct_path(parent, source, sink)

    if path is None:
        print(f"Aucun chemin résiduel de {source} vers {sink}.")
        break

    print(f"Prédécesseurs : {parent}")
    print(f"Chemin trouvé : {path}")

    quantite_a_ajouter = bottleneck(path, residual)
    print(f"Quantité supplémentaire possible : {quantite_a_ajouter}")

    for arc in path:
        debits[arc] += quantite_a_ajouter
        residual[arc] -= quantite_a_ajouter

        print(
            f"Arc {arc[0]} -> {arc[1]} : "
            f"débit = {debits[arc]}, "
            f"capacité restante = {residual[arc]}"
        )

    numero_chemin += 1

# ============================================================
# ÉTAPE 5 - Valider le flot final
# ============================================================
print("\n--- Débit final sur chaque arc ---")
for arc in debits:
    print(f"f({arc[0]}, {arc[1]}) = {debits[arc]} / capacité restante = {residual[arc]}")

valeur_totale_flot = sum(debits[(source, cible)] for cible in G.successors(source))

print("\n--- Bilan final du flot ---")
print(f"Valeur totale du flot : {valeur_totale_flot}")

print("\n--- Débit f / capacité c sur chaque arc ---")
for arc in G.edges:
    debit = debits[arc]
    capacite = G[arc[0]][arc[1]]["capacite"]
    rapport = debit / capacite
    print(f"{arc[0]} -> {arc[1]} : f = {debit}, c = {capacite}, f/c = {rapport:.2f}")

# Visualisation du graphe
pos = {
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

plt.figure(figsize=(10, 6))
edge_colors = ['red' if debits[edge] == G[edge[0]][edge[1]]['capacite'] else 'gray' for edge in G.edges]
edge_widths = [3.0 if debits[edge] == G[edge[0]][edge[1]]['capacite'] else 1.2 for edge in G.edges]

nx.draw(
    G, pos, with_labels=True, node_color='lightblue', 
    node_size=2500, font_weight='bold', arrowsize=20,
    edge_color=edge_colors, width=edge_widths
)
edge_labels = {edge: f"{debits[edge]}/{G[edge[0]][edge[1]]['capacite']}" for edge in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='darkblue')
plt.title("Flot final dans le réseau (Arcs saturés en rouge)")
plt.show()