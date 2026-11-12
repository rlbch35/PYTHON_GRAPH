"""
Point d'entrée principal pour l'exécution du TP1.
Exécute :
- Les étapes 1 et 2 (vérification visuelle et règles d'un flot valide)
- L'étude complète du graphe C (calcul du flot maximal, vérifications, coupe minimale et affichage)
"""

from graphes import graph_data_etape1, graph_data_C
from visualisation import etape1et2, etudier_scenario


def main():
    print("=== TP1 - ÉTAPES 1 ET 2 ===")
    etape1et2(graph_data_etape1)

    print("\n=== TP1 - ÉTUDE DU GRAPHE C ===")
    etudier_scenario(graph_data_C, source="S*", puit="T*")


if __name__ == "__main__":
    main()
