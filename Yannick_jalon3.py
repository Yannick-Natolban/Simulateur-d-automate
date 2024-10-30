import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import Canvas

# Variables globales pour stocker les informations de l'automate
etats = set()
alphabet = ['a', 'b']
transitions = {}
init = None
accept = set()

def set_alphabet():
    global alphabet
    alphabet_str = simpledialog.askstring("Alphabet", "Entrez les symboles de l'alphabet séparés par des virgules :")
    if alphabet_str:
        alphabet = alphabet_str.split(',')
def define_afd():
    global etats, init, accept, transitions, automate_type
    automate_type = "AFD"
    etats_count = simpledialog.askinteger("Nombre d'états", "Entrez le nombre d'états :")
    if etats_count is None:
        return
    
    etats = set(range(1, etats_count + 1))
    
    init = simpledialog.askinteger("État initial", "Entrez l'état initial :")
    if init is None or init not in etats:
        messagebox.showerror("Erreur", "L'état initial doit appartenir aux états définis.")
        return
    
    accept_str = simpledialog.askstring("États acceptants", "Entrez les états acceptants séparés par des virgules :")
    if accept_str:
        accept = set(map(int, accept_str.split(',')))
        if not accept.issubset(etats):
            messagebox.showerror("Erreur", "Les états acceptants doivent appartenir aux états définis.")
            return
    else:
        accept = set()
    
    # Créer une fenêtre pop-up pour dessiner la table de transition et saisir les transitions
    transition_window = tk.Toplevel()
    transition_window.title("Table de transition")
    transition_window.geometry("400x300")

    # Couleurs
    label_color = "lightgrey"
    cell_color = "white"
    header_color = "lightblue"
    accept_color = "lightgreen"  # Couleur pour les états acceptants
    
    # Créer une table de transition avec des cases vides
    table = [[None for _ in range(len(alphabet) + 1)] for _ in range(len(etats) + 1)]
    
    # Remplir la première ligne avec les symboles de l'alphabet
    for j, symbol in enumerate(alphabet):
        label = tk.Label(transition_window, text=symbol, bg=header_color, padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=0, column=j + 1, sticky="nsew")
    
    # Remplir la première colonne avec les états
    for i, state in enumerate(etats):
        bg_color = accept_color if state in accept else header_color
        label = tk.Label(transition_window, text=state, bg=bg_color, padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=i + 1, column=0, sticky="nsew")
        
        # Ajouter une flèche devant l'état initial
        if state == init:
            arrow_label = tk.Label(transition_window, text="→", bg=bg_color)
            arrow_label.grid(row=i + 1, column=0, sticky="nse")
    
    # Fonction pour saisir les transitions dans la table
    def enter_transitions(transitions):
        try:
            for i in range(1, len(etats) + 1):
                for j in range(1, len(alphabet) + 1):
                    cell_value = cells[i][j].get()
                    if cell_value:
                        next_state = int(cell_value)
                        if next_state not in etats:
                            messagebox.showerror("Erreur", f"L'état {next_state} n'est pas un état valide.")
                            return
                        transitions[(table[i][0], table[0][j])] = next_state
            transition_window.destroy()
            messagebox.showinfo("Succès", "Automate défini avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des nombres entiers pour les transitions.")
    
    # Créer les champs de saisie pour les transitions
    cells = []
    for i in range(len(etats) + 1):
        row = []
        for j in range(len(alphabet) + 1):
            if i == 0 or j == 0:
                label = tk.Label(transition_window, text=table[i][j], bg=header_color, padx=10, pady=5, borderwidth=1, relief="solid")
                row.append(label)
            else:
                entry = tk.Entry(transition_window, bg=cell_color, borderwidth=1, relief="solid")
                entry.grid(row=i, column=j, sticky="nsew")
                row.append(entry)
        cells.append(row)
    
    # Bouton pour valider les transitions
    btn_enter = tk.Button(transition_window, text="Valider", command=lambda: enter_transitions(transitions))
    btn_enter.grid(row=len(etats) + 2, columnspan=len(alphabet) + 1, pady=10)

    # Bouton pour compléter l'automate
    btn_completer = tk.Button(transition_window, text="Compléter", command=lambda: completer((etats, alphabet, transitions, init, accept)))
    btn_completer.grid(row=len(etats) + 3, columnspan=len(alphabet) + 1, pady=10)

    # Bouton pour émonder l'automate
    btn_emonder = tk.Button(transition_window, text="Émonder", command=lambda: emonder((etats, alphabet, transitions, init, accept)))
    btn_emonder.grid(row=len(etats) + 4, columnspan=len(alphabet) + 1, pady=10)

    # Configurer les poids des lignes et des colonnes pour le redimensionnement
    for i in range(len(etats) + 1):
        transition_window.grid_rowconfigure(i, weight=1)
    for j in range(len(alphabet) + 1):
        transition_window.grid_columnconfigure(j, weight=1)

def define_afn():
    global etats, init, accept, transitions, automate_type
    automate_type = "AFN"
    etats_count = simpledialog.askinteger("Nombre d'états", "Entrez le nombre d'états :")
    if etats_count is None:
        return
    
    etats = set(range(1, etats_count + 1))
    
    init_str = simpledialog.askstring("États initiaux", "Entrez les états initiaux séparés par des virgules :")
    if init_str:
        init_states = map(int, init_str.split(','))
        if any(state not in etats for state in init_states):
            messagebox.showerror("Erreur", "Les états initiaux doivent appartenir aux états définis.")
            return
        init = set(init_states)
    else:
        messagebox.showerror("Erreur", "Veuillez saisir au moins un état initial.")
        return
    
    accept_str = simpledialog.askstring("États acceptants", "Entrez les états acceptants séparés par des virgules :")
    if accept_str:
        accept = set(map(int, accept_str.split(',')))
        if not accept.issubset(etats):
            messagebox.showerror("Erreur", "Les états acceptants doivent appartenir aux états définis.")
            return
    else:
        accept = set()
    
    
    # Créer une fenêtre pop-up pour dessiner la table de transition et saisir les transitions
    transition_window = tk.Toplevel()
    transition_window.title("Table de transition")
    transition_window.geometry("400x300")

    # Couleurs
    label_color = "lightgrey"
    cell_color = "white"
    header_color = "lightblue"
    accept_color = "lightgreen"  # Couleur pour les états acceptants
    
    # Créer une table de transition avec des cases vides
    table = [[None for _ in range(len(alphabet) + 1)] for _ in range(len(etats) + 1)]
    
    # Remplir la première ligne avec les symboles de l'alphabet
    for j, symbol in enumerate(alphabet):
        label = tk.Label(transition_window, text=symbol, bg=header_color, padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=0, column=j + 1, sticky="nsew")
    
    # Remplir la première colonne avec les états
    for i, state in enumerate(etats):
        bg_color = accept_color if state in accept else header_color
        label = tk.Label(transition_window, text=state, bg=bg_color, padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=i + 1, column=0, sticky="nsew")
        
        # Ajouter une flèche devant l'état initial
        if state == init:
            arrow_label = tk.Label(transition_window, text="→", bg=bg_color)
            arrow_label.grid(row=i + 1, column=0, sticky="nse")
    
    # Fonction pour saisir les transitions dans la table
    def enter_transitions(transitions):
        try:
            for i in range(1, len(etats) + 1):
                for j in range(1, len(alphabet) + 1):
                    cell_value = cells[i][j].get()
                    if cell_value:
                        next_state = int(cell_value)
                        if next_state not in etats:
                            messagebox.showerror("Erreur", f"L'état {next_state} n'est pas un état valide.")
                            return
                        transitions[(table[i][0], table[0][j])] = next_state
            transition_window.destroy()
            messagebox.showinfo("Succès", "Automate défini avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des nombres entiers pour les transitions.")
    
    # Créer les champs de saisie pour les transitions
    cells = []
    for i in range(len(etats) + 1):
        row = []
        for j in range(len(alphabet) + 1):
            if i == 0 or j == 0:
                label = tk.Label(transition_window, text=table[i][j], bg=header_color, padx=10, pady=5, borderwidth=1, relief="solid")
                row.append(label)
            else:
                entry = tk.Entry(transition_window, bg=cell_color, borderwidth=1, relief="solid")
                entry.grid(row=i, column=j, sticky="nsew")
                row.append(entry)
        cells.append(row)
    
    # Bouton pour valider les transitions
    btn_enter = tk.Button(transition_window, text="Valider", command=lambda: enter_transitions(transitions))
    btn_enter.grid(row=len(etats) + 2, columnspan=len(alphabet) + 1, pady=10)

    # Bouton pour compléter l'automate
    btn_completer = tk.Button(transition_window, text="Compléter", command=lambda: completer((etats, alphabet, transitions, init, accept)))
    btn_completer.grid(row=len(etats) + 3, columnspan=len(alphabet) + 1, pady=10)

    # Bouton pour émonder l'automate
    btn_emonder = tk.Button(transition_window, text="Émonder", command=lambda: emonder((etats, alphabet, transitions, init, accept)))
    btn_emonder.grid(row=len(etats) + 4, columnspan=len(alphabet) + 1, pady=10)
    
    # Bouton pour determiniser l'automate
    btn_déterminiser = tk.Button(transition_window, text="Déterminiser", command=lambda: déterminise((etats, alphabet, transitions, init, accept)))
    btn_déterminiser.grid(row=len(etats) + 5, columnspan=len(alphabet) + 1, pady=10)

    # Configurer les poids des lignes et des colonnes pour le redimensionnement
    for i in range(len(etats) + 1):
        transition_window.grid_rowconfigure(i, weight=1)
    for j in range(len(alphabet) + 1):
        transition_window.grid_columnconfigure(j, weight=1)
def define_automaton():
    # Créer la fenêtre principale pour choisir entre un AFD et un AFN
    main_window = tk.Toplevel()
    main_window.title("Choix du Type d'Automate")
    
    # Définir la taille de la fenêtre principale
    main_window.geometry("300x200")  # Ajustez la taille selon vos besoins
    
    # Fonction pour fermer la fenêtre principale
    def close_main_window():
        main_window.destroy()
    
    # Bouton pour définir un AFD
    btn_afd = tk.Button(main_window, text="Définir un AFD", command=lambda: [define_afd(), close_main_window()])
    btn_afd.pack(pady=10)
    
    # Bouton pour définir un AFN
    btn_afn = tk.Button(main_window, text="Définir un AFN", command=lambda: [define_afn(), close_main_window()])
    btn_afn.pack(pady=10)

def completer(aut):
    etats, alphabet, transitions, init, accept = aut
    
    # Vérifier si l'automate est déjà complet
    est_complet = all((etat,symbole) in transitions for etat in etats for symbole in alphabet)
    
    # Si l'automate est déjà complet, retourner l'automate d'origine
    if est_complet:
        return aut
    
    # Créer une copie des transitions existantes
    nouvelles_transitions = transitions.copy()
    
    # Ajouter un nouvel état fictif à l'ensemble des états existants
    nouvel_etat = max(etats) + 1
    nouveaux_etats = etats | {nouvel_etat}
    
    # Ajouter des transitions manquantes pour chaque état et chaque symbole de l'alphabet
    for etat in nouveaux_etats:
        for symbole in alphabet:
            # Vérifier si une transition est déjà définie pour l'état et le symbole
            if (etat,symbole) not in transitions:
                # Ajouter une transition vers l'état fictif
                nouvelles_transitions[(etat,symbole)] = nouvel_etat
    
    # Retourner l'automate complet avec les transitions ajoutées et le nouvel état fictif
    return (nouveaux_etats, alphabet, nouvelles_transitions, init, accept)

def coAccessible(aut):
    (etats, alphabet, T, init, Ac) = aut
    
    # Ensemble des états co-accessibles
    etats_co_accessibles = set(Ac) 
    
    # File pour le parcours en largeur
    file = list(Ac)  
    
    for etat_courant in file:
        for transition, etat_suivant in T.items(): 
            if etat_suivant == etat_courant and transition[0] not in etats_co_accessibles:
                etats_co_accessibles.add(transition[0])  
                file.append(transition[0])  
                    
    return etats_co_accessibles
    
def accessible(aut):
    etats, alphabet, transitions, init, accept = aut

    # Initialiser l'ensemble des états accessibles avec l'état initial
    etats_accessibles = {init}
    
    # File pour stocker les états à explorer
    file = [init]
    file_pop = 0
    
    # Parcours en largeur à partir de l'état initial
    while file_pop < len(file):
        etat_courant = file[file_pop]
        file_pop += 1
        # Parcourir les transitions sortantes de l'état courant
        for symbole in alphabet:
            if (etat_courant, symbole) in transitions:
                etat_suivant = transitions[(etat_courant, symbole)]
                # Ajouter l'état suivant à l'ensemble des états accessibles s'il n'a pas déjà été visité
                if etat_suivant not in etats_accessibles:
                    etats_accessibles.add(etat_suivant)
                    file.append(etat_suivant)
    
    return etats_accessibles


def emonder(aut):
    # Trouver les états accessibles et co-accessibles
    accessibles = accessible(aut)
    co_accessibles = coAccessible(aut)
    
    # Intersection des états accessibles et co-accessibles
    états_émondés = accessibles.intersection(co_accessibles)
    print(états_émondés)
    
    # Renommer les états émondés en utilisant un dictionnaire
    états_renommés = {etat: i+1 for i, etat in enumerate(états_émondés)}
    print(set(états_renommés.values()))
    print(états_renommés)
    
    # Récupérer les états acceptants émondés
    accept_emondé = {états_renommés[etat] for etat in aut[4] if etat in états_émondés}
    print(accept_emondé)
    
    # Filtrer les transitions pour ne garder que celles dont les deux états sont émondés
    transitions_émondées = {(états_renommés[transition[0]], transition[1]): états_renommés[état_suivant] for transition, état_suivant in aut[2].items() if transition[0] in états_émondés and état_suivant in états_émondés}
    
    # Retourner l'automate émondé équivalent
    return (set(range(1, len(états_émondés) + 1)), aut[1], transitions_émondées, états_renommés[aut[3]], {états_renommés[etat] for etat in aut[4] if etat in états_émondés})

def déterminise(aut):
    (etats, alphabet, transitions, init, accept) = aut
    
    # Initialiser les nouvelles structures de données
    nouveaux_etats = set()  # Ensemble des nouveaux états de l'AFD
    nouvelles_transitions = {}  # Dictionnaire des nouvelles transitions de l'AFD
    nouveaux_accept = set()  # Ensemble des nouveaux états acceptants de l'AFD
    
    # Initialiser la file pour le parcours en largeur
    file = [set(init)]  # Ajouter l'ensemble contenant l'état initial
    nouveaux_etats.add(tuple(set(init)))
    
    # Liste pour stocker les états de l'AFD
    liste_etats_afd = [set(init)]
    
    # Parcourir chaque état de l'AFD à partir de l'état initial
    while file:
        etat_courant = file.pop(0)
        # Vérifier si l'état courant contient un état acceptant de l'AFN
        if any(e in accept for e in etat_courant):
            nouveaux_accept.add(tuple(etat_courant))
        # Parcourir chaque symbole de l'alphabet
        for symbole in alphabet:
            etat_suivant = set()  # Ensemble des états atteints avec le symbole courant
            # Pour chaque état de l'ensemble courant, trouver les états atteints avec le symbole courant
            for e in etat_courant:
                if (e, symbole) in transitions:
                    etat_suivant.update(transitions[(e, symbole)])
            # Ajouter les transitions de l'AFD
            if etat_suivant:
                if tuple(etat_suivant) not in nouveaux_etats:
                    nouveaux_etats.add(tuple(etat_suivant))
                    file.append(etat_suivant)
                    liste_etats_afd.append(etat_suivant)
                nouvelles_transitions[(tuple(etat_courant), symbole)] = tuple(etat_suivant)
                
    # Créer une bijection en renommant les états de l'AFD
    bijection = {tuple(etat): i+1 for i, etat in enumerate(liste_etats_afd)}
    
    # Remplacer les nouvelles transitions par la bijection
    nouvelles_transitions = {(bijection[etat], symbole): bijection[etat_suivant] for (etat, symbole), etat_suivant in nouvelles_transitions.items()}
    nouveaux_accept = {bijection[etat] for etat in nouveaux_accept}
    init = bijection[tuple(set(init))]
    
    print('Liste des états :')
    print(liste_etats_afd)
    # Retourner l'AFD résultant et la liste des états
    return set(bijection.values()), alphabet, nouvelles_transitions, {init}, nouveaux_accept
 




def simulate_reading():
    try:
        word = entry_input_word.get()
        if not word:
            messagebox.showwarning("Attention", "Veuillez saisir un mot à lire.")
            return
        
        current_state = init
        tape = [(current_state, '')]
        
        
        # Fonction pour mettre à jour la machine à ruban et l'état courant
        def update_tape_and_state(symbol):
            nonlocal current_state
            # current_state = transitions[(current_state, symbol)] #######################################""
            tape.append((current_state, symbol))
            draw_tape(word)  # Passer le mot à la fonction draw_tape
            if current_state in accept:
                messagebox.showinfo("Résultat", "Le mot est accepté.")
            else:
                messagebox.showinfo("Résultat", "Le mot est rejeté.")
        
        # Fonction pour lire le mot lettre par lettre avec un délai
        def read_word():
            for symbol in word:
                update_tape_and_state(symbol)
                root.after(500)  # Délai en millisecondes
            root.after(1000, lambda: messagebox.showinfo("Fin de la lecture", "Lecture terminée."))
        
        read_word()
    except KeyError:
        messagebox.showerror("Erreur", f"Aucune transition définie pour l'état {current_state} avec ce symbole .")

def draw_tape(word):  # Accepter le mot en tant que paramètre
    canvas.delete("all")
    for i, (state, symbol) in enumerate(tape):
        canvas.create_text(50 + i * 50, 50, text=f"q{state}")
        canvas.create_text(50 + i * 50, 70, text=symbol)
    # canvas.create_line(20, 20, 20, 80 + len(tape) * 20, arrow=tk.LAST)
    # canvas.create_line(20, 20, 70 + len(word) * 50, 20, arrow=tk.LAST)  # Utiliser le mot passé en paramètre


root = tk.Tk()
root.title("Simulateur d'Automate Fini")

# Menu pour modifier l'alphabet
menu_bar = tk.Menu(root)
alphabet_menu = tk.Menu(menu_bar, tearoff=0)
alphabet_menu.add_command(label="Modifier l'alphabet", command=set_alphabet)
menu_bar.add_cascade(label="Alphabet", menu=alphabet_menu)
root.config(menu=menu_bar)

label_input_word = tk.Label(root, text="Mot à lire :")
label_input_word.grid(row=0, column=0, padx=10, pady=10)
entry_input_word = tk.Entry(root)
entry_input_word.grid(row=0, column=1, padx=10, pady=10)

btn_define_automaton = tk.Button(root, text="Définir Automate", command=define_automaton)
btn_define_automaton.grid(row=0, column=2, padx=10, pady=10)

btn_simulate = tk.Button(root, text="Simuler Lecture", command=simulate_reading)
btn_simulate.grid(row=0, column=3, padx=10, pady=10)

canvas = Canvas(root, width=800, height=200)
canvas.grid(row=1, columnspan=4)

tape = []

root.mainloop()
