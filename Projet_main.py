import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from graphes import *



global capacite_sature
capacite_sature=0
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

def extraire_cout(graph_data):
    """Extrait les couts de chaque arc actif sous forme de dictionnaire {(u, v): cout}."""
    cout = {}
    for src, targets in graph_data.items():
        for target in targets:
            if target.get("enabled", True):
                cout[(src, target["to"])] = target.get("cout", 0)
    return cout

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
            capacite_coupe, _ = coupe(graph_data, source, residual, afficher=True)
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


def afficher_graphe_reseau(
    arcs,
    pos,
    debits,
    latences,
    couts=None,
    taux_utilisations=None,
    titre="État du réseau",
    chemin_highlight=None,
    mode_congestion=False,
):
  """Affiche un graphe orienté du réseau avec plusieurs options de visualisation.

  - Si chemin_highlight est fourni : affiche le graphe en gris neutre et ne
    met en évidence que le chemin (nœuds en doré, arcs en bleu).
  - Si mode_congestion=True : colore selon le taux d'utilisation
    (vert/jaune/rouge)
    et adapte l'épaisseur au débit.
  - Par défaut : surligne uniquement les arcs saturés en rouge.
  """
  taux_utilisations = taux_utilisations or {}
  couts = couts or {} 
  # 1. Construction du graphe
  G = nx.DiGraph()
  for (u, v), capacite in arcs.items():
    G.add_edge(
        u,
        v,
        capacite=capacite,
        latence=round(latences.get((u, v), 0),2),
        cout=round(couts.get((u, v), 0),1),
        debit=debits.get((u, v), 0),
        taux_utilisation=taux_utilisations.get((u, v), 0),
    )

  # Taille panoramique pour éviter l'écrasement horizontal
  fig, ax = plt.subplots(num=titre, figsize=(13, 8))

  # 2. Calcul des couleurs et épaisseurs des arcs
  if chemin_highlight:
    edge_colors = ["#BDC3C7" for _ in G.edges]
    edge_widths = [1.5 for _ in G.edges]
  elif mode_congestion:
    edge_colors = []
    for u, v in G.edges:
      taux = G[u][v]["taux_utilisation"]
      if taux > 0.9:
        edge_colors.append("red")
      elif taux > 0.5:
        edge_colors.append("#F1C40F")
      else:
        edge_colors.append("green")

    max_debit = max((G[u][v]["debit"] for u, v in G.edges), default=0)
    edge_widths = [
        1.5 + 5.5 * (G[u][v]["debit"] / max_debit) if max_debit > 0 else 1.5
        for u, v in G.edges
    ]
  else:
    edge_colors = [
        "red" if G[u][v]["debit"] == G[u][v]["capacite"] else "#7F8C8D"
        for u, v in G.edges
    ]
    edge_widths = [
        3.0 if G[u][v]["debit"] == G[u][v]["capacite"] else 1.5
        for u, v in G.edges
    ]

  # 3. Dessin séparé des nœuds, labels et arêtes
  courbure = "arc3,rad=0.08"
  taille_noeud = 2100

  nx.draw_networkx_nodes(
      G,
      pos,
      node_color="lightblue",
      edgecolors="#2980B9",
      linewidths=1.5,
      node_size=taille_noeud,
      ax=ax,
  )
  nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)

  nx.draw_networkx_edges(
      G,
      pos,
      edge_color=edge_colors,
      width=edge_widths,
      arrowsize=18,
      node_size=taille_noeud,
      connectionstyle=courbure,
      ax=ax,
  )

  # 4. Mise en évidence d'un chemin
  if chemin_highlight:
    if isinstance(chemin_highlight[0], tuple):
      arcs_chemin = chemin_highlight
      noeuds_chemin = list({noeud for arc in arcs_chemin for noeud in arc})
    else:
      noeuds_chemin = chemin_highlight
      arcs_chemin = list(zip(noeuds_chemin[:-1], noeuds_chemin[1:]))

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=noeuds_chemin,
        node_color="gold",
        edgecolors="#D4AC0D",
        linewidths=1.5,
        node_size=taille_noeud,  # Cohérent avec les flèches pour ne pas masquer les pointes
        ax=ax,
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=arcs_chemin,
        edge_color="dodgerblue",
        width=4.0,
        arrowsize=22,
        node_size=taille_noeud,
        connectionstyle=courbure,
        ax=ax,
    )

  # 5. Étiquettes des arcs horizontales (rotate=False)
  edge_labels = {
      (u, v): f"{G[u][v]['debit']}/{G[u][v]['capacite']}/{G[u][v]['latence']}ms/{G[u][v]['cout']}$"
      for u, v in G.edges
  }
  nx.draw_networkx_edge_labels(
      G,
      pos,
      edge_labels=edge_labels,
      font_size=8,
      font_color="darkblue",
      label_pos=0.5,
      rotate=False,
      bbox=dict(
          boxstyle="round,pad=0.2",
          facecolor="white",
          edgecolor="none",
          alpha=0.85,
      ),
      ax=ax,
  )

  ax.margins(0.10)
  plt.axis("off")
  plt.title(titre, fontsize=14, fontweight="bold", pad=15)
  plt.tight_layout()
  plt.show()


# ============================================================
# FONCTIONS DE LATENCE ET PLUS COURT CHEMIN (TP2)
# ============================================================

def infos_arcs(graph_data, debits):
    """Calcule et affiche les taux d'utilisation et latences dynamiques (BPR) en Python natif."""
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    taux_utilisations = {}
    latences_c = {}

    #print("\n--- Débit f / capacité c sur chaque arc ---")
    for (u, v), capacite in arcs.items():
        debit = debits.get((u, v), 0)
        latence = latences.get((u, v), 0)
        taux_utilisation = debit / capacite if capacite > 0 else 0
        latence_C = latence * (1 + 0.15 * (taux_utilisation ** 4))

        taux_utilisations[(u, v)] = taux_utilisation
        latences_c[(u, v)] = latence_C
        #print(f"{u} -> {v} : f = {debit}, c = {capacite}, f/c = {taux_utilisation:.2f}, latence = {latence_C:.2f}")

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


def dijkstra(graph_data, source, sink, poids_arcs=None, residual=None):
    """Algorithme de Dijkstra (sans heapq ni NetworkX) : trouve le chemin de poids minimal entre source et sink."""
    sommets, _, successeurs, _ = extraire_donnees_graphe(graph_data)
    if poids_arcs is None:
        poids_arcs = extraire_latences(graph_data)

    distances = {sommet: float('inf') for sommet in sommets}
    distances[source] = 0
    parent = {source: None}
    non_visites = set(sommets)

    while non_visites:
        # 1. On choisit le sommet non visité ayant la plus petite distance connue
        u = min(non_visites, key=lambda sommet: distances[sommet])

        # Si le plus proche est encore à +inf (inatteignable) ou si on a atteint le puits, on s'arrête
        if distances[u] == float('inf') or u == sink:
            break

        # 2. On fixe définitivement ce sommet
        non_visites.remove(u)

        # 3. Relâchement de tous ses arcs sortants
        for v in successeurs.get(u, []):
            # Si un graphe résiduel est fourni, on ignore les arcs saturés
            if residual is not None and residual.get((u, v), 0) <= 0:
                continue

            poids = poids_arcs.get((u, v), 0)
            nouvelle_distance = distances[u] + poids
            if nouvelle_distance < distances[v]:
                distances[v] = nouvelle_distance
                parent[v] = u

    chemin = reconstruct_path(parent, source, sink)
    if chemin is None:
        return float('inf'), None
    return distances[sink], chemin


def tri_priorité(demandes):
    Priorite_sorted=[]
    niveaux=['critique','élevée','normale','faible']
    for niveau in niveaux:
        for demande in demandes:
            Priorite=demandes[demande]["Priorité"]
            if Priorite == niveau :
                Priorite_sorted.append(demande)
    return Priorite_sorted

def Saturation(capacite_a_ajouter):
    global capacite_sature
    capacite_sature+=capacite_a_ajouter
    return capacite_sature

def calcul_residuel2(graph_data, debits, residual, capacite_a_ajouter, chemins_trouves=None, afficher=True, cout=False):
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    source, sink = trouver_source_et_puits(graph_data)
    numero_chemin = 1

    while capacite_a_ajouter > 0:
        if afficher:
            print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")
            print(f"Il faut ajouter {capacite_a_ajouter}")

        # 1. Mise à jour des latences dynamiques (BPR) selon les débits actuels
        _, latences_dynamiques = infos_arcs(graph_data, debits)

        # 2. Recherche du chemin le moins latent parmi ceux non saturés
        if cout:
            couts = extraire_cout(graph_data)
            valeur_poids, path = dijkstra(
                graph_data,
                source,
                sink,
                poids_arcs=couts,
                residual=residual,
            )
        else:
            valeur_poids, path = dijkstra(
                graph_data,
                source,
                sink,
                poids_arcs=latences_dynamiques,
                residual=residual,
            )

        if path is None:
            if afficher:
                print("Plus aucun chemin résiduel disponible pour absorber le reste de la demande.")
                print(f"{Saturation(capacite_a_ajouter)}Mbit/s n'a pu être placé")                
            break

        if afficher:
            print(f"Chemin trouvé : {path} (latence totale : {valeur_poids:.2f} ms)")

        quantite_a_ajoutermax = bottleneck(path, residual)
        ajout_faisable = min(capacite_a_ajouter, quantite_a_ajoutermax)
        capacite_a_ajouter -= ajout_faisable
        
        for u, v in path:
            if (u, v) in arcs:
                debits[(u, v)] += ajout_faisable
                debit_actuel = debits[(u, v)]
            else:
                debits[(v, u)] -= ajout_faisable
                debit_actuel = debits[(v, u)]

            residual[(u, v)] -= ajout_faisable
            residual[(v, u)] = residual.get((v, u), 0) + ajout_faisable

            if afficher:
                print(f"Arc {u} -> {v} : débit = {debit_actuel}, capacité restante = {residual[(u, v)]}")
        print(f"Il reste {capacite_a_ajouter} à ajouter")
        numero_chemin += 1


# ============================================================
# PROGRAMME PRINCIPAL (TP1 + TP2)
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
    graph_data = graph_data_TP1

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
    capacite_coupe = calcul_residuel(graph_data, source, sink, debits, residual, afficher=False)
    debit_arc(debits, residual)
    valeur_flot_tp1 = calcul_flot(graph_data, source, debits, capacite_coupe)
    ###
    # ============================================================
    # Représentation graphique TP1
    # ============================================================
    afficher_graphe_reseau(arcs=arcs,pos=pos_TP1,debits=debits,latences=latences,titre=(f"TP1 Étape 0 - Débits | Flot: {valeur_flot_tp1} ms"))

    # ============================================================
    # TP2 - Congestion
    # ============================================================
    taux_utilisations, _ = infos_arcs(graph_data, debits)
    afficher_graphe_reseau(arcs=arcs,pos=pos_TP1,debits=debits,latences=latences,taux_utilisations=taux_utilisations,titre=(f"Étape Débits | Affichage de la congestion"),mode_congestion=True)
    
     # ============================================================
        # TP2 - Latences dynamiques et plus court chemin (Dijkstra)
        # ============================================================
    graph_data = graph_data_TP2cout#Modification du graphe avec une latence supplémentaire
    # 1. Ré-extraction des données propres à graph_data_TP2cout
    _, arcs, _, _ = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    couts = extraire_cout(graph_data)
    source, sink = trouver_source_et_puits(graph_data)
    
    # 2. Calcul du plus court chemin (Dijkstra)
    Distance, Chemin = dijkstra(graph_data, source, sink)
    print("\n")
    print(f"Le chemin le plus court a pour distance : {Distance} et est {Chemin}")
    afficher_graphe_reseau(arcs=arcs,pos=pos_TP2,debits=debits,latences=latences,taux_utilisations=taux_utilisations,titre=(f"Étape 1 - Initial | Dijkstra: {Distance} ms"),chemin_highlight=Chemin,)
    graph_data = graph_data_TP2_ajout_latenceR1#Modification du graphe avec une latence supplémentaire
    latences = extraire_latences(graph_data)
    Distance, Chemin = dijkstra(graph_data, source, sink)
    print("\n")
    print(f"Réflexion ingénieur - Si la latence change, le parcours aussi, test en augmentant une arrete")
    print(f"Le chemin le plus court a pour distance : {Distance} et est {Chemin}")
    afficher_graphe_reseau(arcs=arcs,pos=pos_TP2,debits=debits,latences=latences,taux_utilisations=taux_utilisations,titre=(f"Étape 2 - Modification latence R1-R3 | Dijkstra: {Distance} ms"),chemin_highlight=Chemin,)


# ============================================================
        # TP2 - couts et plus court chemin (Dijkstra)
        # ============================================================
    graph_data = graph_data_TP2cout#Modification du graphe avec une latence supplémentaire
    latences = extraire_latences(graph_data)
    couts=extraire_cout(graph_data)
    Distance, Chemin = dijkstra(graph_data, source, sink, poids_arcs=couts)
    print("\n")
    afficher_graphe_reseau(arcs=arcs,pos=pos_TP2,debits=debits,latences=latences,taux_utilisations=taux_utilisations,couts=couts,titre=(f"Étape 2 - Avec le cout | Dijkstra: {Distance} $"),chemin_highlight=Chemin,)

    # ============================================================
    # TP2 - Exemple streamflow gestion latence
    # ============================================================ 
    graph_data = graph_data_Streamflow_exemple
     #1. Ré-extraction des données propres à graph_data_Streamflow
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    couts=extraire_cout(graph_data)

    # 2. Détection de la source et du puits AVANT la recherche de chemins
    source, sink = trouver_source_et_puits(graph_data)
    chemins_trouves = recherche_all_chemins(graph_data, source, sink)

    # 3. Réinitialisation des débits et du graphe résiduel sur les nouveaux arcs
    debits = {arc: 0 for arc in arcs}
    residual2 = {arc: capacite for arc, capacite in arcs.items()}

    calcul_residuel2(graph_data, debits, residual2,720,chemins_trouves, afficher=True,)#Il faudrait calculer le flot a chaque fois
    taux_utilisations,latence_c = infos_arcs(graph_data, debits) 
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - Flux priorisation latence"),mode_congestion=True)
    # ============================================================
    # TP2 - Exemple streamflow gestion cout
     # ============================================================ 
     #1. Ré-extraction des données propres à graph_data_Streamflow
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    couts=extraire_cout(graph_data)

    # 2. Détection de la source et du puits AVANT la recherche de chemins
    source, sink = trouver_source_et_puits(graph_data)
    chemins_trouves = recherche_all_chemins(graph_data, source, sink)

    # 3. Réinitialisation des débits et du graphe résiduel sur les nouveaux arcs
    debits = {arc: 0 for arc in arcs}
    residual2 = {arc: capacite for arc, capacite in arcs.items()}
    
    calcul_residuel2(graph_data, debits, residual2,720,chemins_trouves, afficher=True,cout=True)#Il faudrait calculer le flot a chaque fois
    taux_utilisations,latence_c = infos_arcs(graph_data, debits) 
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - Flux priorisation cout"),mode_congestion=True)
    
    # ============================================================
    # TP2 - Exemple streamflow gestion priorité congestion
    # ============================================================  

    graph_data = graph_data_Streamflow

    # 1. Ré-extraction des données propres à graph_data_Streamflow
    sommets, arcs, successeurs, predecesseurs = extraire_donnees_graphe(graph_data)
    latences = extraire_latences(graph_data)
    couts=extraire_cout(graph_data)

    # 2. Détection de la source et du puits AVANT la recherche de chemins
    source, sink = trouver_source_et_puits(graph_data)
    chemins_trouves = recherche_all_chemins(graph_data, source, sink)

    # 3. Réinitialisation des débits et du graphe résiduel sur les nouveaux arcs
    debits = {arc: 0 for arc in arcs}
    residual2 = {arc: capacite for arc, capacite in arcs.items()}

    # ============================================================
    # TP2 - Exemple streamflow avec priorité
    # ============================================================  
    ###ETAPE5
    demandes={
        "CONTROL": {"débit":20,"Priorité":'critique'},
        "LIVE": {"débit":180,"Priorité":'élevée'}, 
        "VOD": {"débit":220,"Priorité":'normale'},
        "BACKUP": {"débit":300,"Priorité":'faible'}, 
    }
    #trier les demandes par priorité 
    Priorite_sorted=tri_priorité(demandes)
    print("\n")
    print(Priorite_sorted)
    #pour chaque demande, construire le sous-graphe des arcs ayant assez de capacité résiduelle ; 
    print("CONTROL")
    calcul_residuel2(graph_data, debits, residual2,20,chemins_trouves, afficher=True,)#Il faudrait calculer le flot a chaque fois
    taux_utilisations,latence_c = infos_arcs(graph_data, debits) 
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - Critique"),mode_congestion=True)
    print("LIVE")
    calcul_residuel2(graph_data, debits, residual2,180,chemins_trouves, afficher=True,)
    taux_utilisations, latence_c = infos_arcs(graph_data, debits)
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - Elevé"),mode_congestion=True)
    print("VOD")
    calcul_residuel2(graph_data, debits, residual2,220,chemins_trouves, afficher=True,)
    taux_utilisations, latence_c = infos_arcs(graph_data, debits)
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - normale "),mode_congestion=True)
    print("BACKUP")
    calcul_residuel2(graph_data, debits, residual2,300,chemins_trouves, afficher=True,)
    taux_utilisations, latence_c = infos_arcs(graph_data, debits)
    afficher_graphe_reseau(arcs=arcs,pos=pos_Streamflow,debits=debits,latences=latence_c,couts=couts,taux_utilisations=taux_utilisations,titre=(f"TP2 Étape 5 - faible "),mode_congestion=True)
    # calculer un chemin selon un poids choisi ; 
    # placer le trafic ; 
    # mettre à jour capacités résiduelles et latences ;
    #continuer
if __name__ == "__main__":
    main()