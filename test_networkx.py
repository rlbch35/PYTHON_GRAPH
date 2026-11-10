import networkx as nx
import matplotlib.pyplot as plt


GraphData = dict[str, list[dict[str, int | str]]]
Flow = dict[tuple[str, str], int]
Residual = dict[tuple[str, str], int]


def bfs_residual(graph, source, sink, residual):
    """
    Cherche un chemin entre source et sink avec une recherche en largeur.

    La fonction retourne un dictionnaire de prédécesseurs ou None si aucun
    chemin résiduel n'est disponible.
    """
    # Le dictionnaire mémorise le sommet qui a permis de découvrir
    # chaque sommet. La source n'a pas de prédécesseur.
    parent = {source: None}

    # La file contient les sommets qui doivent encore être examinés.
    queue = [source]

    while queue:
        # La recherche en largeur examine les sommets dans l'ordre
        # dans lequel ils ont été ajoutés à la file.
        node = queue.pop(0)

        for voisin in graph.successors(node):
            arc = (node, voisin)

            # Un arc est utilisable seulement s'il possède encore
            # une capacité résiduelle strictement positive.
            if arc in residual:
                capacite_restante = residual[arc]
            else:
                capacite_restante = 0

            sommet_deja_visite = voisin in parent
            arc_utilisable = capacite_restante > 0

            if not sommet_deja_visite and arc_utilisable:
                parent[voisin] = node

                if voisin == sink:
                    return parent

                queue.append(voisin)

    return None


def reconstruct_path(parent, source, sink):
    """Reconstruit le chemin à partir du dictionnaire des prédécesseurs."""
    if parent is None:
        return None

    if sink not in parent:
        return None

    # Le chemin est reconstruit en partant du puits et en remontant
    # jusqu'à la source grâce aux prédécesseurs.
    path = []
    node = sink

    while node != source:
        precedent = parent[node]
        arc = (precedent, node)
        path.append(arc)
        node = precedent

    # La reconstruction s'est faite à l'envers.
    path.reverse()
    return path


def bottleneck(path, residual):
    """Retourne la plus petite capacité résiduelle du chemin."""
    if len(path) == 0:
        return 0

    # La capacité du premier arc est la première valeur de référence.
    plus_petite_capacite = residual[path[0]]

    # Chaque arc est ensuite comparé à cette valeur.
    for arc in path:
        capacite = residual[arc]
        if capacite < plus_petite_capacite:
            plus_petite_capacite = capacite

    return plus_petite_capacite


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


def trouver_source_et_puits(graph):
    """Retourne l'unique source et l'unique puits du graphe."""
    sources = []
    sinks = []

    # Une source n'a aucun arc entrant.
    # Un puits n'a aucun arc sortant.
    for node in graph.nodes:
        if graph.in_degree(node) == 0:
            sources.append(node)
        if graph.out_degree(node) == 0:
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

    return sources[0], sinks[0]


def calculer_flot(graph):
    """
    Calcule le flot maximal par augmentations successives avec BFS.

    Cette fonction ne fait aucun affichage et retourne uniquement le résultat
    du calcul.
    """
    source, sink = trouver_source_et_puits(graph)

    # Au début, aucun débit ne circule sur les arcs.
    debits: Flow = {}
    for arc in graph.edges:
        debits[arc] = 0

    # La capacité résiduelle initiale est égale à la capacité de chaque arc.
    residual: Residual = {}
    for arc in graph.edges:
        source_arc = arc[0]
        destination_arc = arc[1]
        residual[arc] = graph[source_arc][destination_arc]["capacite"]

    while True:
        # On cherche un nouveau chemin allant de la source au puits.
        parent = bfs_residual(graph, source, sink, residual)
        path = reconstruct_path(parent, source, sink)

        # S'il n'y a plus de chemin disponible, le calcul est terminé.
        if path is None:
            break

        # Le goulot d'étranglement indique la quantité ajoutable
        # sans dépasser la capacité d'un des arcs du chemin.
        quantite_a_ajouter = bottleneck(path, residual)

        for arc in path:
            # Le débit augmente sur chaque arc du chemin.
            debits[arc] += quantite_a_ajouter

            # La capacité résiduelle diminue de la même quantité.
            residual[arc] -= quantite_a_ajouter

    # La valeur totale du flot est la somme des débits sortant de la source.
    valeur_totale_flot = 0
    for cible in graph.successors(source):
        arc = (source, cible)
        valeur_totale_flot += debits[arc]

    return debits, residual, valeur_totale_flot, source, sink


def verifier_flot(graph, debits, source, sink):
    """Vérifie les contraintes de capacité et de conservation du flot."""
    capacites_respectees = True

    # Aucun débit ne doit être négatif ni dépasser la capacité de son arc.
    for arc in graph.edges:
        source_arc = arc[0]
        destination_arc = arc[1]
        debit = debits[arc]
        capacite = graph[source_arc][destination_arc]["capacite"]

        if debit < 0 or debit > capacite:
            capacites_respectees = False
            break

    conservation_respectee = True

    # Pour chaque sommet intermédiaire, le débit entrant doit
    # être égal au débit sortant.
    for node in graph.nodes:
        if node in (source, sink):
            continue

        debit_entrant = 0
        for precedent in graph.predecessors(node):
            arc_entrant = (precedent, node)
            debit_entrant += debits[arc_entrant]

        debit_sortant = 0
        for suivant in graph.successors(node):
            arc_sortant = (node, suivant)
            debit_sortant += debits[arc_sortant]

        if debit_entrant != debit_sortant:
            conservation_respectee = False
            break

    verification = {}
    verification["capacites_respectees"] = capacites_respectees
    verification["conservation_respectee"] = conservation_respectee
    return verification


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


graph_data: GraphData = {
    "DC-A": [
        {"to": "R1", "capacite": 120},
        {"to": "R2", "capacite": 100},
    ],
    "R1": [
        {"to": "R3", "capacite": 70},
        {"to": "Zone-X", "capacite": 40},
    ],
    "R2": [
        {"to": "R3", "capacite": 90},
        {"to": "Zone-X", "capacite": 30},
    ],
    "R3": [
        {"to": "Zone-X", "capacite": 140},
    ],
}


def main():
    """Exécute le scénario complet : entrée, calcul, résultats, affichage."""
    graph = construire_graphe(graph_data)
    debits, residual, valeur_totale_flot, source, sink = calculer_flot(graph)
    afficher_resultats(
        graph, debits, residual, valeur_totale_flot, source, sink
    )
    dessiner_graphe(graph, debits)


if __name__ == "__main__":
    main()
