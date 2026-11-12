"""
Module de visualisation graphique et d'affichage pour les graphes.
C'est le seul module du projet qui utilise NetworkX et Matplotlib.
"""

import networkx as nx
import matplotlib.pyplot as plt

from algorithmes import (
    extraire_donnees_graphe,
    calculer_flot,
    verifier_flot,
    calculer_coupe_minimale,
)


def dessiner_graphe(graph_data, debits):
    """Visualise un flot déjà calculé sans recalculer l'algorithme."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    graph = nx.DiGraph()
    for (source, destination), capacite in arcs.items():
        graph.add_edge(source, destination, capacite=capacite)

    pos = nx.spring_layout(graph, seed=42)
    # Les arcs saturés sont dessinés en rouge et les autres en gris.
    # Chaque étiquette indique le débit actuel et la capacité de l'arc.
    edge_colors = []
    edge_widths = []
    edge_labels = {}
    for edge in graph.edges: # on garde l'ordre de NetworkX pour que les couleurs correspondent aux bons arcs
        capacite = arcs[edge]
        edge_labels[edge] = f"{debits[edge]}/{capacite}"
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
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, font_color="darkblue"
    )
    plt.title("Flot final dans le réseau (Arcs saturés en rouge)")
    plt.show()


def afficher_resultats(graph_data, debits, residual, valeur_totale_flot, source, sink):
    """Affiche les résultats d'un calcul déjà effectué."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    print("\n--- Débit f / capacité c sur chaque arc ---")
    for arc, capacite in arcs.items():
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"f = {debits[arc]}, c = {capacite}, "
            f"f/c = {debits[arc] / capacite:.2f}, "
            f"capacité restante = {residual[arc]}"
        )

    print("\n--- Bilan final du flot ---")
    print(f"Valeur totale du flot : {valeur_totale_flot}")

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


def afficher_coupe_minimale(graph_data, residual, source):
    """Calcule puis affiche la coupe minimale (PARTIE D)."""
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = calculer_coupe_minimale(
        graph_data, residual, source
    )
    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")
    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} (capacité = {arc[2]})")
    print(f"Capacité de la coupe : {capacite_de_la_coupe}")


def etudier_scenario(graph_data, source, puit):
    """Calcule, affiche et dessine le flot maximal d'un graphe."""
    debits, residual, valeur_totale_flot, _, _ = calculer_flot(graph_data, source, puit)
    afficher_resultats(graph_data, debits, residual, valeur_totale_flot, source, puit)
    afficher_coupe_minimale(graph_data, residual, source)
    dessiner_graphe(graph_data, debits)


def etape1et2(graph_data_etape1):
    """
    Vérification visuelle et règles de base (Étape 1 et 2 du TP1).
    """
    _, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data_etape1)

    # Création du graphe orienté NetworkX uniquement pour l'affichage.
    G = nx.DiGraph()
    for (source, destination), capacite in arcs.items():
        G.add_edge(source, destination, capacite=capacite)

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

    # Simulation d'un flot valide sur le graphe pour tester les règles de flot valide graphe residuel
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
        capacite = arcs[(source, cible)]
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
        debit_entrant = sum(debits.get((precedent, routeur), 0) for precedent in predecesseurs[routeur])
        debit_sortant = sum(debits.get((routeur, suivant), 0) for suivant in successeurs[routeur])

        respecte = debit_entrant == debit_sortant # on vérifie que somme des débits entrants = somme des débits sortants pour le noeud courant
        print(
            f"{routeur} : entrant = {debit_entrant}, sortant = {debit_sortant} : "
            f"{'OK' if respecte else 'NON RESPECTÉE'}"
        )
        conservation_respectee = conservation_respectee and respecte

    print(f"\nRoutage valide : {capacites_respectees and conservation_respectee}")
