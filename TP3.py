from TP1 import (
    calculer_flot,
    etudier_scenario,
    extraire_donnees_graphe,
)

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


### 4.3 Partie B Etape 3 Teste chaque liaison et retourne un tableau décroissant des impacts
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


def classer_impacts(graph_data, source, puit):
    """Calcule l'impact de la suppression de chaque arc sur le flot maximal."""
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
    Pour chaque sommet, désactive chaque arc un par un et retourne
    les sommets qui ne sont plus accessibles depuis ce sommet.
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

    ### graphe initial, puis R1-R3 désactivé, puis R3-Clients désactivé
    for donnees in [graph_data, graph_data_R1R3disable, graph_data_R3Clidisable]:
        etudier_scenario(donnees, source, puit)

    dfs = dfs_connectivite(graph_data, "DC")
    print(f"{dfs}")

    resultats_connectivite = etude_disable_connectivite(graph_data)
    print("\n--- Étude de connectivité après désactivation d'arête, cas ou des sommet se retouve isolé ---")
    for sommet, arc, sommets_isoles in resultats_connectivite:
        if sommets_isoles:
            print(f"Depuis {sommet}, sans {arc[0]} -> {arc[1]} : sommets isolés = {sommets_isoles}")
        
if __name__ == "__main__":
    main()
