"""
Boîte à outils algorithmique pour les graphes en Python pur (sans NetworkX).
Contient les fonctions de recherche de chemins, de calcul de flot maximal,
de coupe minimale, de connectivité et de simulation de pannes.
"""


def extraire_donnees_graphe(graph_data):
    """
    Extrait les structures Python pures utiles aux algorithmes à partir de
    `graph_data`, en ne conservant que les arêtes actives (`enabled=True`).
    Retourne : (sommets, arcs, successeurs, predecesseurs)
    """
    sommets = set()
    arcs = {}           # {(u, v): capacite}
    successeurs = {}    # {u: [v, ...]}
    predecesseurs = {}  # {v: [u, ...]}

    for source, targets in graph_data.items():
        sommets.add(source)
        successeurs.setdefault(source, [])
        predecesseurs.setdefault(source, [])

        for target in targets:
            destination = target["to"]
            sommets.add(destination)
            successeurs.setdefault(destination, [])
            predecesseurs.setdefault(destination, [])

            if target.get("enabled", True):
                arcs[(source, destination)] = target["capacite"]
                successeurs[source].append(destination)
                predecesseurs[destination].append(source)

    return sommets, arcs, successeurs, predecesseurs


def bfs_predecesseurs(source, puit, residualCapacities):
    """
    Recherche un chemin augmentant avec un parcours en largeur (BFS)
    dans le réseau résiduel.
    """
    parent = {source: None}
    queue = [source]
    while queue:
        node = queue.pop(0)
        for arc in residualCapacities:
            source_arc = arc[0]
            destination_arc = arc[1]

            if source_arc != node:
                continue
            capacite_restante = residualCapacities[arc]

            if capacite_restante <= 0:
                continue
            if destination_arc in parent:
                continue
            parent[destination_arc] = node
            if destination_arc == puit:
                return parent
            queue.append(destination_arc)
    return None


def reconstruct_path(parent, source, puit):
    """Reconstruit le chemin de la source au puits à partir des prédécesseurs."""
    if parent is None or puit not in parent:
        return None
    path = []
    node = puit
    while node != source:
        precedent = parent[node]
        arc = (precedent, node)
        path.append(arc)
        node = precedent

    path.reverse()
    return path


def bottleneck(path, residualCapacities):
    """Retourne la plus petite capacité résiduelle du chemin."""
    if len(path) == 0:
        return 0
    plus_petite_capacite = residualCapacities[path[0]]
    for arc in path:
        capacite = residualCapacities[arc]
        if capacite < plus_petite_capacite:
            plus_petite_capacite = capacite
    return plus_petite_capacite


def calculer_flot(graph_data, source, puit):
    """
    Calcule le flot maximal par augmentations successives (Edmonds-Karp).
    Retourne : (debits, residual, valeur_totale_flot, source, puit)
    """
    _, arcs, successeurs, _ = extraire_donnees_graphe(graph_data)
    debits = {}
    residual = {}
    for (source_arc, destination_arc), capacite in arcs.items():
        debits[(source_arc, destination_arc)] = 0
        residual[(source_arc, destination_arc)] = capacite
        residual[(destination_arc, source_arc)] = 0

    while True:
        parent = bfs_predecesseurs(source, puit, residual)
        path = reconstruct_path(parent, source, puit)
        if path is None:
            break
        quantite_a_ajouter = bottleneck(path, residual)
        for arc in path:
            source_arc = arc[0]
            destination_arc = arc[1]
            if arc in debits:
                debits[arc] += quantite_a_ajouter
            else:
                arc_original = (destination_arc, source_arc)
                debits[arc_original] -= quantite_a_ajouter
            residual[arc] -= quantite_a_ajouter
            arc_inverse = (destination_arc, source_arc)
            residual[arc_inverse] += quantite_a_ajouter

    valeur_totale_flot = 0
    for cible in successeurs.get(source, []):
        arc = (source, cible)
        valeur_totale_flot += debits[arc]

    return debits, residual, valeur_totale_flot, source, puit


def verifier_flot(graph_data, debits, sourceNode, arriveeNode):
    """
    Vérifie le respect des contraintes de capacité et de conservation du débit.
    """
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    capacites_respectees = True
    for arc, capacite in arcs.items():
        debit = debits[arc]
        if debit < 0 or debit > capacite:
            capacites_respectees = False
            break

    conservation_respectee = True
    for node in sommets:
        if node in (sourceNode, arriveeNode):
            continue

        debit_entrant = sum(debits[(p, node)] for p in predecesseurs[node])
        debit_sortant = sum(debits[(node, s)] for s in successeurs[node])

        if debit_entrant != debit_sortant:
            conservation_respectee = False
            break

    return {
        "capacites_respectees": capacites_respectees,
        "conservation_respectee": conservation_respectee,
    }


def calculer_coupe_minimale(graph_data, residual, source):
    """
    Détermine les ensembles A et B ainsi que les arcs de la coupe minimale
    après calcul du flot maximal.
    Retourne : (ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe)
    """
    sommets, arcs, _, _ = extraire_donnees_graphe(graph_data)
    sommets_accessibles = {source}
    queue = [source]
    while queue:
        sommet_courant = queue.pop(0)
        for arc in residual:
            sommet_depart = arc[0]
            sommet_arrivee = arc[1]
            if sommet_depart != sommet_courant:
                continue
            if residual[arc] <= 0:
                continue
            if sommet_arrivee in sommets_accessibles:
                continue
            sommets_accessibles.add(sommet_arrivee)
            queue.append(sommet_arrivee)

    ensemble_A = sommets_accessibles
    ensemble_B = sommets - ensemble_A

    arcs_de_la_coupe = []
    capacite_de_la_coupe = 0
    for (sommet_depart, sommet_arrivee), capacite in arcs.items():
        if sommet_depart in ensemble_A and sommet_arrivee in ensemble_B:
            arcs_de_la_coupe.append((sommet_depart, sommet_arrivee, capacite))
            capacite_de_la_coupe += capacite

    return (ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe)


def dfs_connectivite(graph_data, sommet_depart):
    """
    Parcours en profondeur (DFS) retournant l'ensemble des sommets
    accessibles depuis `sommet_depart`.
    """
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
    """Retourne une copie de graph_data où l'arc donné est désactivé."""
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


def desactiver_sommet(graph, sommet):
    """
    Crée une copie de graph et désactive toutes les arêtes
    incidentes (sortantes et entrantes) de `sommet`.
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


def classer_impacts(graph_data, source, puit):
    """
    Calcule l'impact individuel de chaque arête sur le flot maximal
    et retourne les résultats triés par impact décroissant.
    """
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    _, _, performance_nominale, _, _ = calculer_flot(graph_data, source, puit)

    impacts = []
    for arc in arcs:
        graphe_sans_arc = desactiver_arc(graph_data, arc[0], arc[1])
        _, _, performance_sans_arc, _, _ = calculer_flot(graphe_sans_arc, source, puit)
        impact = performance_nominale - performance_sans_arc
        impacts.append((arc, performance_sans_arc, impact))

    impacts.sort(key=lambda resultat: resultat[2], reverse=True)
    return impacts


def etude_disable_connectivite(graph_data):
    """
    Pour chaque sommet, teste la désactivation de chaque arc un par un
    et retourne les sommets devenus inaccessibles.
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


def analyser_desactivation_sommet(graph_data, sommet, source, puit):
    """
    Analyse l'impact de la désactivation d'un sommet sur le flot maximal,
    les zones servies, le taux d'utilisation et la coupe minimale.
    """
    resultats = {}
    graphe_sans_sommet = desactiver_sommet(graph_data, sommet)

    debits, residual, performance_apres, _, _ = calculer_flot(graphe_sans_sommet, source, puit)
    resultats["performance_apres_desactivation"] = performance_apres

    # Zones non totalement servies (déficit de débit vers le puits)
    zones = ["NORD", "IDF", "Sud-Est"]
    zones_non_servies = []
    for zone in zones:
        demande = graph_data[zone][0]["capacite"]
        recu = debits.get((zone, puit), 0)
        if recu < demande:
            zones_non_servies.append(f"{zone} ({recu}/{demande})")
    resultats["zones_non_servies"] = zones_non_servies

    # Taux maximal d'utilisation f / c après reroutage
    _, arcs_actifs, _, _ = extraire_donnees_graphe(graphe_sans_sommet)
    taux_max = 0.0
    for arc, capacite in arcs_actifs.items():
        taux = debits[arc] / capacite
        if taux > taux_max:
            taux_max = taux
    resultats["taux_max_utilisation"] = f"{taux_max:.2%}"

    # Nouvelle coupe minimale
    _, _, arcs_coupe, capacite_coupe = calculer_coupe_minimale(graphe_sans_sommet, residual, source)
    resultats["arcs_coupe_minimale"] = arcs_coupe
    resultats["capacite_coupe_minimale"] = capacite_coupe

    return resultats
