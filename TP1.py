from asyncio import graph

import networkx as nx
import matplotlib.pyplot as plt


#### LES GRAPHES
graph_data_etape1 = {
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

# Structure du graphe
graph_data_C = {
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

#=============== ETAPE 6 reflexion ====================
graph_data_C_add100_REItoEST= {
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
            {"to":"EST-280","capacite": 360}
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


graph_data_C_add100_ROUtoREI = {
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
            {"to":"REI","capacite": 280}
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

# Conclusion PARTIE D  Pour augmenter la valeur du flot maximal, il faut augmenter la valeur d'un arc de la coupe
#=================================================================

# ============================================================
# ÉTAPE 1 - Représenter le graphe
# ============================================================
# Pour chaque sommet, on indique ses arcs sortants
# et la capacité de chaque arc.

def etape1et2(graph):

    # Création du graphe orienté NetworkX.
    G = nx.DiGraph()

    # Ajout de chaque arc dans le graphe.
    for source, targets in graph.items():
        for target in targets:
            # On ajoute l'arête avec sa source, sa destination et sa capacité
            G.add_edge(source, target["to"], capacite=target["capacite"])

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
    plt.show(block=False)
    plt.pause(0.1)

    # ============================================================
    # ÉTAPE 2 - Écrire et vérifier les règles d'un flot valide
    # ============================================================
    # Débit f(u, v) envoyé sur chaque arc (u, v).
    # Ces valeurs servent de point de départ avant les augmentations.

    #Simulation d'un flot valide sur le graphe pour tester les règles de flot valide graphe residuel
    debits = {
        ("DC-A", "R1"): 70,
        ("DC-A", "R2"): 50,
        ("R1", "R3"): 30,
        ("R1", "Zone-X"): 40,
        ("R2", "R3"): 20,
        ("R2", "Zone-X"): 30,
        ("R3", "Zone-X"): 50,
    }

    # Règle (i) version 1: le débit d'un arc ne doit jamais dépasser sa capacité. 
    print("--- Vérification des capacités ---")
    capacites_respectees = True
    for (source, cible), debit in debits.items():
        capacite = G[source][cible]["capacite"]
        respecte = 0 <= debit <= capacite # on vérifie que 0 ≤ f(u, v) ≤ c(u, v)
        print(
            f"f({source}, {cible}) = {debit} / capacité = {capacite} : "
            f"{'OK' if respecte else 'NON RESPECTÉE'}"
        )
        capacites_respectees = capacites_respectees and respecte

    # Règle (ii) version 1 : dans un routeur intermédiaire,
    # le débit entrant doit être égal au débit sortant. 
    print("\n--- Vérification de la conservation du débit pour R1, R2 et R3 ---")
    conservation_respectee = True
    for routeur in ["R1", "R2", "R3"]:
        debit_entrant = 0
        for precedent in G.predecessors(routeur):
            debit_entrant = debit_entrant + debits.get((precedent, routeur), 0)

        debit_sortant = 0
        for suivant in G.successors(routeur):
            debit_sortant = debit_sortant + debits.get((routeur, suivant), 0)

        respecte = debit_entrant == debit_sortant # on vérifie que somme des débits entrants = somme des débits sortants pour le noeud courant
        print(
            f"{routeur} : entrant = {debit_entrant}, sortant = {debit_sortant} : "
            f"{'OK' if respecte else 'NON RESPECTÉE'}"
        )
        conservation_respectee = conservation_respectee and respecte

    print(f"\nRoutage valide : {capacites_respectees and conservation_respectee}")


## ============================================================
# PARTIE B
## ===========================================================

GraphData = dict[str, list[dict[str, int | str]]]
Flow = dict[tuple[str, str], int]
Residual = dict[tuple[str, str], int]

def verifier_flot(graphe, debits, sourceNode, arriveeNode):
    """Vérification contraintes capacités version 2 """
    capacites_respectees = True # on initialise la variable à True, on va la mettre à False si on trouve un débit qui ne respecte pas les contraintes
    # Aucun débit ne doit être négatif ni dépasser la capacité de son arc. on parcours tous les arcs du graphe et on vérifie que le débit de chaque arc est compris entre 0 et la capacité de l'arc
    for arc in graphe.edges:
        source_arc = arc[0] # on récupère le sommet source de l'arc
        destination_arc = arc[1] # on récupère le sommet destination de l'arc
        debit = debits[arc] # on récupère le débit de l'arc
        capacite = graphe[source_arc][destination_arc]["capacite"] # on récupère la capacité de l'arc dans le graphe en entrée

        # on vérifie que le débit est compris entre 0 et la capacité de l'arc
        if debit < 0 or debit > capacite:
            capacites_respectees = False # on met la variable à False si le débit ne respecte pas les contraintes
            break
    conservation_respectee = True


    """Vérification contraintes conservation version 2 """
    for node in graphe.nodes:
        if node in (sourceNode, arriveeNode): # on ne vérifie pas les sommets source et puits, on ne vérifie que les sommets intermédiaires
            continue

        debit_entrant = 0 # on initialise le débit entrant à 0
        for precedent in graphe.predecessors(node): # on parcourt tous les sommets précédents du sommet courant
            arc_entrant = (precedent, node) # on récupère l'arc entrant du sommet
            debit_entrant += debits[arc_entrant] # on ajoute le débit de l'arc entrant au débit entrant total

        debit_sortant = 0
        for suivant in graphe.successors(node): # on parcourt tous les sommets suivants du sommet courant
            arc_sortant = (node, suivant) # on récupère l'arc sortant du sommet
            debit_sortant += debits[arc_sortant] # on ajoute le débit de l'arc sortant au débit sortant total

        if debit_entrant != debit_sortant: # on vérifie que le débit entrant est égal au débit sortant pour le sommet courant
            conservation_respectee = False
            break

    verification = {}
    verification["capacites_respectees"] = capacites_respectees
    verification["conservation_respectee"] = conservation_respectee
    return verification


def bfs_predecesseurs(graphe, source, puit, residualCapacities):
    """
    Recherche un chemin augmentant avec une recherche en largeur.

    La recherche utilise le réseau résiduel. Elle peut donc parcourir :
    - des arcs originaux encore disponibles ;
    - des arcs inverses permettant d'annuler un flot déjà envoyé.
    """
    parent = {source: None} # on initialise le dictionnaire des prédécesseurs avec la source comme clé et None comme valeur
    queue = [source] # on initialise la file d'attente avec la source comme premier élément
    while queue:
        node = queue.pop(0) # on récupère le premier élément de la file d'attente et on l'enlève de la file.
        for arc in residualCapacities: # on parcourt tous les arcs du graphe résiduel
            source_arc = arc[0]
            destination_arc = arc[1]
            
            if source_arc != node:# on ne considère que les arcs sortants du noeud courant
                continue
            capacite_restante = residualCapacities[arc] # on récupère la capacité résiduelle de l'arc dans le graphe résiduel

            if capacite_restante <= 0:# on ne considère que les arcs avec une capacité résiduelle positive
                continue
            if destination_arc in parent: # on ne considère que les arcs dont le sommet destination n'a pas encore été visité
                continue
            parent[destination_arc] = node # on ajoute le sommet destination à la liste des prédécesseurs avec le sommet courant comme prédécesseur
            if destination_arc == puit: # on a trouvé un chemin augmentant jusqu'au puits, on retourne le dictionnaire des prédécesseurs
                return parent
            queue.append(destination_arc) # on ajoute le sommet destination à la file d'attente pour continuer la recherche
    return None

def reconstruct_path(parent, source, puit):
    """Reconstruit le chemin à partir du dictionnaire des prédécesseurs."""
    if parent is None or puit not in parent:
        return None
    # Le chemin est reconstruit en partant du puits et en remontant jusqu'à la source grâce aux prédécesseurs.
    path = [] # on initialise le chemin comme une liste vide
    node = puit # on initialise le noeud courant comme le puits

    while node != source: # on continue tant que le noeud courant n'est pas la source
        precedent = parent[node] # on récupère le prédécesseur du noeud courant grace au dictionnaire des prédécesseurs
        arc = (precedent, node) # on crée un arc entre le prédécesseur et le noeud courant
        path.append(arc) # on ajoute l'arc au chemin
        node = precedent # on met à jour le noeud courant pour continuer la reconstruction du chemin

    path.reverse() # on inverse le chemin pour qu'il soit dans le bon ordre, de la source au puits
    return path # on retourne le chemin reconstruit


def bottleneck(path, residualCapacities):
    """Retourne la plus petite capacité résiduelle du chemin."""
    if len(path) == 0:
        return 0
    # La capacité du premier arc est la première valeur de référence.
    plus_petite_capacite = residualCapacities[path[0]]

    # Chaque arc est ensuite comparé à cette valeur.
    for arc in path: # on parcourt tous les arcs du chemin
        capacite = residualCapacities[arc] # on récupère la capacité résiduelle de l'arc dans le graphe résiduel
        if capacite < plus_petite_capacite: # on compare la capacité résiduelle de l'arc avec la plus petite capacité trouvée jusqu'à présent
            plus_petite_capacite = capacite # on met à jour la plus petite capacité si la capacité résiduelle de l'arc est plus petite

    return plus_petite_capacite # on retourne la plus petite capacité résiduelle du chemin

def trouver_source_et_puits(graph):
    """Retourne l'unique source et l'unique puits du graphe."""
    sources = []
    sinks = []
    # Une source n'a aucun arc entrant.
    # Un puits n'a aucun arc sortant.
    for node in graph.nodes:
        if graph.in_degree(node) == 0: # on vérifie si le noeud courant est une source en vérifiant s'il n'a aucun arc entrant, fonction intégrée doc : https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.in_degree.html
            sources.append(node)
        if graph.out_degree(node) == 0: # on vérifie si le noeud courant est un puits en vérifiant s'il n'a aucun arc sortant, fonction intégrée doc : https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.out_degree.html
            sinks.append(node)
    if len(sources) != 1:
        raise ValueError(
            "Le graphe doit avoir une seule source, "
            f"mais {len(sources)} ont été trouvées : {sources}"
        )
    if len(sinks) != 1:
        raise ValueError(
            "Le graphe doit avoir un seul puits, "
            f"mais {len(sinks)} ont été trouvés : {sinks}"
        )
    return sources[0], sinks[0] # on retourne la source et le puits

    
def calculer_flot(graph):
    """
    Calcule le flot maximal par augmentations successives des flots.
    Cette fonction ne fait aucun affichage et retourne uniquement le résultat
    du calcul.
    """
    source, puit = trouver_source_et_puits(graph) # on récupère la source et le puits du graphe
    debits: Flow = {} # on initialise le dictionnaire des débits comme un dictionnaire vide
    for arc in graph.edges: # on parcourt tous les arcs du graphe
        debits[arc] = 0 # on initialise le débit de chaque arc à 0

    residual: Residual = {} # on initialise le dictionnaire des capacités résiduelles comme un dictionnaire vide
    for arc in graph.edges:
        source_arc = arc[0]
        destination_arc = arc[1]
        capacite = graph[source_arc][destination_arc]["capacite"] # on récupère la capacité de l'arc dans le graphe en entrée
        residual[(source_arc, destination_arc)] = capacite # on initialise la capacité résiduelle de chaque arc à sa capacité initiale
        residual[(destination_arc, source_arc)] = 0 # on initialise la capacité résiduelle de chaque arc inverse à 0
        
    while True:
        parent = bfs_predecesseurs(graph,source,puit,residual)
        path = reconstruct_path(parent,source,puit) # on reconstruit le chemin à partir du dictionnaire des prédécesseurs
        if path is None:
            break
        quantite_a_ajouter = bottleneck(path,residual) # on calcule la quantité à ajouter au flot en utilisant la fonction bottleneck
        for arc in path: # on parcourt tous les arcs du chemin
            source_arc = arc[0]
            destination_arc = arc[1]
            # Cas d'un arc original.
            if arc in debits:
                debits[arc] += quantite_a_ajouter # on ajoute la quantité à ajouter au débit de l'arc original
            # Cas d'un arc inverse.
            else:
                arc_original = (destination_arc,source_arc)# on inverse l'arc pour retrouver l'arc original
                debits[arc_original] -= quantite_a_ajouter # on soustrait la quantité à ajouter au débit de l'arc original inverse
            residual[arc] -= quantite_a_ajouter # on soustrait la quantité à ajouter à la capacité résiduelle de l'arc
            arc_inverse = (destination_arc,source_arc) # on inverse l'arc pour retrouver l'arc inverse
            residual[arc_inverse] += quantite_a_ajouter # on ajoute la quantité à ajouter à la capacité résiduelle de l'arc inverse

    valeur_totale_flot = 0
    for cible in graph.successors(source): # on parcourt tous les successeurs de la source pour calculer la valeur totale du flot
        arc = (source, cible) # on récupère l'arc sortant de la source vers le sommet cible
        valeur_totale_flot += debits[arc] # on ajoute les débits de l'arc sortant de la source à la valeur totale du flot

    return debits, residual, valeur_totale_flot, source, puit # on retourne les débits, les capacités résiduelles, la valeur totale du flot, la source et le puits


def calculer_coupe_minimale(graph, residual, source):
    """ 
    =============== PARTIE D ETAPE 6   =======================================
    Détermine les ensembles A et B après le calcul du flot maximal.

    A contient les sommets encore accessibles depuis la source
    dans le réseau résiduel avec une capacité strictement positive.

    B contient tous les autres sommets.
    """
    # Ensemble des sommets accessibles depuis la source.
    sommets_accessibles = {source}
    # File utilisée pour effectuer une exploration en largeur.
    queue = [source]
    while queue:
        # On récupère le premier sommet de la file et on l'enlève de la file.
        sommet_courant = queue.pop(0)
        # On parcourt tous les arcs du réseau résiduel.
        for arc in residual:
            sommet_depart = arc[0]
            sommet_arrivee = arc[1]
            # L'arc doit partir du sommet actuellement étudié.
            if sommet_depart != sommet_courant:
                continue
            # L'arc doit avoir une capacité résiduelle positive.
            capacite_restante = residual[arc]
            if capacite_restante <= 0:
                continue
            # On ne visite pas deux fois le même sommet.
            if sommet_arrivee in sommets_accessibles:
                continue
            sommets_accessibles.add(sommet_arrivee) # on ajoute le sommet destination à l'ensemble des sommets accessibles
            queue.append(sommet_arrivee) # on ajoute le sommet destination à la file pour continuer l'exploration en largeur

    # A contient les sommets accessibles.
    ensemble_A = sommets_accessibles
    # B contient les autres sommets du graphe original.
    ensemble_B = set(graph.nodes) - ensemble_A #on utiliser set(graph.nodes) pour récupérer tous les sommets du graphe original et on soustrait l'ensemble des sommets accessibles
    
    arcs_de_la_coupe = [] # on initialise la liste des arcs de la coupe minimale comme une liste vide
    capacite_de_la_coupe = 0 # on initialise la capacité totale de la coupe minimale à 0
    for arc in graph.edges:
        sommet_depart = arc[0]
        sommet_arrivee = arc[1]
        if sommet_depart in ensemble_A and sommet_arrivee in ensemble_B: # on vérifie si le sommet départ est dans l'ensemble A et le sommet arrivée est dans l'ensemble B
            capacite = graph[sommet_depart][sommet_arrivee]["capacite"] # on récupère la capacité de l'arc dans le graphe original
            arcs_de_la_coupe.append((sommet_depart, sommet_arrivee, capacite)) # on ajoute l'arc à la liste des arcs de la coupe minimale
            capacite_de_la_coupe += capacite # on ajoute la capacité de l'arc à la capacité totale de la coupe minimale

    return (ensemble_A,ensemble_B,arcs_de_la_coupe,capacite_de_la_coupe) # on retourne l'ensemble A, l'ensemble B, la liste des arcs de la coupe minimale et la capacité totale de la coupe minimale



def construire_graphe(graph_data: GraphData) -> nx.DiGraph:
    """Construit un graphe NetworkX à partir des données d'entrée."""
    graph = nx.DiGraph()
    # Chaque entrée décrit un sommet de départ et ses arcs sortants.
    for source, targets in graph_data.items():
        for target in targets:
            destination = target["to"]
            capacite = target["capacite"]
            graph.add_edge(source, destination, capacite=capacite)

    return graph

def dessiner_graphe(graph, debits):
    """Visualise un flot déjà calculé sans recalculer l'algorithme."""
    pos = nx.spring_layout(graph, seed=42)
    # Les arcs saturés sont dessinés en rouge et les autres en gris.
    edge_colors = []
    edge_widths = []
    for edge in graph.edges:
        capacite = graph[edge[0]][edge[1]]["capacite"]
        if debits[edge] == capacite:
            edge_colors.append("red")
            edge_widths.append(3.0)
        else:
            edge_colors.append("gray")
            edge_widths.append(1.2)

    plt.figure(figsize=(9, 6))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2500,
        font_weight="bold",
        arrowsize=20,
        edge_color=edge_colors,
        width=edge_widths,
    )
    # Chaque étiquette indique le débit actuel et la capacité de l'arc.
    edge_labels = {}
    for edge in graph.edges:
        capacite = graph[edge[0]][edge[1]]["capacite"]
        edge_labels[edge] = f"{debits[edge]}/{capacite}"
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, font_color="darkblue"
    )
    plt.title("Flot final dans le réseau (Arcs saturés en rouge)")
    plt.show()


def afficher_resultats(graph, debits, residual, valeur_totale_flot, source, sink):
    """Affiche les résultats d'un calcul déjà effectué."""
    print("\n--- Débit final sur chaque arc ---")
    for arc in graph.edges:
        print(
            f"f({arc[0]}, {arc[1]}) = {debits[arc]} "
            f"/ capacité restante = {residual[arc]}"
        )

    print("\n--- Bilan final du flot ---")
    print(f"Valeur totale du flot : {valeur_totale_flot}")

    print("\n--- Débit f / capacité c sur chaque arc ---")
    for arc in graph.edges:
        capacite = graph[arc[0]][arc[1]]["capacite"]
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"f = {debits[arc]}, c = {capacite}, "
            f"f/c = {debits[arc] / capacite:.2f}"
        )

    print("\n--- Arcs saturés ---")
    arcs_satures = []
    for arc in graph.edges:
        capacite = graph[arc[0]][arc[1]]["capacite"]
        if debits[arc] == capacite:
            arcs_satures.append(arc)
    if arcs_satures:
        for arc in arcs_satures:
            print(f"{arc[0]} -> {arc[1]}")
    else:
        print("Aucun arc saturé.")

    verification = verifier_flot(graph, debits, source, sink)
    print("\n--- Résultat des vérifications finales ---")
    print(
        "Contraintes de capacité respectées : "
        f"{verification['capacites_respectees']}"
    )
    print(
        f"Conservation respectée : "
        f"{verification['conservation_respectee']}"
    )

    


def main():
    """Exécute le scénario complet : entrée, calcul, résultats, affichage."""
    etape1et2(graph_data_etape1)
    
    
    graph = construire_graphe(graph_data_C)
    debits, residual, valeur_totale_flot, source, puit = (calculer_flot(graph))
    afficher_resultats(graph,debits, residual,valeur_totale_flot,source,puit)

    ## PARTIE D
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph,residual,source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph, debits)

if __name__ == "__main__":
    main()
