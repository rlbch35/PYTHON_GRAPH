import io
import sys
from datetime import datetime

# Utiliser le backend non-interactif 'Agg' pour éviter que les fenêtres
# graphiques ne bloquent la génération du rapport Markdown
import matplotlib
matplotlib.use("Agg")

import Projet_main


def capturer_prints_projet():
    """
    Exécute Projet_main.main() en capturant tout ce qui est affiché
    avec print() dans le terminal.
    """
    ancien_stdout = sys.stdout
    tampon = io.StringIO()
    sys.stdout = tampon

    try:
        Projet_main.main()
    finally:
        # On restaure toujours la sortie standard normale
        sys.stdout = ancien_stdout

    return tampon.getvalue()


def convertir_en_markdown(texte_brut):
    """
    Transforme le texte brut des print() en un document Markdown structuré.
    """
    lignes_markdown = []
    date_heure = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

    lignes_markdown.append("# Rapport d'analyse réseau (TP1, TP2 & TP3)\n")
    lignes_markdown.append(f"*Généré automatiquement le {date_heure} depuis `Projet_main.py`*\n")
    lignes_markdown.append("---\n")

    lignes = texte_brut.splitlines()

    for ligne in lignes:
        ligne_propre = ligne.strip()

        # Ignorer les lignes vides multiples ou les simples barres "==="
        if not ligne_propre:
            lignes_markdown.append("")
            continue
        if ligne_propre.startswith("===="):
            continue

        # Transformer les titres "--- Titre ---" en sous-titres Markdown (###)
        if ligne_propre.startswith("--- ") and ligne_propre.endswith(" ---"):
            titre = ligne_propre.replace("--- ", "").replace(" ---", "")
            lignes_markdown.append(f"\n### {titre}\n")

        # Transformer les lignes "Clé : Valeur" en liste à puces
        elif " : " in ligne_propre:
            morceaux = ligne_propre.split(" : ", 1)
            cle = morceaux[0]
            valeur = morceaux[1]
            lignes_markdown.append(f"- **`{cle}`** : {valeur}")

        # Autres lignes (ex: ensembles, chemins, etc.)
        else:
            lignes_markdown.append(f"- {ligne_propre}")

    return "\n".join(lignes_markdown)


def main():
    fichier_sortie = "rapport_resultats.md"

    print("Exécution de Projet_main.py et capture des résultats...")
    texte_capture = capturer_prints_projet()

    print("Conversion en Markdown...")
    contenu_md = convertir_en_markdown(texte_capture)

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        f.write(contenu_md)

    print(f"Terminé ! Le rapport a été enregistré dans '{fichier_sortie}'.")


if __name__ == "__main__":
    main()
