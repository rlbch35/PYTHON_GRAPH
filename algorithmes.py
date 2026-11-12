"""
Boîte à outils algorithmique pour les graphes en Python pur (sans NetworkX).
Contient les fonctions de recherche de chemins, de calcul de flot maximal,
de coupe minimale, de connectivité et de simulation de pannes.
"""


def extraire_donnees_graphe(graph_data):
    """
    Extrait les structures Python pures utiles aux algorithmes à partir de
    `graph_data`, en ne conservant que les arêtes actives (`enabled=True`).
    """
    sommets = set()
    arcs = {}           # {(u, v): capacite}
    successeurs = {}    # {u: [v, ...]}
    predecesseurs = {}  # {v: [u, ...]}

    for source, targets in graph_data.items(): # on parcourt tous les sommets du graphe
        sommets.add(source) # on ajoute le sommet courant à l'ensemble des sommets
        successeurs.setdefault(source, []) # on initialise la liste des successeurs du sommet courant si elle n'existe pas encore
        predecesseurs.setdefault(source, []) # on initialise la liste des prédécesseurs du sommet courant si elle n'existe pas encore

        for target in targets:
            destination = target["to"] # on récupère le sommet destination de l'arc courant
            sommets.add(destination) # on ajoute le sommet destination à l'ensemble des sommets
            successeurs.setdefault(destination, []) # on initialise la liste des successeurs du sommet destination si elle n'existe pas encore
            predecesseurs.setdefault(destination, []) # on initialise la liste des prédécesseurs du sommet destination si elle n'existe pas encore

            if target.get("enabled", True): # on vérifie si l'arc est activé, par défaut il est activé
                arcs[(source, destination)] = target["capacite"] # on ajoute l'arc courant à la liste des arcs avec sa capacité
                successeurs[source].append(destination) # on ajoute le sommet destination à la liste des successeurs du sommet courant
                predecesseurs[destination].append(source) # on ajoute le sommet courant à la liste des prédécesseurs du sommet destination

    return sommets, arcs, successeurs, predecesseurs # on retourne l'ensemble des sommets, la liste des arcs avec leurs capacités, la liste des successeurs et la liste des prédécesseurs


def bfs_predecesseurs(source, puit, residualCapacities):
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
    debits = {} # on initialise le dictionnaire des débits comme un dictionnaire vide
    residual = {} # on initialise le dictionnaire des capacités résiduelles comme un dictionnaire vide
    for (source_arc, destination_arc), capacite in arcs.items(): # on parcourt tous les arcs du graphe
        debits[(source_arc, destination_arc)] = 0 # on initialise le débit de chaque arc à 0
        residual[(source_arc, destination_arc)] = capacite # on initialise la capacité résiduelle de chaque arc à sa capacité initiale
        residual[(destination_arc, source_arc)] = 0 # on initialise la capacité résiduelle de chaque arc inverse à 0
        
    while True:
        parent = bfs_predecesseurs(source, puit, residual)
        path = reconstruct_path(parent, source, puit) # on reconstruit le chemin à partir du dictionnaire des prédécesseurs
        if path is None:
            break
        quantite_a_ajouter = bottleneck(path, residual) # on calcule la quantité à ajouter au flot en utilisant la fonction bottleneck
        for arc in path: # on parcourt tous les arcs du chemin
            source_arc = arc[0]
            destination_arc = arc[1]
            # Cas d'un arc original.
            if arc in debits:
                debits[arc] += quantite_a_ajouter # on ajoute la quantité à ajouter au débit de l'arc original
            # Cas d'un arc inverse.
            else:
                arc_original = (destination_arc, source_arc)# on inverse l'arc pour retrouver l'arc original
                debits[arc_original] -= quantite_a_ajouter # on soustrait la quantité à ajouter au débit de l'arc original inverse
            residual[arc] -= quantite_a_ajouter # on soustrait la quantité à ajouter à la capacité résiduelle de l'arc
            arc_inverse = (destination_arc, source_arc) # on inverse l'arc pour retrouver l'arc inverse
            residual[arc_inverse] += quantite_a_ajouter # on ajoute la quantité à ajouter à la capacité résiduelle de l'arc inverse

    valeur_totale_flot = 0
    for cible in successeurs.get(source, []): # on parcourt tous les successeurs de la source pour calculer la valeur totale du flot
        arc = (source, cible) # on récupère l'arc sortant de la source vers le sommet cible
        valeur_totale_flot += debits[arc] # on ajoute les débits de l'arc sortant de la source à la valeur totale du flot

    return debits, residual, valeur_totale_flot, source, puit # on retourne les débits, les capacités résiduelles, la valeur totale du flot, la source et le puits


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

    return {
        "capacites_respectees": capacites_respectees,
        "conservation_respectee": conservation_respectee,
    }


def calculer_coupe_minimale(graph_data, residual, source):
    """ 
    =============== PARTIE D ETAPE 6 =======================================
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

    return (ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe) # on retourne l'ensemble A, l'ensemble B, la liste des arcs de la coupe minimale et la capacité totale de la coupe minimale


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


def desactiver_arc(graph_data, arc_source, arc_destination):
    """Retourne une copie de graph_data où l'arc donné est désactivé.
    1. On crée une copie du graphe original.
    2. On parcourt chaque sommet et ses arcs sortants.
    3. Si l'arc correspond à l'arc à désactiver, on le marque comme désactivé.
    4. On retourne le graphe modifié.
    """
    copie_graph = {}
    for source, targets in graph_data.items():
        copie_targets = []
        for target in targets:
            nouvelle_arete = dict(target)
            if source == arc_source and target["to"] == arc_destination:
                nouvelle_arete["enabled"] = False
            copie_targets.append(nouvelle_arete)
        copie_graph[source] = copie_targets
    return copie_graph


### 4.3 Partie B Etape 3 Teste chaque liaison et retourne un tableau décroissant des impacts
def classer_impacts(graph_data, source, puit):
    """Calcule l'impact de la suppression de chaque arc sur le flot maximal.
    1. On extrait les données du graphe pour obtenir les sommets et les arcs.
    2. On calcule le flot maximal nominal du graphe original.
    3. Pour chaque arc, on désactive l'arc et on calcule le flot maximal du graphe modifié.
    4. On calcule l'impact comme la différence entre le flot nominal et le flot sans l'arc.
    5. On stocke les résultats dans une liste et on la trie par impact décroissant.
    6. On retourne la liste triée des impacts.
    """
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    _, _, performance_nominale, _, _ = calculer_flot(graph_data, source, puit)

    impacts = []
    for arc in arcs:
        graphe_sans_arc = desactiver_arc(graph_data, arc[0], arc[1])
        _, _, performance_sans_arc, _, _ = calculer_flot(graphe_sans_arc, source, puit)
        impact = performance_nominale - performance_sans_arc
        impacts.append((arc, performance_sans_arc, impact))

    impacts.sort(key=lambda resultat: resultat[2], reverse=True) # on trie la liste des impacts par ordre décroissant de l'impact
    return impacts


def etude_disable_connectivite(graph_data):
    """
    Pour chaque sommet, désactive chaque arc un par un et retourne
    les sommets qui ne sont plus accessibles depuis ce sommet.
    1. On extrait les données du graphe pour obtenir les sommets et les arcs.
    2. Pour chaque sommet, on calcule les sommets accessibles avant la désactivation avec dfs_connectivite.
    3. Pour chaque arc, on désactive l'arc et on calcule les sommets accessibles après la désactivation avec dfs_connectivite.
    4. On détermine les sommets isolés en comparant les ensembles de sommets accessibles avant et après la désactivation.
    5. On stocke les résultats dans une liste et on la retourne.    
    """
    sommets, arcs, _, _ = extraire_donnees_graphe(graph_data)
    resultats = []
    for sommet in sommets:
        accessibles_avant = dfs_connectivite(graph_data, sommet)
        for arc in arcs:
            graphe_sans_arc = desactiver_arc(graph_data, arc[0], arc[1])
            accessibles_apres = dfs_connectivite(graphe_sans_arc, sommet)
            sommets_isoles = accessibles_avant - accessibles_apres
            resultats.append((sommet, arc, sommets_isoles))
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
    1. On crée une copie du graphe original.
    2. On parcourt chaque sommet et ses arcs sortants.
    3. Si l'arc sortant ou l'arc entrant correspond au sommet à désactiver, on le marque comme désactivé.
    4. On retourne le graphe modifié.
    """
    copie_graph = {}
    for arc_source, targets in graph.items():
        copie_targets = []
        for target in targets:
            nouvelle_arete = dict(target)
            if arc_source == sommet or nouvelle_arete["to"] == sommet:
                nouvelle_arete["enabled"] = False
            copie_targets.append(nouvelle_arete)
        copie_graph[arc_source] = copie_targets

    return copie_graph


def analyser_desactivation_sommet(graph_data, sommet, source, puit):
    """
    Analyse l'impact de la désactivation d'un sommet sur le flot maximal,
    les zones servies, le taux d'utilisation et la coupe minimale.
    """
    resultats = {}
    # 1. Désactiver le sommet
    graphe_sans_sommet = desactiver_sommet(graph_data, sommet)

    # 2. Calculer le flot après désactivation (on récupère debits et residual !)
    debits, residual, performance_apres, _, _ = calculer_flot(graphe_sans_sommet, source, puit)
    resultats["performance_apres_desactivation"] = performance_apres

    # 3. Zones non totalement servies (les zones vers T* dont le débit n'atteint pas la demande)
    zones = ["NORD", "IDF", "Sud-Est"]
    zones_non_servies = []
    for zone in zones:
        demande = graph_data[zone][0]["capacite"]
        recu = debits.get((zone, puit), 0)
        if recu < demande:
            zones_non_servies.append(f"{zone} ({recu}/{demande})")
    resultats["zones_non_servies"] = zones_non_servies

    # 4. Taux maximal d'utilisation f / c après reroutage
    _, arcs_actifs, _, _ = extraire_donnees_graphe(graphe_sans_sommet)
    taux_max = 0.0
    for arc, capacite in arcs_actifs.items():
        taux = debits[arc] / capacite
        if taux > taux_max:
            taux_max = taux
    resultats["taux_max_utilisation"] = f"{taux_max:.2%}"

    # 5. Calculer la nouvelle coupe minimale en passant bien `residual` et `source`
    _, _, arcs_coupe, capacite_coupe = calculer_coupe_minimale(graphe_sans_sommet, residual, source)
    resultats["arcs_coupe_minimale"] = arcs_coupe
    resultats["capacite_coupe_minimale"] = capacite_coupe

    return resultats
