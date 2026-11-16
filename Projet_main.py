import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from graphes import graph_data_TP1, graph_data_TP1_add100_REItoEST, graph_data_TP1_add100_ROUtoREI, graph_data_TP3, debits_TP3, graph_data_TP3_R1R3disable, graph_data_TP3_R3Clidisable, graph_data_TP3_datacenter,graph_data_TP2, pos_TP2

# ============================================================
# EXTRACTION DONNEES GRAPHE (TP1 + TP2 + TP3)
# ============================================================

def extraire_donnees_graphe(graph_data):
    """
    Extrait les sommets, arcs actifs, successeurs et prédécesseurs en Python natif
    (sans utiliser les fonctions de connectivité ou de graphe de NetworkX).
    """
    sommets = set()
    arcs = {}
    successeurs = {}
    predecesseurs = {}

    for src, targets in graph_data.items():
        sommets.add(src)
        successeurs.setdefault(src, [])
        predecesseurs.setdefault(src, [])
        for target in targets:
            dest = target["to"]
            sommets.add(dest)
            successeurs.setdefault(dest, [])
            predecesseurs.setdefault(dest, [])
            if target.get("enabled", True):
                arcs[(src, dest)] = target["capacite"]
                successeurs[src].append(dest)
                predecesseurs[dest].append(src)

    return sommets, arcs, successeurs, predecesseurs


def extraire_latences(graph_data):
    """Extrait les latences de chaque arc actif sous forme de dictionnaire {(u, v): latence}."""
    latences = {}
    for src, targets in graph_data.items():
        for target in targets:
            if target.get("enabled", True):
                latences[(src, target["to"])] = target.get("latence", 0)
    return latences


# ============================================================
# FONCTIONS DE BASE : FLOT MAXIMAL & COUPE MINIMALE (TP1)
# ============================================================

def bfs_residual(graph_data, source, sink, residual):
    """
    Cherche un chemin entre source et sink avec une recherche en largeur.
    """
    parent = {source: None}
    queue = [source]
    while queue:
        node = queue.pop(0) #On prends un élement de la queue
        for (u, v), capacite in residual.items(): #Boucle qui teste le graphe résiduel
            if u == node and capacite > 0: # Si le sommet départ et la capacité est disponible
                voisin = v
                if voisin not in parent:#ET si le sommet arrivé n'est pas dans les parents du sommet
                    parent[voisin] = node#Alors on l'ajoute au tableau
                    if voisin == sink:#Si c'est le puit on s'arrete
                        return parent
                    queue.append(voisin)
    return None


def reconstruct_path(parent, source, sink):
    """Reconstruit le chemin à partir du dictionnaire des prédécesseurs."""
    #On vérifie que le parent n'est pas vide et que le puit est dans parents
    if parent is None or sink not in parent: 
        return None
    path = []
    node = sink#On se place au puit
    while node != source:#Tant que l'on est pas à la source
        precedent = parent[node]#On récupère le parent du sommet
        arc = (precedent, node)#On définit l'arrete entre les deux
        path.append(arc)#Et on l'ajout au chemin
        node = precedent#On remonte les sommets parents
    path.reverse()#On inverse le chemin pour bien avoir le début vers la fin
    return path


def bottleneck(path, residual):
    """Retourne la plus petite capacité résiduelle du chemin."""
    if not path:
        return 0
    plus_petite_capacite = residual[path[0]]#On instancie la plus petite capacité avec la première valeur du chemin
    for arc in path:#Pour chaque arc du chemin
        capacite = residual[arc]#On instancie capacité avec la valeur de l'arrete dans le graphe résiduel
        if capacite < plus_petite_capacite:#Si la capacité est plus petite alors
            plus_petite_capacite = capacite#On redéfinie la valeur de capacité pour correspondre
    return plus_petite_capacite


def bfs_sommets_joignables(source, residual):
    """
    Cherche un chemin encore disponible.
    """
    parent = {source: None}
    queue = [source]
    while queue:
        node = queue.pop(0) #On prends un élement de la queue
        for (u, v), capacite in residual.items(): #Boucle qui teste le graphe résiduel
            if u == node and capacite > 0: # Si le sommet départ et la capacité est disponible
                voisin = v
                if voisin not in parent:#ET si le sommet arrivé n'est pas dans les parents du sommet
                    parent[voisin] = node#Alors on l'ajoute au tableau
                    queue.append(voisin)
    return list(parent.keys())


def coupe(graph_data, source, residual, afficher=True):
    """Calcule la coupe minimale en Python natif via extraire_donnees_graphe."""
    sommets, arcs, _, _ = extraire_donnees_graphe(graph_data)
    ensemble_A = bfs_sommets_joignables(source, residual)
    # On récupère ça dans le sous-ensemble A
    ensemble_B = sommets - set(ensemble_A)
    # On soustrait les noeuds injoignables dans B (noeuds_total est la liste de tous les noeuds)
    if afficher:
        print(f"Coupe minimale: A={ensemble_A} | B={ensemble_B}")
    arcs_coupe = []
    capacite_coupe = 0
    for u in ensemble_A:
        for v in ensemble_B:
            if (u, v) in arcs:
                cap = arcs[(u, v)]
                arcs_coupe.append((u, v, cap))
                capacite_coupe += cap

    return capacite_coupe, arcs_coupe


def calcul_residuel(graph_data, source, sink, debits, residual, afficher=True):
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    numero_chemin = 1
    capacite_coupe = 0

    while True:#On boucle tant que l'on a pas trouvé tous les chemins
        if afficher:
            print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")
        parent = bfs_residual(graph_data, source, sink, residual)#On appelle la fonction bfs pour récupérer les parents
        path = reconstruct_path(parent, source, sink)#On reconstruit le chemin  en fonction du bfs
        #Cassage si pas de chemin trouvé dans le bfs
        if path is None:
            if afficher:
                print(f"Aucun chemin résiduel de {source} vers {sink}.")
                # --- RÉALISATION DE LA COUPE MINIMALE --- Appel fonction coupe
            capacite_coupe, _ = coupe(graph_data, source, residual, afficher=afficher)
            break

        if afficher:
            #Affiche le chemin et les parents
            print(f"Prédécesseurs : {parent}")
            print(f"Chemin trouvé : {path}")
        quantite_a_ajouter = bottleneck(path, residual)#On calcule la plus petite quantité possible à ajouter sur le chemin
        if afficher:
            print(f"Quantité supplémentaire possible : {quantite_a_ajouter}")

        for arc in path:
            u, v = arc
            #Gestion des arêtes "retour" pour le calcul des débits
            if (u, v) in arcs:
                debits[(u, v)] += quantite_a_ajouter
                debit_actuel = debits[(u, v)]
            else:
                debits[(v, u)] -= quantite_a_ajouter
                debit_actuel = debits[(v, u)]

            residual[(u, v)] -= quantite_a_ajouter
            residual[(v, u)] = residual.get((v, u), 0) + quantite_a_ajouter
            #Affiche les valeurs trouvées pour le chemin
            if afficher:
                print(
                    f"Arc {u} -> {v} : "
                    f"débit = {debit_actuel}, "
                    f"capacité restante = {residual[(u, v)]}"
                )
        numero_chemin += 1

    return capacite_coupe


def debit_arc(debits, residual):
    """Affiche le débit final et la capacité restante de chaque arc."""
    print("\n--- Débit final sur chaque arc ---")
    for arc in debits:
        print(f"({arc[0]}, {arc[1]}) = {debits[arc]} / capacité restante = {residual[arc]}")


def calcul_flot(graph_data, source, debits, capacite_coupe):
    """Calcule et affiche le bilan final du flot à partir de extraire_donnees_graphe."""
    _, _, successeurs, _ = extraire_donnees_graphe(graph_data)
    valeur_totale_flot = sum(debits.get((source, cible), 0) for cible in successeurs.get(source, []))
    print("\n--- Bilan final du flot ---")
    print(f"Valeur totale du flot : {valeur_totale_flot}")
    print(f"Capacité de la coupe : {capacite_coupe} == capacité du flot : {valeur_totale_flot} ")
    return valeur_totale_flot


# ============================================================
# FONCTIONS DE LATENCE ET PLUS COURT CHEMIN (TP2)
# ============================================================

def infos_arcs(graph_data, debits):
    """Calcule et affiche les taux d'utilisation et latences dynamiques (BPR) en Python natif."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    taux_utilisations = {}
    latences_c = {}

    print("\n--- Débit f / capacité c sur chaque arc ---")
    for (u, v), capacite in arcs.items():
        debit = debits.get((u, v), 0)
        latence = latences.get((u, v), 0)
        taux_utilisation = debit / capacite if capacite > 0 else 0
        latence_C = latence * (1 + 0.15 * (taux_utilisation ** 4))

        taux_utilisations[(u, v)] = taux_utilisation
        latences_c[(u, v)] = latence_C
        print(f"{u} -> {v} : f = {debit}, c = {capacite}, f/c = {taux_utilisation:.2f}, latence = {latence_C:.2f}")

    return taux_utilisations, latences_c

def recherche_all_chemins(graph_data, source, sink):
    """Trouve tous les chemins simples possibles entre source et sink."""
    chemins_trouves = set()
    while True:
        path = bfs(graph_data, source, sink, chemins_trouves)
        if path is None:
            break
        chemins_trouves.add(tuple(path))
    return chemins_trouves

def bfs(graph_data, source, sink, chemins_deja_trouves):
    """
    Cherche un chemin qui n'a pas été trouvé entre source et sink en largeur,
    en utilisant extraire_donnees_graphe (sans NetworkX).
    """
    _, _, successeurs, _ = extraire_donnees_graphe(graph_data)
    # La file stocke des chemins entiers (listes de sommets) et non plus de simples noeuds
    queue = deque([[source]])

    while queue:
        chemin_sommets = queue.popleft()
        noeud_actuel = chemin_sommets[-1]
        # Si on a atteint la sink, on formate le chemin en liste d'arcs (u, v)
        if noeud_actuel == sink:
            chemin_arcs = [
                (chemin_sommets[i], chemin_sommets[i + 1])
                for i in range(len(chemin_sommets) - 1)
            ]
            # On ne le retourne que s'il n'a pas déjà été découvert lors d'un tour précédent
            if tuple(chemin_arcs) not in chemins_deja_trouves:
                return chemin_arcs
        
        # On explore tous les voisins directs
        for voisin in successeurs.get(noeud_actuel, []):
            # 'voisin not in chemin_sommets' empêche uniquement de tourner en rond (cycles),
            # mais autorise d'autres chemins à réutiliser les mêmes sommets et arêtes.
            if voisin not in chemin_sommets:
                queue.append(chemin_sommets + [voisin])

    return None




def dijkstra(graph_data, chemins_trouves, poids_arcs=None):
    """Trouve le chemin de poids minimal parmi les chemins découverts (sans NetworkX)."""
    if poids_arcs is None:
        poids_arcs = extraire_latences(graph_data)

    Valeur_Dijsktra = float('inf')
    Chemin_plus_court = []
    for chemin in chemins_trouves:#On prends les chemins trouvés
        Valeur_chemin = sum(poids_arcs.get(arc, 0) for arc in chemin) #   à réécrire
        if Valeur_Dijsktra > Valeur_chemin:#On garde en mémoire le plus petit
            Valeur_Dijsktra = Valeur_chemin
            Chemin_plus_court = chemin
        #print(f"La somme de du chemin est {Valeur_chemin} ") 

    return Valeur_Dijsktra, Chemin_plus_court


# ============================================================
# VISUALISATION
# ============================================================

def dessiner_graphe_projet(graph_data, debits, taux_utilisations):
    """Construit un graphe NetworkX uniquement pour l'affichage visuel."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)

    G_visu = nx.DiGraph()
    for (u, v), cap in arcs.items():
        G_visu.add_edge(u, v, capacite=cap, latence=latences.get((u, v), 0), debit=debits.get((u, v), 0))

    plt.figure(figsize=(10, 6))
    edge_colors = []
    for edge in G_visu.edges:
        taux = taux_utilisations.get(edge, 0)
        if taux > 0.9:
            edge_colors.append('red')
        elif taux > 0.5:
            edge_colors.append('yellow')
        else:
            edge_colors.append('green')

    max_debit = max((debits.get(e, 0) for e in G_visu.edges), default=0)
    edge_widths = []
    for edge in G_visu.edges:
        debit = debits.get(edge, 0)
        width = 1.0 + 6.5 * (debit / max_debit) if max_debit > 0 else 1.0
        edge_widths.append(width)

    nx.draw(
        G_visu, pos_TP2, with_labels=True, node_color='lightblue',
        node_size=2500, font_weight='bold', arrowsize=20,
        edge_color=edge_colors, width=edge_widths
    )
    edge_labels = {
        edge: f"{debits.get(edge, 0)}/{arcs[edge]}/{latences.get(edge, 0)}ms"
        for edge in G_visu.edges
    }
    nx.draw_networkx_edge_labels(G_visu, pos, edge_labels=edge_labels, font_color='darkblue')
    plt.title("Flot final dans le réseau (Arcs saturés en rouge)")
    plt.show()


# ============================================================
# TP3 - ANALYSE D'IMPACTS, CONNECTIVITÉ ET PANNES N-1
# (100% Python natif avec extraire_donnees_graphe, sans NetworkX)
# ============================================================

def calculer_flot_et_coupe(graph_data, source, sink):
    """
    Calcule le flot maximal et la coupe minimale sur graph_data
    en utilisant extraire_donnees_graphe et les fonctions de Projet_main.
    """
    sommets, arcs, successeurs, _ = extraire_donnees_graphe(graph_data)
    debits_loc = {arc: 0 for arc in arcs}
    residual_loc = dict(arcs)

    capacite_coupe = calcul_residuel(graph_data, source, sink, debits_loc, residual_loc, afficher=False)
    _, arcs_coupe = coupe(graph_data, source, residual_loc, afficher=False)

    valeur_totale_flot = sum(
        debits_loc.get((source, cible), 0) for cible in successeurs.get(source, [])
    )

    return arcs, debits_loc, residual_loc, valeur_totale_flot, arcs_coupe, capacite_coupe


def desactiver_arc(graph_data, arc_source, arc_destination):
    """Retourne une copie de graph_data où l'arc donné est désactivé."""
    copie_graph = {}
    for src, targets in graph_data.items():
        copie_targets = []
        for target in targets:
            nouvelle_arete = dict(target)
            if src == arc_source and target["to"] == arc_destination:
                nouvelle_arete["enabled"] = False
            copie_targets.append(nouvelle_arete)
        copie_graph[src] = copie_targets
    return copie_graph


def classer_impacts(graph_data, source, sink):
    """Calcule l'impact de la suppression de chaque arc sur le flot maximal."""
    arcs, _, _, performance_nominale, _, _ = calculer_flot_et_coupe(graph_data, source, sink)

    impacts = []
    for arc in arcs:
        graphe_sans_arc = desactiver_arc(graph_data, arc[0], arc[1])
        _, _, _, performance_sans_arc, _, _ = calculer_flot_et_coupe(graphe_sans_arc, source, sink)
        impact = performance_nominale - performance_sans_arc
        impacts.append((arc, performance_sans_arc, impact))

    impacts.sort(key=lambda resultat: resultat[2], reverse=True)
    return impacts


def dfs_connectivite(graph_data, sommet_depart):
    """Retourne l'ensemble des sommets atteignables depuis sommet_depart (sans NetworkX)."""
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
    """Pour chaque sommet, désactive chaque arc un par un et retourne les sommets isolés."""
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


def desactiver_sommet(graph, sommet):
    """Retourne une copie de graph où toutes les arêtes incidentes de sommet sont désactivées."""
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


def analyser_desactivation_sommet(graph_data, sommet, source, sink):
    """
    Analyse l'impact de la désactivation d'un sommet sur le flot maximal,
    les zones servies, le taux d'utilisation et la coupe minimale.
    """
    resultats = {}
    graphe_sans_sommet = desactiver_sommet(graph_data, sommet)

    arcs_apres, debits_apres, _, performance_apres, arcs_coupe, capacite_coupe = calculer_flot_et_coupe(
        graphe_sans_sommet, source, sink
    )
    resultats["performance_apres_desactivation"] = performance_apres

    zones = [u for u, targets in graph_data.items() if any(t["to"] == sink for t in targets)]
    zones_non_servies = []
    for zone in zones:
        demande = next((t["capacite"] for t in graph_data[zone] if t["to"] == sink), 0)
        recu = debits_apres.get((zone, sink), 0)
        if recu < demande:
            zones_non_servies.append(f"{zone} ({recu}/{demande})")
    resultats["zones_non_servies"] = zones_non_servies

    taux_max = 0
    for (u, v), cap in arcs_apres.items():
        if cap > 0:
            taux = (debits_apres.get((u, v), 0) / cap) * 100
            if taux > taux_max:
                taux_max = taux
    resultats["taux_max_utilisation"] = round(taux_max, 2)

    resultats["arcs_coupe_minimale"] = arcs_coupe
    resultats["capacite_coupe_minimale"] = capacite_coupe

    return resultats


# ============================================================
# PROGRAMME PRINCIPAL (TP1 + TP2 + TP3)
# ============================================================

def main():
    # Extraction en Python natif
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data_TP1)

    # Détection de la source et du puits sans NetworkX
    sources = [s for s in sommets if len(predecesseurs[s]) == 0]
    sinks = [s for s in sommets if len(successeurs[s]) == 0]
    if len(sources) != 1 or len(sinks) != 1:
        raise ValueError("Le graphe doit contenir exactement 1 source et 1 puits.")

    source = sources[0]
    sink = sinks[0]

    debits = {arc: 0 for arc in arcs}
    residual = dict(arcs)

    # --- TP1 ---
    capacite_coupe = calcul_residuel(graph_data_TP1, source, sink, debits, residual, afficher=True)
    debit_arc(debits, residual)
    calcul_flot(graph_data_TP1, source, debits, capacite_coupe)

    # --- TP2 ---
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data_TP2)
    taux_utilisations, _ = infos_arcs(graph_data_TP2, debits)
    chemins_trouves = recherche_all_chemins(graph_data_TP2, source, sink)
    Distance, Chemin = dijkstra(graph_data_TP2, chemins_trouves)
    print("\n")
    print(f"Le chemin le plus court a pour distance : {Distance} et est {Chemin}")

    # --- TP3 ---
    print("\n" + "=" * 60)
    print("TP3 - ANALYSE D'IMPACTS ET PANNES N-1")
    print("=" * 60)

    print("\n--- Classement des impacts sur le graphe du projet ---")
    for arc, perf_sans, impact in classer_impacts(graph_data_TP3, source, sink):
        print(f"{arc[0]} -> {arc[1]} : flot sans l'arc = {perf_sans}, impact = {impact}")

    print("\n--- Connectivité DFS depuis la source ---")
    print(dfs_connectivite(graph_data, source))

    try:
        from graphes import graph_data_datacenter
        soms_test = ["DC-LILLE", "DC-PARIS", "DC-LYON", "LIL", "PAR", "LYO", "REI", "STR"]
        for s_test in soms_test:
            res = analyser_desactivation_sommet(graph_data_datacenter, s_test, "S*", "T*")
            print(f"\n--- Désactivation de {s_test} ---")
            print(f"Trafic servi : {res['performance_apres_desactivation']}")
            print(f"Taux max d'utilisation : {res['taux_max_utilisation']}%")
            print(f"Zones non totalement servies : {res['zones_non_servies']}")
            print(f"Nouvelle coupe limitante : {res['arcs_coupe_minimale']} (capacité = {res['capacite_coupe_minimale']})")
    except ImportError:
        pass

    # --- Affichage visuel ---
    dessiner_graphe_projet(graph_data_TP3, debits, taux_utilisations)


if __name__ == "__main__":
    main()
