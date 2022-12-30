def solveur(mot_a_trou: str, mot_déjà_écrit: list = [], lettres_interdites: set = set(), lettres_mal_placés: set = set()):
    liste_mot = []
    mot_a_trou = mot_a_trou.replace(" ", "")
    with open("mots.txt", "r", encoding="utf-8") as f:
        # Parcourez chaque ligne du fichier
        for ligne in f:
                ligne = ligne.strip()
                if len(ligne) == len(mot_a_trou):
                    # Vérifiez si toutes les lettres du mot incomplet sont présentes
                    # dans le mot et si elles se trouvent aux bons emplacements
                    if all(mot_a_trou[i] == "." or mot_a_trou[i] == ligne[i] for i in range(len(ligne))):
                        if all(lettre_i not in ligne for lettre_i in lettres_interdites):
                            if all(lettre_mp[0] in ligne for lettre_mp in lettres_mal_placés):
                                if all(ligne[lettre_mp[1]] != lettre_mp[0] for lettre_mp in lettres_mal_placés):
                                    if ligne not in mot_déjà_écrit:
                                        liste_mot.append(ligne)             
    return liste_mot

if __name__ == "__main__":
    pass