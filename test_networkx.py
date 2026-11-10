import networkx as nx
import matplotlib.pyplot as plt


# Fonctions utilisées par les étapes 3 et 4
def bfs_residual(graph, source, sink, residual):
    """
    Cherche un chemin entre source et sink avec une recherche en largeur.
    La fonction retourne un dictionnaire qui indique le prédécesseur
    de chaque sommet trouvé. Ce dictionnaire permettra ensuite de
    reconstruire le chemin complet.
    """
    # parent mémorise le prédécesseur de chaque sommet visité.
    parent = {source: None}
    # queue contient les sommets qui restent à visiter.
    queue = [source]
    while queue:
        # On prend le premier sommet de la file.
        node = queue.pop(0)
        voisins = graph.successors(node)
        for voisin in voisins:
            arc = (node, voisin)
            sommet_deja_visite = voisin in parent
            if arc in residual:
                capacite_restante = residual[arc]
            else:
                capacite_restante = 0
            arc_utilisable = capacite_restante > 0
            if not sommet_deja_visite and arc_utilisable:
                # L'arc est utilisable : on mémorise d'où vient voisin.
                parent[voisin] = node
                if voisin == sink:
                    return parent
                queue.append(voisin)

    # Aucun chemin disponible n'a permis d'atteindre sink.
    return None


def reconstruct_path(parent, source, sink):
    """
    Reconstruit le chemin à partir du dictionnaire des prédécesseurs.

    Le dictionnaire parent est parcouru à l'envers :
    on part de sink et on remonte jusqu'à source.
    """
    if parent is None:
        return None
    if sink not in parent:
        return None
    # On part de sink et on remonte vers source.
    path = []
    node = sink
    while node != source:
        precedent = parent[node]
        arc = (precedent, node)
        path.append(arc)
        node = precedent
    # Le chemin a été construit à l'envers.
    path.reverse()
    return path


def bottleneck(path, residual):
    """Retourne la plus petite capacité résiduelle du chemin."""
    # Un chemin vide ne possède aucune capacité disponible.
    if len(path) == 0:
        return 0
    # On commence par prendre la capacité du premier arc
    # comme plus petite capacité connue.
    plus_petite_capacite = residual[path[0]]
    for arc in path:
        # On récupère la capacité restante de l'arc actuel.
        capacite = residual[arc]
        # Si elle est plus petite, elle devient la nouvelle référence.
        if capacite < plus_petite_capacite:
            plus_petite_capacite = capacite
    # Cette valeur limite le débit que l'on peut ajouter au chemin.
    return plus_petite_capacite

# ============================================================
# ÉTAPE 1 - Représenter le graphe
# ============================================================
# Pour chaque sommet, on indique ses arcs sortants
# et la capacité de chaque arc.
graph_data = {
    "DC-A": [
        {"to":"R1","capacite": 120},
        {"to":"R2","capacite": 100}
    ],
    "R1": [
        {"to":"R3","capacite": 70},
        {"to":"Zone-X","capacite": 40}
    ],
    "R2": [
        {"to":"R3","capacite": 90},
        {"to":"Zone-X","capacite": 30}
    ],
    "R3": [
        {"to":"Zone-X","capacite": 140}
    ]
}
# Création du graphe orienté NetworkX.
G = nx.DiGraph()

# Ajout de chaque arc dans le graphe.
for source, targets in graph_data.items():
    for target in targets:
        # On ajoute l'arête avec sa source, sa destination et sa capacité
        G.add_edge(source, target["to"], capacite=target["capacite"])

# ============================================================
# ÉTAPE 2 - Écrire et vérifier les règles d'un flot valide
# ============================================================
# Débit f(u, v) envoyé sur chaque arc (u, v).
# Ces valeurs servent de point de départ avant les augmentations.
debits = {
    ("DC-A", "R1"): 70,
    ("DC-A", "R2"): 50,
    ("R1", "R3"): 30,
    ("R1", "Zone-X"): 40,
    ("R2", "R3"): 20,
    ("R2", "Zone-X"): 30,
    ("R3", "Zone-X"): 50,
}

# Règle (i) : le débit d'un arc ne doit jamais dépasser sa capacité.
print("--- Vérification des capacités ---")
capacites_respectees = True
for (source, cible), debit in debits.items():
    capacite = G[source][cible]["capacite"]
    respecte = 0 <= debit <= capacite
    print(
        f"f({source}, {cible}) = {debit} / capacité = {capacite} : "
        f"{'OK' if respecte else 'NON RESPECTÉE'}"
    )
    capacites_respectees = capacites_respectees and respecte

# Règle (ii) : dans un routeur intermédiaire,
# le débit entrant doit être égal au débit sortant.
print("\n--- Vérification de la conservation du débit ---")
conservation_respectee = True
for routeur in ["R1", "R2", "R3"]:
    debit_entrant = 0
    for precedent in G.predecessors(routeur):
        debit_entrant = debit_entrant + debits.get((precedent, routeur), 0)

    debit_sortant = 0
    for suivant in G.successors(routeur):
        debit_sortant = debit_sortant + debits.get((routeur, suivant), 0)

    respecte = debit_entrant == debit_sortant
    print(
        f"{routeur} : entrant = {debit_entrant}, sortant = {debit_sortant} : "
        f"{'OK' if respecte else 'NON RESPECTÉE'}"
    )
    conservation_respectee = conservation_respectee and respecte

print(f"\nRoutage valide : {capacites_respectees and conservation_respectee}")

# ============================================================
# ÉTAPE 3 - Chercher un chemin disponible avec BFS
# ÉTAPE 4 - Augmenter le flot
# ============================================================
# Création du réseau résiduel.
#
# Pour chaque arc, la capacité résiduelle correspond à la capacité
# totale moins le débit qui passe déjà sur cet arc.
residual = {}

for source_arc, cible_arc in G.edges:
    arc = (source_arc, cible_arc)

    capacite_totale = G[source_arc][cible_arc]["capacite"]

    if arc in debits:
        debit_actuel = debits[arc]
    else:
        debit_actuel = 0

    capacite_restante = capacite_totale - debit_actuel
    residual[arc] = capacite_restante

source = "DC-A"
sink = "Zone-X"

# Cette boucle recherche plusieurs chemins successifs.
# Elle s'arrête seulement lorsqu'il n'existe plus de chemin disponible.
numero_chemin = 1

while True:
    print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")

    # BFS cherche un chemin entre source et sink
    # en utilisant uniquement les arcs qui ont encore de la capacité.
    parent = bfs_residual(G, source, sink, residual)

    # On transforme les prédécesseurs en une liste d'arcs.
    path = reconstruct_path(parent, source, sink)

    # Si aucun chemin n'a été trouvé, le travail est terminé.
    if path is None:
        print(f"Aucun chemin résiduel de {source} vers {sink}.")
        break

    print(f"Prédécesseurs : {parent}")
    print(f"Chemin trouvé : {path}")

    # Le goulot d'étranglement est la plus petite capacité
    # encore disponible sur les arcs du chemin.
    quantite_a_ajouter = bottleneck(path, residual)
    print(f"Quantité supplémentaire possible : {quantite_a_ajouter}")

    # On parcourt chaque arc du chemin trouvé.
    for arc in path:
        source_arc = arc[0]
        cible_arc = arc[1]

        # Le débit augmente de la quantité qui peut être ajoutée.
        debits[arc] = debits[arc] + quantite_a_ajouter

        # La capacité résiduelle diminue de la même quantité.
        residual[arc] = residual[arc] - quantite_a_ajouter

        print(
            f"Arc {source_arc} -> {cible_arc} : "
            f"débit = {debits[arc]}, "
            f"capacité restante = {residual[arc]}"
        )

    # On passe au numéro du chemin suivant.
    numero_chemin = numero_chemin + 1

# ============================================================
# ÉTAPE 5 - Valider le flot final
# ============================================================
print("\n--- Débit final sur chaque arc ---")
for arc in debits:
    source_arc = arc[0]
    cible_arc = arc[1]
    print(
        f"f({source_arc}, {cible_arc}) = {debits[arc]} "
        f"/ capacité restante = {residual[arc]}"
    )

# La valeur totale du flot est le débit qui sort de la source.
# Ici, la source est DC-A.
valeur_totale_flot = 0

for cible in G.successors(source):
    arc = (source, cible)
    valeur_totale_flot = valeur_totale_flot + debits[arc]

print("\n--- Bilan final du flot ---")
print(f"Valeur totale du flot : {valeur_totale_flot}")

# Pour chaque arc, on affiche le débit f,
# la capacité c et le rapport f/c.
print("\n--- Débit f / capacité c sur chaque arc ---")

for arc in G.edges:
    source_arc = arc[0]
    cible_arc = arc[1]
    debit = debits[arc]
    capacite = G[source_arc][cible_arc]["capacite"]

    rapport = debit / capacite

    print(
        f"{source_arc} -> {cible_arc} : "
        f"f = {debit}, c = {capacite}, f/c = {rapport:.2f}"
    )

# Un arc est saturé lorsque son débit est égal à sa capacité.
print("\n--- Arcs saturés ---")
arc_sature_trouve = False

for arc in G.edges:
    source_arc = arc[0]
    cible_arc = arc[1]
    debit = debits[arc]
    capacite = G[source_arc][cible_arc]["capacite"]

    if debit == capacite:
        print(f"{source_arc} -> {cible_arc}")
        arc_sature_trouve = True

if not arc_sature_trouve:
    print("Aucun arc saturé.")

# Vérification manuelle de la contrainte de capacité.
print("\n--- Vérification finale des capacités ---")
capacites_finales_respectees = True

for arc in G.edges:
    source_arc = arc[0]
    cible_arc = arc[1]
    debit = debits[arc]
    capacite = G[source_arc][cible_arc]["capacite"]

    if debit >= 0 and debit <= capacite:
        print(f"{source_arc} -> {cible_arc} : OK")
    else:
        print(f"{source_arc} -> {cible_arc} : NON RESPECTÉE")
        capacites_finales_respectees = False

# Vérification manuelle de la conservation du débit.
# Pour chaque routeur intermédiaire, le débit entrant
# doit être égal au débit sortant.
print("\n--- Vérification finale de la conservation ---")
conservation_finale_respectee = True

for routeur in ["R1", "R2", "R3"]:
    debit_entrant = 0

    for precedent in G.predecessors(routeur):
        arc_entrant = (precedent, routeur)
        debit_entrant = debit_entrant + debits[arc_entrant]

    debit_sortant = 0

    for suivant in G.successors(routeur):
        arc_sortant = (routeur, suivant)
        debit_sortant = debit_sortant + debits[arc_sortant]

    if debit_entrant == debit_sortant:
        print(
            f"{routeur} : entrant = {debit_entrant}, "
            f"sortant = {debit_sortant} : OK"
        )
    else:
        print(
            f"{routeur} : entrant = {debit_entrant}, "
            f"sortant = {debit_sortant} : NON RESPECTÉE"
        )
        conservation_finale_respectee = False

print("\n--- Résultat des vérifications finales ---")
print(f"Contraintes de capacité respectées : {capacites_finales_respectees}")
print(f"Conservation respectée : {conservation_finale_respectee}")

# Vérification visuelle du graphe de l'Étape 1.
pos = {
    'DC-A': (0, 1),    
    'R1': (1, 2),      
    'R2': (1, 0),      
    'R3': (2, 1),      
    'Zone-X': (3, 1)   
}

nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_color='lightblue', 
    node_size=2500, 
    font_weight='bold', 
    arrowsize=20
)
edge_labels = nx.get_edge_attributes(G, 'capacite')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.show()
