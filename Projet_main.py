import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from graphes import graph_data_TP1, graph_data_TP1_add100_REItoEST, graph_data_TP1_add100_ROUtoREI, graph_data_TP3, debits_TP3, graph_data_TP3_R1R3disable, graph_data_TP3_R3Clidisable, graph_data_TP3_datacenter,graph_data_TP2, pos_TP2

# ============================================================
# EXTRACTION DONNEES GRAPHE 
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
    en utilisant extraire_donnees_graphe.
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

def trouver_source_et_puits(graph_data):
    """Trouve automatiquement la source (sans prédécesseur) et le puits (sans successeur)."""
    sommets, _, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    sources = []
    sinks = []
    for sommet in sommets:
        if len(predecesseurs[sommet]) == 0:
            sources.append(sommet)
        if len(successeurs[sommet]) == 0:
            sinks.append(sommet)
    if len(sources) != 1 or len(sinks) != 1:
        raise ValueError("Le graphe doit contenir exactement 1 source et 1 puits.")
    return sources[0], sinks[0]


def main():
    graph_data = graph_data_TP2

    # ============================================================
    # ÉTAPE 1 - Extraction et initialisation des données
    # ============================================================
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)

    # ============================================================
    # Initialisation du graphe
    # ============================================================
    # Initialisation dynamique de tous les débits à 0
    debits = {}
    for arc in arcs:
        debits[arc] = 0

    # On définit source et sink (sommet sans prédécesseur / sans successeur)
    sources = []
    sinks = []
    for sommet in sommets:
        if len(predecesseurs[sommet]) == 0:
            sources.append(sommet)
        if len(successeurs[sommet]) == 0:
            sinks.append(sommet)

    if len(sources) != 1 or len(sinks) != 1:
        raise ValueError("Le graphe doit contenir exactement 1 source et 1 puits.")
    source = sources[0]
    sink = sinks[0]

    # Création du graphe résiduel initial
    residual = {}
    for arc, capacite in arcs.items():
        residual[arc] = capacite - debits[arc]

    # ============================================================
    # TP1 - Calcul du flot maximal et de la coupe minimale
    # ============================================================
    capacite_coupe = calcul_residuel(graph_data, source, sink, debits, residual, afficher=True)
    debit_arc(debits, residual)
    valeur_flot_tp1 = calcul_flot(graph_data, source, debits, capacite_coupe)

    # ============================================================
    # TP2 - Latences dynamiques et plus court chemin (Dijkstra)
    # ============================================================
    taux_utilisations, _ = infos_arcs(graph_data, debits)
    chemins_trouves = recherche_all_chemins(graph_data, source, sink)
    Distance, Chemin = dijkstra(graph_data, chemins_trouves)
    print("\n")
    print(f"Le chemin le plus court a pour distance : {Distance} et est {Chemin}")

    # ============================================================
    # Représentation graphique
    # ============================================================
    G = nx.DiGraph()
    for (u, v), capacite in arcs.items():
        G.add_edge(
            u, v,
            capacite=capacite,
            latence=latences.get((u, v), 0),
            debit=debits.get((u, v), 0),
            taux_utilisation=taux_utilisations.get((u, v), 0),
        )

    plt.figure(num="TP1 & TP2 - Réseau Live / Backup (Flot & Latence)", figsize=(10, 6))
    # Modification des couleurs en fonction de l'utilisation
    edge_colors = []
    for edge in G.edges:
        taux_utilisation = G[edge[0]][edge[1]]['taux_utilisation']
        if taux_utilisation>0.9:
            edge_colors.append('red')
        elif taux_utilisation > 0.5:
            edge_colors.append('yellow')
        else:
            edge_colors.append('green')

    # Modification des largeurs en fonction du débit
    max_debit = 0
    for u, v in G.edges:
        debit = G[u][v]['debit']
        if debit > max_debit:
            max_debit = debit

    edge_widths = []
    for edge in G.edges:
        debit = G[edge[0]][edge[1]]['debit']
        if max_debit > 0:
            # Épaisseur comprise entre 1.0 (vide) et 6.5 (débit max)
            width = 1.0 + 6.5 * (debit / max_debit)
        else:
            width = 1.0
        edge_widths.append(width)

    nx.draw(
        G, pos_TP2, with_labels=True, node_color='lightblue',
        node_size=2500, font_weight='bold', arrowsize=20,
        edge_color=edge_colors, width=edge_widths
    )
    edge_labels = {}
    for edge in G.edges:
        u = edge[0]
        v = edge[1]
        capacite_arc = G[u][v]['capacite']
        latence_arc = G[u][v]['latence']
        edge_labels[edge] = f"{debits[edge]}/{capacite_arc}/{latence_arc}ms"
    nx.draw_networkx_edge_labels(G, pos_TP2, edge_labels=edge_labels, font_color='darkblue')
    plt.title(f"TP1 & TP2 - Flot maximal : {valeur_flot_tp1} | Plus court chemin : {Distance} ms (Arcs >90% en rouge)")
    plt.show()

    # ============================================================
    # TP3
    # ============================================================
    # On retrouve automatiquement la source et le puits pour le graphe TP3
    source_tp3, puit_tp3 = trouver_source_et_puits(graph_data_TP3)

    impacts = classer_impacts(graph_data_TP3, source_tp3, puit_tp3)

    print("\n--- Classement des impacts ---")
    for arc, performance_sans_arc, impact in impacts:
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"flot sans l'arc = {performance_sans_arc}, "
            f"impact = {impact}"
        )

    ### Graphe initial, puis R1-R3 désactivé, puis R3-Clients désactivé (sans etudier_scenario)
    scenarios_tp3 = [graph_data_TP3, graph_data_TP3_R1R3disable, graph_data_TP3_R3Clidisable]
    titres_tp3 = [
        "TP3 - Scénario initial",
        "TP3 - Arc R1 -> R3 désactivé",
        "TP3 - Arc R3 -> Clients désactivé",
    ]
    pos_tp3 = {
        "DC": (0, 1),
        "R1": (1, 2),
        "R2": (1, 0),
        "R3": (2, 2),
        "R4": (2, 0),
        "Clients": (3, 1),
    }

    for indice in range(len(scenarios_tp3)):
        donnees = scenarios_tp3[indice]
        titre_scen = titres_tp3[indice]

        arcs_scen, debits_scen, residual_scen, _, arcs_coupe_scen, capacite_coupe_scen = calculer_flot_et_coupe(
            donnees, source_tp3, puit_tp3
        )
        print(f"\n--- {titre_scen} ({source_tp3} -> {puit_tp3}) ---")
        debit_arc(debits_scen, residual_scen)
        calcul_flot(donnees, source_tp3, debits_scen, capacite_coupe_scen)
        print(f"Arcs de la coupe minimale : {arcs_coupe_scen} (capacité = {capacite_coupe_scen})")

        # Représentation graphique avec NetworkX & Matplotlib
        G_tp3 = nx.DiGraph()
        for (u, v), cap in arcs_scen.items():
            G_tp3.add_edge(u, v, capacite=cap, debit=debits_scen.get((u, v), 0))

        edge_colors_tp3 = []
        edge_widths_tp3 = []
        edge_labels_tp3 = {}
        for edge in G_tp3.edges:
            u = edge[0]
            v = edge[1]
            cap_arc = G_tp3[u][v]["capacite"]
            deb_arc = G_tp3[u][v]["debit"]
            edge_labels_tp3[edge] = f"{deb_arc}/{cap_arc}"
            if deb_arc == cap_arc:
                edge_colors_tp3.append("red")
                edge_widths_tp3.append(3.0)
            else:
                edge_colors_tp3.append("gray")
                edge_widths_tp3.append(1.2)

        plt.figure(num=titre_scen, figsize=(9, 5))
        nx.draw(
            G_tp3, pos_tp3, with_labels=True, node_color="lightblue",
            node_size=2500, font_weight="bold", arrowsize=20,
            edge_color=edge_colors_tp3, width=edge_widths_tp3,
        )
        nx.draw_networkx_edge_labels(G_tp3, pos_tp3, edge_labels=edge_labels_tp3, font_color="darkblue")
        plt.title(f"{titre_scen} | Flot max : {capacite_coupe_scen} (Arcs saturés en rouge)")
        plt.show()

    dfs = dfs_connectivite(graph_data_TP3, source_tp3)
    print(f"\nSommets atteignables depuis {source_tp3} : {dfs}")

    resultats_connectivite = etude_disable_connectivite(graph_data_TP3)

    # On retrouve automatiquement la source et le puits pour le réseau datacenter
    source_dc, puit_dc = trouver_source_et_puits(graph_data_TP3_datacenter)

    # Représentation graphique du réseau datacenter
    arcs_dc, debits_dc, _, flot_dc, _, _ = calculer_flot_et_coupe(
        graph_data_TP3_datacenter, source_dc, puit_dc
    )
    G_dc = nx.DiGraph()
    for (u, v), cap in arcs_dc.items():
        G_dc.add_edge(u, v, capacite=cap, debit=debits_dc.get((u, v), 0))

    pos_dc = {
        "S*": (0, 1),
        "DC-LILLE": (2, 2),
        "DC-PARIS": (2, 1),
        "DC-LYON": (2, 0),
        "LIL": (4, 2),
        "PAR": (4, 1),
        "LYO": (4, 0),
        "REI": (6, 1.5),
        "STR": (6, 0.5),
        "NORD": (8, 2),
        "IDF": (8, 1),
        "Sud-Est": (8, 0),
        "T*": (10, 1),
    }

    edge_colors_dc = []
    edge_widths_dc = []
    edge_labels_dc = {}
    for edge in G_dc.edges:
        u = edge[0]
        v = edge[1]
        cap_arc = G_dc[u][v]["capacite"]
        deb_arc = G_dc[u][v]["debit"]
        edge_labels_dc[edge] = f"{deb_arc}/{cap_arc}"
        if deb_arc == cap_arc:
            edge_colors_dc.append("red")
            edge_widths_dc.append(3.0)
        else:
            edge_colors_dc.append("gray")
            edge_widths_dc.append(1.2)

    plt.figure(num="TP3 - Réseau Datacenter (État nominal)", figsize=(11, 6))
    nx.draw(
        G_dc, pos_dc, with_labels=True, node_color="lightblue",
        node_size=2400, font_weight="bold", font_size=9, arrowsize=20,
        edge_color=edge_colors_dc, width=edge_widths_dc,
    )
    nx.draw_networkx_edge_labels(G_dc, pos_dc, edge_labels=edge_labels_dc, font_color="darkblue", font_size=8)
    plt.title(f"TP3 - Réseau Datacenter nominal | Flot max : {flot_dc} Gbps (Arcs saturés en rouge)")
    plt.show()

    sommet_a_tester = ["DC-LILLE", "DC-PARIS", "DC-LYON", "LIL", "PAR", "LYO", "REI", "STR"]
    for sommet in sommet_a_tester:
        print(f"\n--- Étude de connectivité graph_data_TP3_datacenter - Désactivation de {sommet} ---")
        resultats_connectivite_dict = analyser_desactivation_sommet(
            graph_data_TP3_datacenter, sommet, source_dc, puit_dc
        )
        print(f"Performance après désactivation de {sommet} : {resultats_connectivite_dict['performance_apres_desactivation']}")
        print(f"Taux maximal d'utilisation : {resultats_connectivite_dict['taux_max_utilisation']}%")
        print(f"Zones non totalement servies : {resultats_connectivite_dict['zones_non_servies']}")
        print(f"Arcs de la coupe minimale : {resultats_connectivite_dict['arcs_coupe_minimale']}")
        print(f"Capacité de la coupe minimale : {resultats_connectivite_dict['capacite_coupe_minimale']}")
    


if __name__ == "__main__":
    main()
