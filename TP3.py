from TP1 import (
    calculer_coupe_minimale,
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
    """Retourne une copie de graph_data où l'arc donné est désactivé.
    1. On crée une copie du graphe original.
    2. On parcourt chaque sommet et ses arcs sortants.
    3. Si l'arc correspond à l'arc à désactiver, on le marque comme désactivé.
    4. On retourne le graphe modifié."""
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
    """Calcule l'impact de la suppression de chaque arc sur le flot maximal.
    1. On extrait les données du graphe pour obtenir les sommets et les arcs.
    2. On calcule le flot maximal nominal du graphe original.
    3. Pour chaque arc, on désactive l'arc et on calcule le flot maximal du graphe modifié.
    4. On calcule l'impact comme la différence entre le flot nominal et le flot sans l'arc.
    5. On stocke les résultats dans une liste et on la trie par impact décroissant.
    6. On retourne la liste triée des impacts."""
    
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
def dfs_connectivite(graph_data, sommet_depart):
    """entrée : graph_data, sommet de départ
    sortie : ensemble des sommets atteignables depuis le sommet de départ
    1. On extrait les données du graphe pour obtenir les successeurs de chaque sommet.
    2. On initialise un ensemble pour suivre les sommets visités et une pile pour l'exploration en profondeur.
    3. Tant que la pile n'est pas vide, on dépile un sommet courant et on explore ses voisins.
    4. Si un voisin n'a pas été visité, on l'ajoute à l'ensemble des visites et on l'empile pour exploration future.
    5. On retourne l'ensemble des sommets visités, qui représente les sommets atteignables depuis le sommet de départ.
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
    # 5. Calculer la nouvelle coupe minimale en passant bien `residual` et `source`
    _, _, arcs_coupe, capacite_coupe = calculer_coupe_minimale(graphe_sans_sommet, residual, source)
    resultats["arcs_coupe_minimale"] = arcs_coupe
    resultats["capacite_coupe_minimale"] = capacite_coupe

    return resultats


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
    sommet_a_tester = [ "DC-LILLE","DC-PARIS","DC-LYON","LIL","PAR","LYO","REI","STR","NORD","IDF", "Sud-Est"]
    for sommet in sommet_a_tester:
        resultats_connectivite_dict = analyser_desactivation_sommet(graph_data_datacenter, sommet,"S*", "T*")
        print(f"\n--- Étude de connectivité graph_data_datacenter - Désactivation de {sommet} ---")
        resultats_connectivite_dict =  analyser_desactivation_sommet(graph_data_datacenter, sommet,"S*", "T*")
        print(f"Performance après désactivation de {sommet} : {resultats_connectivite_dict['performance_apres_desactivation']}")
        print(f"Zones non totalement servies : {resultats_connectivite_dict['zones_non_servies']}")
        print(f"Arcs de la coupe minimale : {resultats_connectivite_dict['arcs_coupe_minimale']}")
        print(f"Capacité de la coupe minimale : {resultats_connectivite_dict['capacite_coupe_minimale']}")
        
if __name__ == "__main__":
    main()
