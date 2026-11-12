from TP1 import (
    afficher_resultats,
    calculer_coupe_minimale,
    calculer_flot,
    dessiner_graphe,
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


GraphData = dict[str, list[dict[str, int | str]]]
Flow = dict[tuple[str, str], int]
Residual = dict[tuple[str, str], int]


### 4.3 Partie B Etape 3 Teste chaque liaison et retourne un tableau décroissant des impacts
def classer_impacts(graph_data, source, puit):
    """
    Calcule l'impact individuel de chaque arête sur le flot maximal.

    Une arête est désactivée seule pour chaque essai. Les données originales
    restent inchangées et chaque graphe testé est évalué directement.
    """
    etats_enabled = {}
    for source_arc, targets in graph_data.items():
        for target in targets:
            etats_enabled[(source_arc, target["to"])] = target.get("enabled",True)
            target["enabled"] = True

    _, _, performance_nominale, _, _ = calculer_flot(graph_data,source,puit)
    impacts = []
    for source_arc, targets in graph_data.items():
        for target in targets:
            destination_arc = target["to"]
            target["enabled"] = False
            _, _, performance_sans_arc, _, _ = calculer_flot(graph_data,source,puit)
            impact = performance_nominale - performance_sans_arc
            impacts.append(
                (
                    (source_arc, destination_arc),
                    performance_sans_arc,
                    impact
                )
            )
            target["enabled"] = True

    for source_arc, targets in graph_data.items():
        for target in targets:
            target["enabled"] = etats_enabled[(source_arc, target["to"])]

    impacts.sort(key=lambda resultat: resultat[2], reverse=True) # on trie la liste des impacts par ordre décroissant de l'impact
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
    Étudie l'impact de la désactivation individuelle de chaque arête
    sur la connectivité (sommets accessibles) depuis chaque sommet du graphe.
    """
    etats_enabled = {}
    for source, targets in graph_data.items():
        for target in targets:
            etats_enabled[(source, target["to"])] = target.get("enabled", True)
            target["enabled"] = True

    sommets, _, _, _ = extraire_donnees_graphe(graph_data)
    resultats = []
    for sommet in sommets:
        accessibles_avant = dfs_connectivite(graph_data, sommet)

        for source, targets in graph_data.items():
            for target in targets:
                destination = target["to"]
                target["enabled"] = False
                accessibles_apres = dfs_connectivite(graph_data, sommet)
                sommets_isoles = accessibles_avant - accessibles_apres
                resultats.append((sommet, (source, destination), sommets_isoles))
                # Restaurer l'état initial de l'arc (à l'intérieur de la boucle sur les arêtes)
                target["enabled"] = True
    # Restauration des états initiaux de graph_data
    for source_arc, targets in graph_data.items():
        for target in targets:
            target["enabled"] = etats_enabled[(source_arc, target["to"])]
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
            if "enabled" not in nouvelle_arete:
                nouvelle_arete["enabled"] = True
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

    ### graphe initial
    debits, residual, valeur_totale_flot, source, puit = (
        calculer_flot(graph_data, source, puit)
    )
    afficher_resultats(graph_data, debits, residual, valeur_totale_flot, source, puit)
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data, debits)
    
    ## R1-R3 disable
    debits, residual, valeur_totale_flot, source, puit = (
        calculer_flot(graph_data_R1R3disable, source, puit)
    )
    afficher_resultats(graph_data_R1R3disable, debits, residual, valeur_totale_flot, source, puit)

    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data_R1R3disable, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data_R1R3disable, debits)

    #R3-client disable
    debits, residual, valeur_totale_flot, source, puit = ( calculer_flot(graph_data_R3Clidisable, source, puit))
    afficher_resultats(graph_data_R3Clidisable, debits, residual, valeur_totale_flot, source, puit)
    ensemble_A, ensemble_B, arcs_de_la_coupe, capacite_de_la_coupe = ( calculer_coupe_minimale(graph_data_R3Clidisable, residual, source))

    print("\n--- Coupe minimale ---")
    print(f"Ensemble A : {ensemble_A}")
    print(f"Ensemble B : {ensemble_B}")

    for arc in arcs_de_la_coupe:
        print(f"{arc[0]} -> {arc[1]} " f"(capacité = {arc[2]})")

    print(f"Capacité de la coupe : {capacite_de_la_coupe}")

    dessiner_graphe(graph_data_R3Clidisable, debits)
    
    dfs = dfs_connectivite(graph_data, "DC")
    print(f"{dfs}")
    
    
    resultats_connectivite = etude_disable_connectivite(graph_data)
    print("\n--- Étude de connectivité après désactivation d'arête, cas ou des sommet se retouve isolé ---")
    for sommet, arc, sommets_isoles in resultats_connectivite:
        if sommets_isoles:
            print(f"Depuis {sommet}, sans {arc[0]} -> {arc[1]} : sommets isolés = {sommets_isoles}")
        
if __name__ == "__main__":
    main()
