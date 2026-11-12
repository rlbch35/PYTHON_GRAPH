from asyncio import graph

import networkx as nx
import matplotlib.pyplot as plt
from TP1 import extraire_donnees_graphe

#### LES GRAPHES
graph_data= {
    "DC": [
        {"to":"R1","capacite": 180 },
        {"to":"R2","capacite": 180}
    ],
    "R1": [
        {"to":"R3","capacite": 140},
        {"to":"R4","capacite": 80}
    ],
    "R2": [
        {"to":"R3","capacite": 80},
        {"to":"R4","capacite": 140}
    ],
    "R3": [
        {"to":"Clients","capacite": 160}
    ],
    "R4": [
        {"to":"Clients","capacite": 160}
        ]
}

debits = {
    ("DC", "R1"): 70,
    ("DC", "R2"): 50,
    ("R1", "R3"): 30,
    ("R1", "R5"): 40,
    ("R2", "R3"): 20,
    ("R2", "R4"): 30,
    ("R3", "Clients"): 50,
    ("R4", "Clients"): 50
}


#### LES GRAPHES
graph_data_R1R3disable= {
    "DC": [
        {"to":"R1","capacite": 180, "enabled"  : True },
        {"to":"R2","capacite": 180, "enabled"  : True }
    ],
    "R1": [
        {"to":"R3","capacite": 140, "enabled"  : False },
        {"to":"R4","capacite": 80, "enabled"  : True }
    ],
    "R2": [
        {"to":"R3","capacite": 80, "enabled"  : True },
        {"to":"R4","capacite": 140, "enabled"  : True }
    ],
    "R3": [
        {"to":"Clients","capacite": 160, "enabled"  : True }
    ],
    "R4": [
        {"to":"Clients","capacite": 160, "enabled"  : True }
        ]
}


graph_data_R3Clidisable= {
    "DC": [
        {"to":"R1","capacite": 180, "enabled"  : True },
        {"to":"R2","capacite": 180, "enabled"  : True }
    ],
    "R1": [
        {"to":"R3","capacite": 140, "enabled"  : False },
        {"to":"R4","capacite": 80, "enabled"  : True }
    ],
    "R2": [
        {"to":"R3","capacite": 80, "enabled"  : True },
        {"to":"R4","capacite": 140, "enabled"  : True }
    ],
    "R3": [
        {"to":"Clients","capacite": 160, "enabled"  : False }
    ],
    "R4": [
        {"to":"Clients","capacite": 160, "enabled"  : True }
        ]
}

# Structure du graphe
graph_data_datacenter = {
    "S*": [
            {"to":"DC-LILLE","capacite": 350},
            {"to":"DC-PARIS","capacite": 500},
            {"to":"DC-LYON","capacite": 420}
        ],
    "DC-LILLE": [
            {"to":"LIL","capacite": 350},
    ],
    "DC-PARIS": [
            {"to":"PAR","capacite": 500}
        ],
    "DC-LYON": [
            {"to":"LYO","capacite": 420}
        ],
    "LIL": [
            {"to":"REI","capacite": 240},
            {"to":"PAR","capacite": 180}
    ],
    "PAR": [
            {"to":"REI","capacite": 320},
            {"to":"STR","capacite": 260},
            {"to":"LYO","capacite": 230}
    ],
    "LYO": [
            {"to":"STR","capacite": 230},
    ],
    "REI": [
            {"to":"NORD","capacite": 250},
            {"to":"IDF","capacite": 350}
    ],
    "STR": [
                {"to":"Sud-Est","capacite": 350},
                {"to":"IDF","capacite": 180}
        ],
    "NORD": [
            {"to":"T*","capacite": 250}
        ],
    "IDF": [
            {"to":"T*","capacite": 530}
        ],
    "Sud-Est": [
            {"to":"T*","capacite": 350}
        ]
}


GraphData = dict[str, list[dict[str, int | str]]]
Flow = dict[tuple[str, str], int]
Residual = dict[tuple[str, str], int]

def verifier_flot(graph_data, debits, sourceNode, arriveeNode):
    """Vérification contraintes capacités """
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    capacites_respectees = True # on initialise la variable à True, on va la mettre à False si on trouve un débit qui ne respecte pas les contraintes
    # Aucun débit ne doit être négatif ni dépasser la capacité de son arc. on parcours tous les arcs du graphe et on vérifie que le débit de chaque arc est compris entre 0 et la capacité de l'arc
    for arc, capacite in arcs.items():
        debit = debits[arc] # on récupère le débit de l'arc

        # on vérifie que le débit est compris entre 0 et la capacité de l'arc
        if debit < 0 or debit > capacite:
            capacites_respectees = False # on met la variable à False si le débit ne respecte pas les contraintes
            break
    conservation_respectee = True


    """Vérification contraintes conservation """
    for node in sommets:
        if node in (sourceNode, arriveeNode): # on ne vérifie pas les sommets source et puits, on ne vérifie que les sommets intermédiaires
            continue

        debit_entrant = 0 # on initialise le débit entrant à 0
        for precedent in predecesseurs[node]: # on parcourt tous les sommets précédents du sommet courant
            arc_entrant = (precedent, node) # on récupère l'arc entrant du sommet
            debit_entrant += debits[arc_entrant] # on ajoute le débit de l'arc entrant au débit entrant total

        debit_sortant = 0
        for suivant in successeurs[node]: # on parcourt tous les sommets suivants du sommet courant
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


    
def calculer_flot(graph_data, source, puit):
    """
    Calcule le flot maximal par augmentations successives des flots.
    Cette fonction ne fait aucun affichage et retourne uniquement le résultat
    du calcul.
    """
    _, arcs, successeurs, _ = extraire_donnees_graphe(graph_data)
    debits: Flow = {} # on initialise le dictionnaire des débits comme un dictionnaire vide
    residual: Residual = {} # on initialise le dictionnaire des capacités résiduelles comme un dictionnaire vide
    for (source_arc, destination_arc), capacite in arcs.items(): # on parcourt tous les arcs du graphe
        debits[(source_arc, destination_arc)] = 0 # on initialise le débit de chaque arc à 0
        residual[(source_arc, destination_arc)] = capacite # on initialise la capacité résiduelle de chaque arc à sa capacité initiale
        residual[(destination_arc, source_arc)] = 0 # on initialise la capacité résiduelle de chaque arc inverse à 0
        
    while True:
        parent = bfs_predecesseurs(graph_data,source,puit,residual)
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
    for cible in successeurs.get(source, []): # on parcourt tous les successeurs de la source pour calculer la valeur totale du flot
        arc = (source, cible) # on récupère l'arc sortant de la source vers le sommet cible
        valeur_totale_flot += debits[arc] # on ajoute les débits de l'arc sortant de la source à la valeur totale du flot

    return debits, residual, valeur_totale_flot, source, puit # on retourne les débits, les capacités résiduelles, la valeur totale du flot, la source et le puits


def calculer_coupe_minimale(graph_data, residual, source):
    """ 
    Détermine les ensembles A et B après le calcul du flot maximal.

    A contient les sommets encore accessibles depuis la source
    dans le réseau résiduel avec une capacité strictement positive.

    B contient tous les autres sommets.
    """
    sommets, arcs, _, _ = extraire_donnees_graphe(graph_data)
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
    ensemble_B = sommets - ensemble_A
    
    arcs_de_la_coupe = [] # on initialise la liste des arcs de la coupe minimale comme une liste vide
    capacite_de_la_coupe = 0 # on initialise la capacité totale de la coupe minimale à 0
    for (sommet_depart, sommet_arrivee), capacite in arcs.items():
        if sommet_depart in ensemble_A and sommet_arrivee in ensemble_B: # on vérifie si le sommet départ est dans l'ensemble A et le sommet arrivée est dans l'ensemble B
            arcs_de_la_coupe.append((sommet_depart, sommet_arrivee, capacite)) # on ajoute l'arc à la liste des arcs de la coupe minimale
            capacite_de_la_coupe += capacite # on ajoute la capacité de l'arc à la capacité totale de la coupe minimale

    return (ensemble_A,ensemble_B,arcs_de_la_coupe,capacite_de_la_coupe) # on retourne l'ensemble A, l'ensemble B, la liste des arcs de la coupe minimale et la capacité totale de la coupe minimale   


### 4.3 Partie B Etape 3 Teste chaque liaison et retourne un tableau décroissant des impacts
def classer_impacts(graph_data, source, puit):
    """
    Calcule l'impact individuel de chaque arête sur le flot maximal.

    Une arête est désactivée seule pour chaque essai. Les données originales
    restent inchangées et chaque graphe testé est évalué directement.
    """
    etats_enabled = {}
    for source_arc, targets in graph_data.items():
        for target in targets:
            etats_enabled[(source_arc, target["to"])] = target.get("enabled",True)
            target["enabled"] = True

    _, _, performance_nominale, _, _ = calculer_flot(graph_data,source,puit)
    impacts = []
    for source_arc, targets in graph_data.items():
        for target in targets:
            destination_arc = target["to"]
            target["enabled"] = False
            _, _, performance_sans_arc, _, _ = calculer_flot(graph_data,source,puit)
            impact = performance_nominale - performance_sans_arc
            impacts.append(
                (
                    (source_arc, destination_arc),
                    performance_sans_arc,
                    impact
                )
            )
            target["enabled"] = True

    for source_arc, targets in graph_data.items():
        for target in targets:
            target["enabled"] = etats_enabled[(source_arc, target["to"])]

    impacts.sort(key=lambda resultat: resultat[2], reverse=True) # on trie la liste des impacts par ordre décroissant de l'impact
    return impacts

## 4.4 Partie C Etape 4 test de connectivité
## dfs retourne les sommet atteignables depuis un sommet de départ et le sommet de départ lui-même
"""Sans utiliser les fonctions de connectivité de NetworkX, programmez un BFS/DFS qui indique
quels sommets sont accessibles depuis un sommet donné. Utilisez-le pour déterminer si la
suppression d une arête sépare le graphe utile en plusieurs composantes. Comparez cette notion
avec l impact sur le flot.
"""
def dfs_connectivite(graph_data, sommet_depart):
    _, _, successeurs, _ = extraire_donnees_graphe(graph_data)
    visites = {sommet_depart}
    pile = [sommet_depart]
    while pile:
        sommet_courant = pile.pop()
        for voisin in successeurs.get(sommet_courant, []):
            if voisin not in visites:
                visites.add(voisin)
                pile.append(voisin)
    return visites


def etude_disable_connectivite(graph_data):
    """
    Étudie l'impact de la désactivation individuelle de chaque arête
    sur la connectivité (sommets accessibles) depuis chaque sommet du graphe.
    """
    etats_enabled = {}
    for source, targets in graph_data.items():
        for target in targets:
            etats_enabled[(source, target["to"])] = target.get("enabled", True)
            target["enabled"] = True

    sommets, _, _, _ = extraire_donnees_graphe(graph_data)
    resultats = []
    for sommet in sommets:
        accessibles_avant = dfs_connectivite(graph_data, sommet)

        for source, targets in graph_data.items():
            for target in targets:
                destination = target["to"]
                target["enabled"] = False
                accessibles_apres = dfs_connectivite(graph_data, sommet)
                sommets_isoles = accessibles_avant - accessibles_apres
                resultats.append((sommet, (source, destination), sommets_isoles))
                # Restaurer l'état initial de l'arc (à l'intérieur de la boucle sur les arêtes)
                target["enabled"] = True
    # Restauration des états initiaux de graph_data
    for source_arc, targets in graph_data.items():
        for target in targets:
            target["enabled"] = etats_enabled[(source_arc, target["to"])]
    return resultats

### 4.5 Partie D 
"""Ajoutez la possibilité de désactiver un sommet et toutes ses arêtes incidentes. Testez la perte
de chaque datacenter puis chaque routeur. Pour chaque scénario, relevez : trafic servi ; zones
non totalement servies ; taux maximal d utilisation après reroutage ; nouvelle coupe limitante si
nécessaire."""


def desactiver_sommet(graph, sommet):
    """
    Crée une copie des données du graphe et désactive toutes les arêtes
    incidentes (sortantes et entrantes) de `sommet`.
    """
    copie_graph = {}
    for arc_source, targets in graph.items():
        copie_targets = []
        for target in targets:
            nouvelle_arete = dict(target)
            if "enabled" not in nouvelle_arete:
                nouvelle_arete["enabled"] = True
            if arc_source == sommet or nouvelle_arete["to"] == sommet:
                nouvelle_arete["enabled"] = False
            copie_targets.append(nouvelle_arete)
        copie_graph[arc_source] = copie_targets

    return copie_graph



def dessiner_graphe(graph_data, debits):
    """Visualise un flot déjà calculé sans recalculer l'algorithme."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    graph = nx.DiGraph()
    for (source, destination), capacite in arcs.items():
        graph.add_edge(source, destination, capacite=capacite)

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




def afficher_resultats(graph_data, debits, residual, valeur_totale_flot, source, sink):
    """Affiche les résultats d'un calcul déjà effectué."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    print("\n--- Débit final sur chaque arc ---")
    for arc in arcs:
        print(
            f"f({arc[0]}, {arc[1]}) = {debits[arc]} "
            f"/ capacité restante = {residual[arc]}"
        )

    print("\n--- Bilan final du flot ---")
    print(f"Valeur totale du flot : {valeur_totale_flot}")

    print("\n--- Débit f / capacité c sur chaque arc ---")
    for arc, capacite in arcs.items():
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"f = {debits[arc]}, c = {capacite}, "
            f"f/c = {debits[arc] / capacite:.2f}"
        )

    print("\n--- Arcs saturés ---")
    arcs_satures = []
    for arc, capacite in arcs.items():
        if debits[arc] == capacite:
            arcs_satures.append(arc)
    if arcs_satures:
        for arc in arcs_satures:
            print(f"{arc[0]} -> {arc[1]}")
    else:
        print("Aucun arc saturé.")

    verification = verifier_flot(graph_data, debits, source, sink)
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

    #on définit la source et le puit
    source = "DC"
    puit = "Clients"

    impacts = classer_impacts(graph_data, source, puit)

    print("\n--- Classement des impacts ---")
    for arc, performance_sans_arc, impact in impacts:
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"flot sans l'arc = {performance_sans_arc}, "
            f"impact = {impact}"
        )

    ### graphe initial
    debits, residual, valeur_totale_flot, source, puit = (
        calculer_flot(graph_data, source, puit)
    )
    afficher_resultats(graph_data, debits, residual, valeur_totale_flot, source, puit)
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data, debits)
    
    ## R1-R3 disable
    debits, residual, valeur_totale_flot, source, puit = (
        calculer_flot(graph_data_R1R3disable, source, puit)
    )
    afficher_resultats(graph_data_R1R3disable, debits, residual, valeur_totale_flot, source, puit)

    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data_R1R3disable, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data_R1R3disable, debits)

    #R3-client disable
    debits, residual, valeur_totale_flot, source, puit = ( calculer_flot(graph_data_R3Clidisable, source, puit))
    afficher_resultats(graph_data_R3Clidisable, debits, residual, valeur_totale_flot, source, puit)
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data_R3Clidisable, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data_R3Clidisable, debits)
    
    dfs = dfs_connectivite(graph_data, "DC")
    print(f"{dfs}")
    
    
    resultats_connectivite = etude_disable_connectivite(graph_data)
    print("\n--- Étude de connectivité après désactivation d'arête, cas ou des sommet se retouve isolé ---")
    for sommet, arc, sommets_isoles in resultats_connectivite:
        if sommets_isoles:
            print(f"Depuis {sommet}, sans {arc[0]} -> {arc[1]} : sommets isolés = {sommets_isoles}")
        
if __name__ == "__main__":
    main()
