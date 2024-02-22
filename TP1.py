import PySimpleGUI as sg  # Importe la bibliothèque PySimpleGUI pour la création d'interfaces graphiques
import csv  # Importe la bibliothèque csv pour la manipulation de fichiers CSV

def charger_fichier_csv(nom_fichier):
    """Charge un fichier CSV et retourne son contenu sous forme de liste de listes."""
    donnees = []  # Initialise une liste vide pour stocker les données CSV
    try:
        with open(nom_fichier, 'r', newline='', encoding='utf-8') as fichier:  # Ouvre le fichier CSV en mode lecture
            lecteur = csv.reader(fichier)  # Crée un objet lecteur CSV pour parcourir les lignes du fichier
            for ligne in lecteur:  # Parcourt chaque ligne du fichier CSV
                donnees.append(ligne)  # Ajoute la ligne à la liste des données
    except FileNotFoundError:  # Gère l'erreur si le fichier n'est pas trouvé
        sg.popup_error("Fichier non trouvé!")
    except Exception as e:  # Gère les autres erreurs potentielles lors de la lecture du fichier
        sg.popup_error(f"Une erreur est survenue : {e}")
    return donnees  # Retourne les données CSV chargées

def principal():
    sg.theme('Reddit')  # Définit le thème de l'interface graphique

    fichier_par_defaut = 'C:\\Users\\elabd\\OneDrive\\Bureau\\TP1 (2)\\CITATIONS.csv'  # Chemin du fichier CSV par défaut

    donnees = charger_fichier_csv(fichier_par_defaut)  # Charge les données du fichier CSV par défaut

    # Définit la mise en page de l'interface graphique
    layout = [
        [sg.Text('Liste des citations', size=(20, 1), font=('Helvetica', 14), justification='center', background_color='#003F5C', text_color='white')],
        [sg.Table(values=donnees[1:], headings=donnees[0], key='-TABLE-', enable_events=True, display_row_numbers=False, auto_size_columns=False, col_widths=25, background_color='#F7F3EC')],
        [sg.Text('Détails de la citation', size=(20, 1), font=('Helvetica', 14), justification='center', background_color='#003F5C', text_color='white')],
        [sg.Multiline("", size=(50, 5), key='-DETAILS-', disabled=True)],
        [sg.Radio("Français", "LANG", default=True, key='-FRANCAIS-', background_color='#003F5C', text_color='white'), sg.Radio("Anglais", "LANG", key='-ANGLAIS-', background_color='#003F5C', text_color='white')],
        [sg.Button("Charger un fichier", size=(15, 1), button_color=('white', '#4CAF50')), sg.Button("Quitter", size=(15, 1), button_color=('white', '#FF5733'))]
    ]

    window = sg.Window('Affichage CSV', layout, background_color='#003F5C')  # Crée une fenêtre avec la mise en page définie

    while True:
        event, values = window.read()  # Attend un événement de la fenêtre
        if event == sg.WINDOW_CLOSED or event == 'Quitter':  # Quitte la boucle si la fenêtre est fermée ou si l'utilisateur clique sur "Quitter"
            break
        elif event == 'Charger un fichier':  # Charge un nouveau fichier CSV si l'utilisateur clique sur "Charger un fichier"
            nom_fichier = sg.popup_get_file('Sélectionnez un fichier CSV', file_types=(("Fichiers CSV", "*.csv"),))
            if nom_fichier:
                nouvelles_donnees = charger_fichier_csv(nom_fichier)
                if nouvelles_donnees:
                    donnees = nouvelles_donnees
                    window['-TABLE-'].update(values=donnees[1:])  # Met à jour les données affichées dans la table
                else:
                    sg.popup_error("Le fichier est vide ou corrompu.")  # Affiche une erreur si le fichier est vide ou corrompu
        elif event == '-TABLE-' and values['-TABLE-']:  # Met à jour les détails de la citation lorsque l'utilisateur sélectionne une ligne dans la table
            indice_ligne_selectionnee = values['-TABLE-'][0] + 1  # Ajoute 1 à l'indice de la ligne sélectionnée
            ligne_selectionnee = donnees[indice_ligne_selectionnee]
            langue_selectionnee = 'fr' if values['-FRANCAIS-'] else 'en'
            indice_citation = 2 if langue_selectionnee == 'fr' else 3
            citation = f'«{ligne_selectionnee[indice_citation]}»' if len(ligne_selectionnee) > indice_citation else ''
            auteur = f"- {ligne_selectionnee[0]}" if len(ligne_selectionnee) > 1 else ''
            indice_profession = 1 if langue_selectionnee == 'fr' else 1
            profession = ligne_selectionnee[indice_profession] if len(ligne_selectionnee) > indice_profession else ''
            details = f"{citation}\n\n{auteur}\n{profession}"
            window['-DETAILS-'].update(value=details)  # Met à jour les détails affichés
    window.close()  # Ferme la fenêtre lorsque l'application se termine

if __name__ == "__main__":
    principal()  # Exécute la fonction principale si le script est exécuté en tant que programme principal
