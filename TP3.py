"""
TP3 - Tolérance aux pannes, connectivité et scénarios de défaillance.
Ce fichier réexporte les modules pour conserver une totale rétrocompatibilité.
"""

from graphes import (
    graph_data,
    graph_data_R1R3disable,
    graph_data_R3Clidisable,
    graph_data_datacenter,
)
from algorithmes import (
    extraire_donnees_graphe,
    calculer_flot,
    calculer_coupe_minimale,
    dfs_connectivite,
    desactiver_arc,
    desactiver_sommet,
    classer_impacts,
    etude_disable_connectivite,
    analyser_desactivation_sommet,
)
from visualisation import (
    dessiner_graphe,
    afficher_resultats,
    afficher_coupe_minimale,
    etudier_scenario,
)
from main_tp3 import main


if __name__ == "__main__":
    main()
