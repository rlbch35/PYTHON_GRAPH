import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# Structure du graphe
graph_data = {
    "S*": [
            {"to":"DC-A","capacite": 200,"latence":0},
            {"to":"DC-B","capacite": 250,"latence":0}
        ],
    "DC-A": [
            {"to":"R1","capacite": 200,"latence":5}
        ],
    "DC-B": [
            {"to":"R2","capacite": 250,"latence":7}
    ],
    "R1": [
            {"to":"R3","capacite": 160,"latence":6},
            {"to":"LIVE","capacite": 100,"latence":18}
        ],
    "R2": [
            {"to":"R3","capacite": 220,"latence":12},
            {"to":"BACKUP","capacite": 100,"latence":25}
    ],
    "R3": [
            {"to":"LIVE","capacite": 220,"latence":8},
            {"to":"BACKUP","capacite": 250,"latence":10}
    ],
    "LIVE": [
            {"to":"T*","capacite": 220,"latence":0}
    ],
    "BACKUP": [
            {"to":"T*","capacite": 200,"latence":0}
    ]
}

# Positionnement du graphe
pos = {
    'S*':(-2,1),
    'DC-A': (0, 2),    
    'DC-B': (0, 0),      
    'R1': (4, 2),      
    'R2': (4, 0),    
    'R3': (6, 1),      
    'LIVE': (8, 2),
    'BACKUP': (8, 0),
    'T*':(10,1),
}
# Fonctions utilisées par les étapes suivantes
def bfs_residual(graph, source, sink, residual):
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

def bfs_sommets_joignables(source,residual):
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

def coupe(source,residual):
    capacites_initiales=[]
    # On récupère ça dans le sous-ensemble A
    ensemble_A = bfs_sommets_joignables(source, residual)
    # On soustrait les noeuds injoignables dans B (noeuds_total est la liste de tous les noeuds)
    ensemble_B = set(G.nodes) - set(ensemble_A)
    print(f"Coupe minimale: A={ensemble_A} | B={ensemble_B}")
    capacite_coupe = 0
    for u in ensemble_A:
        for v in ensemble_B:
            if G.has_edge(u, v): 
                capacite_coupe += G[u][v]["capacite"]
    return capacite_coupe

def calcul_residuel():
    numero_chemin = 1
    while True:#On boucle tant que l'on a pas trouvé tous les chemins
        print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")
        parent = bfs_residual(G, source, sink, residual)#On appelle la fonction bfs pour récupérer les parents
        path = reconstruct_path(parent, source, sink)#On reconstruit le chemin  en fonction du bfs
        #Cassage si pas de chemin trouvé dans le bfs
        if path is None:
            print(f"Aucun chemin résiduel de {source} vers {sink}.")
            # --- RÉALISATION DE LA COUPE MINIMALE --- Appel fonction coupe
            capacite_coupe=coupe(source,residual)
            break
        #Affiche le chemin et les parents
        print(f"Prédécesseurs : {parent}")
        print(f"Chemin trouvé : {path}")
        quantite_a_ajouter = bottleneck(path, residual)#On calcule la plus petite quantité possible à ajouter sur le chemin
        print(f"Quantité supplémentaire possible : {quantite_a_ajouter}")

        for arc in path:
            u, v = arc
            #Gestion des arêtes "retour" pour le calcul des débits
            if G.has_edge(u, v):
                debits[(u, v)] += quantite_a_ajouter
                debit_actuel = debits[(u, v)]
            else:
                debits[(v, u)] -= quantite_a_ajouter
                debit_actuel = debits[(v, u)]
            
            residual[(u, v)] -= quantite_a_ajouter
            residual[(v, u)] = residual.get((v, u), 0) + quantite_a_ajouter
            #Affiche les valeurs trouvées pour le chemin
            print(
                    f"Arc {arc[0]} -> {arc[1]} : "
                    f"débit = {debits[arc]}, "
                    f"capacité restante = {residual[arc]}"
                )  
        numero_chemin += 1# On recommence
    return capacite_coupe

def debit_arc(debits):
    print("\n--- Débit final sur chaque arc ---")
    for arc in debits:
        print(f"({arc[0]}, {arc[1]}) = {debits[arc]} / capacité restante = {residual[arc]}")

def calcul_flot(debits,capacite_coupe):
    valeur_totale_flot = sum(debits[(source, cible)] for cible in G.successors(source))#Flot est égal a la valeur des débits en sortie de la source
    print("\n--- Bilan final du flot ---")
    print(f"Valeur totale du flot : {valeur_totale_flot}")
    #On peut vérifier notre coupe : 
    print(f"Capacité de la coupe : {capacite_coupe} == capacité du flot : {valeur_totale_flot} ")

def infos_arcs():
    print("\n--- Débit f / capacité c sur chaque arc ---")
    for arc in G.edges:
        debit = debits[arc]
        G[arc[0]][arc[1]]['debit']=debit
        capacite = G[arc[0]][arc[1]]["capacite"]
        latence = G[arc[0]][arc[1]]["latence"]
        taux_utilisation = debit / capacite
        G[arc[0]][arc[1]]['taux_utilisation']=taux_utilisation
        latence_C=latence*(1+0.15*(taux_utilisation**4))
        G[arc[0]][arc[1]]['latence_c']=latence_C
        print(f"{arc[0]} -> {arc[1]} : f = {debit}, c = {capacite}, f/c = {taux_utilisation:.2f}, latence = {latence_C:.2f}")

def recherche_all_chemins(): 
    numero_chemin = 1
    #Recherche de tous les chemins
    while True:
        #print(f"\n--- Recherche du chemin numéro {numero_chemin} ---")
        path = bfs(G, source, sink, chemins_trouves)
        if path is None:
            #print(f"Tous les chemins de {source} vers {sink} ont été trouvés.")
            break
        # On mémorise ce chemin (converti en tuple car une liste n'est pas hachable dans un set)
        chemins_trouves.add(tuple(path))
        #print(f"Chemin trouvé : {path}")
    numero_chemin += 1

def bfs(graph, source, sink, chemins_deja_trouves):
    """
    Cherche un chemin qui n'a pas été trouvé entre source et sink en largeur,
    sans modifier le graphe.
    """
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
        for voisin in graph.successors(noeud_actuel):
            # 'voisin not in chemin_sommets' empêche uniquement de tourner en rond (cycles),
            # mais autorise d'autres chemins à réutiliser les mêmes sommets et arêtes.
            if voisin not in chemin_sommets:
                queue.append(chemin_sommets + [voisin])

    return None

def dijkstra(G,chemins_trouves,weight='latence'):
    Valeur_Dijsktra=float('inf')
    Chemin_plus_court=[]
    for chemin in chemins_trouves:#On prends les chemins trouvés
        #print(chemin)
        Valeur_chemin=0
        for arc in chemin:#Pour chaque arc, on additionne le poids choisi
         Valeur_chemin+=G.edges[arc[0],arc[1]][weight]
        if Valeur_Dijsktra>Valeur_chemin:#On garde en mémoire le plus petit
            Valeur_Dijsktra=Valeur_chemin
            Chemin_plus_court=chemin
        #print(f"La somme de du chemin est {Valeur_chemin} ")    
        
    return (Valeur_Dijsktra, Chemin_plus_court)
# ============================================================
# ÉTAPE 1 - Représenter le graphe
# ============================================================
G = nx.DiGraph()
#Ajout des infos au graphe
for source, targets in graph_data.items():
    for target in targets:
        G.add_edge(source, target["to"], capacite=target["capacite"],latence=target['latence'])

# ============================================================
# Initialisation du graphe
# ============================================================
# Initialisation dynamique de tous les débits à 0
debits = {edge: 0 for edge in G.edges}
#On définit source et sinks (utilisation du fait qu'il n'ait pas de sorties ou d'entrée)
sources = [sommet for sommet in G.nodes if G.in_degree(sommet) == 0]
sinks = [sommet for sommet in G.nodes if G.out_degree(sommet) == 0]
source = sources[0]
sink = sinks[0]
#Vérification qu'on a une seule source et puit
if len(sources) != 1 or len(sinks) != 1:
    raise ValueError("Le graphe doit contenir exactement 1 source et 1 puits.")
# Création du graphe résiduel initial
residual = {}
for source_arc, cible_arc in G.edges:#Pour chaque arrete on prends sommet source et cible 
    arc = (source_arc, cible_arc)#L'arret est composée de la source et de la cible
    capacite_totale = G[source_arc][cible_arc]["capacite"]#On ajout la capacité de l'arc
    residual[arc] = capacite_totale - debits[arc]#On réalise l'initialisation des capacités


# ============================================================
# TP1
# ============================================================
#Lancement de la fonction de recherche des chemins, récupère la capacité de coupe, le reste est directement modifié sur le graphe résiduel 
capacite_coupe=calcul_residuel()
debit_arc(debits)#Débit sur chaque arc
calcul_flot(debits,capacite_coupe)#Flot+Validation avec la coupe



# ============================================================
# TP2
# ============================================================
infos_arcs()#Calcul+affichage des infos sur les arcs (latence, taux utilisation)
####AJout dijsktra
chemins_trouves = set()
recherche_all_chemins()
Distance,Chemin= dijkstra(G,chemins_trouves,weight='latence')
print("\n")
print(f"Le chemin le plus court a pour distance : {Distance} et est {Chemin}")


plt.figure(figsize=(10, 6))
#Modification des couleurs en fonction de l'utilisation
edge_colors = []
for edge in G.edges:
    taux_utilisation = G[edge[0]][edge[1]]['taux_utilisation']
    if taux_utilisation>0.9:
        edge_colors.append('red')
    elif taux_utilisation > 0.5:
        edge_colors.append('yellow')
    else:
        edge_colors.append('green')

#Modification des largeurs en fonction de du débit
max_debit = max(G[u][v]['debit'] for u, v in G.edges)#Calcul du débit max pour faire un ratio pour l'affichage
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
    G, pos, with_labels=True, node_color='lightblue', 
    node_size=2500, font_weight='bold', arrowsize=20,
    edge_color=edge_colors, width=edge_widths
)
edge_labels = {edge: f"{debits[edge]}/{G[edge[0]][edge[1]]['capacite']}/{G[edge[0]][edge[1]]['latence']}ms" for edge in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='darkblue')
plt.title("Flot final dans le réseau (Arcs saturés en rouge)")
plt.show()