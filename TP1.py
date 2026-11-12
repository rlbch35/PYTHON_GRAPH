"""
TP1 - Flot maximal et coupe minimale.
Ce fichier réexporte les modules pour conserver une totale rétrocompatibilité.
"""

from graphes import (
    graph_data_etape1,
    graph_data_C,
    graph_data_C_add100_REItoEST,
    graph_data_C_add100_ROUtoREI,
)
from algorithmes import (
    extraire_donnees_graphe,
    bfs_predecesseurs,
    reconstruct_path,
    bottleneck,
    calculer_flot,
    verifier_flot,
    calculer_coupe_minimale,
)
from visualisation import (
    dessiner_graphe,
    afficher_resultats,
    afficher_coupe_minimale,
    etudier_scenario,
    etape1et2,
)
from main_tp1 import main


if __name__ == "__main__":
    main()
