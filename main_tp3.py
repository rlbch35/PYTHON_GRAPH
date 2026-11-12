"""
Point d'entrée principal pour l'exécution du TP3.
Exécute :
- Le classement des impacts individuels des arêtes sur le flot
- L'étude des scénarios de pannes de liaisons (R1-R3, R3-Clients)
- Le test de connectivité DFS
- L'étude des déconnexions d'arêtes isolant des sommets
- L'analyse de la désactivation des sommets (datacenters puis routeurs) sur graph_data_datacenter
"""

from graphes import (
    graph_data,
    graph_data_R1R3disable,
    graph_data_R3Clidisable,
    graph_data_datacenter,
)
from algorithmes import (
    classer_impacts,
    dfs_connectivite,
    etude_disable_connectivite,
    analyser_desactivation_sommet,
)
from visualisation import etudier_scenario


def main():
    source = "DC"
    puit = "Clients"

    print("=== TP3 - CLASSEMENT DES IMPACTS DES ARÊTES ===")
    impacts = classer_impacts(graph_data, source, puit)
    for arc, performance_sans_arc, impact in impacts:
        print(
            f"{arc[0]} -> {arc[1]} : "
            f"flot sans l'arc = {performance_sans_arc}, "
            f"impact = {impact}"
        )

    print("\n=== TP3 - ÉTUDE DES SCÉNARIOS (Initial, R1-R3 coupé, R3-Clients coupé) ===")
    for nom, donnees in [
        ("Graphe initial", graph_data),
        ("R1-R3 désactivé", graph_data_R1R3disable),
        ("R3-Clients désactivé", graph_data_R3Clidisable),
    ]:
        print(f"\n--- {nom} ---")
        etudier_scenario(donnees, source, puit)

    print("\n=== TP3 - CONNECTIVITÉ DFS DEPUIS DC ===")
    dfs = dfs_connectivite(graph_data, "DC")
    print(f"Sommets accessibles depuis DC : {dfs}")

    print("\n=== TP3 - ARÊTES DONT LA DÉCONNEXION ISOLE DES SOMMETS ===")
    resultats_connectivite = etude_disable_connectivite(graph_data)
    for sommet, arc, sommets_isoles in resultats_connectivite:
        if sommets_isoles:
            print(f"Depuis {sommet}, sans {arc[0]} -> {arc[1]} : sommets isolés = {sommets_isoles}")

    print("\n=== TP3 - PARTIE D : PERTE DE CHAQUE DATACENTER PUIS ROUTEUR ===")
    sommet_a_tester = [
        "DC-LILLE", "DC-PARIS", "DC-LYON",
        "LIL", "PAR", "LYO", "REI", "STR",
        "NORD", "IDF", "Sud-Est"
    ]
    for sommet in sommet_a_tester:
        res = analyser_desactivation_sommet(graph_data_datacenter, sommet, "S*", "T*")
        print(f"\n--- Désactivation de {sommet} ---")
        print(f"  Performance après désactivation : {res['performance_apres_desactivation']}")
        print(f"  Zones non totalement servies : {res['zones_non_servies']}")
        print(f"  Taux maximal d'utilisation après reroutage : {res['taux_max_utilisation']}")
        print(f"  Arcs de la coupe minimale : {res['arcs_coupe_minimale']}")
        print(f"  Capacité de la coupe minimale : {res['capacite_coupe_minimale']}")


if __name__ == "__main__":
    main()
