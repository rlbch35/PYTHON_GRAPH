"""
Point d'entrée principal pour l'exécution du TP3.
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

    # on définit la source et le puit
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

    sommet_a_tester = [ "DC-LILLE","DC-PARIS","DC-LYON","LIL","PAR","LYO","REI","STR","NORD","IDF", "Sud-Est"]
    for sommet in sommet_a_tester:
        resultats_connectivite_dict = analyser_desactivation_sommet(graph_data_datacenter, sommet, "S*", "T*")
        print(f"\n--- Étude de connectivité graph_data_datacenter - Désactivation de {sommet} ---")
        print(f"Performance après désactivation de {sommet} : {resultats_connectivite_dict['performance_apres_desactivation']}")
        print(f"Zones non totalement servies : {resultats_connectivite_dict['zones_non_servies']}")
        print(f"Taux maximal d'utilisation après reroutage : {resultats_connectivite_dict['taux_max_utilisation']}")
        print(f"Arcs de la coupe minimale : {resultats_connectivite_dict['arcs_coupe_minimale']}")
        print(f"Capacité de la coupe minimale : {resultats_connectivite_dict['capacite_coupe_minimale']}")


if __name__ == "__main__":
    main()
