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

def define_automaton():
    global etats, init, accept, transitions
    try:
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
        
        # Créer une table de transition avec des cases vides
        table = [[None for _ in range(len(alphabet) + 1)] for _ in range(len(etats) + 1)]
        
        # Remplir la première ligne avec les symboles de l'alphabet
        for j, symbol in enumerate(alphabet):
            table[0][j + 1] = symbol
        
        # Remplir la première colonne avec les états
        for i, state in enumerate(etats):
            table[i + 1][0] = state
        
        # Fonction pour saisir les transitions dans la table
        def enter_transitions():
            global transitions
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
                    label = tk.Label(transition_window, text=table[i][j])
                    row.append(label)
                else:
                    entry = tk.Entry(transition_window)
                    entry.grid(row=i, column=j)
                    row.append(entry)
            cells.append(row)
        
        # Bouton pour valider les transitions
        btn_enter = tk.Button(transition_window, text="Valider", command=enter_transitions)
        btn_enter.grid(row=len(etats) + 2, columnspan=len(alphabet) + 1)

        # Bouton pour compléter l'automate
        btn_completer = tk.Button(transition_window, text="Compléter", command=completer)
        btn_completer.grid(row=len(etats) + 3, columnspan=len(alphabet) + 1)

        # Bouton pour émonder l'automate
        btn_emonder = tk.Button(transition_window, text="Émonder", command=emonder)
        btn_emonder.grid(row=len(etats) + 4, columnspan=len(alphabet) + 1)
        
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez saisir un nombre entier pour le nombre d'états.")

def complet(aut):
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

def emonderr(aut):
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

def completer():
    global etats, alphabet, transitions, init, accept
    # Completer l'automate
    complet()
    # Mettre à jour l'affichage

def emonder():
    global etats, alphabet, transitions, init, accept
    # Émonder l'automate
    emonderr()
    # Mettre à jour l'affichage

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
            current_state = transitions[(current_state, symbol)]
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
        messagebox.showerror("Erreur", f"Aucune transition définie pour l'état {current_state} avec le symbole '{symbol}'.")

def draw_tape(word):  # Accepter le mot en tant que paramètre
    canvas.delete("all")
    for i, (state, symbol) in enumerate(tape):
        canvas.create_text(50 + i * 50, 50, text=f"q{state}")
        canvas.create_text(50 + i * 50, 70, text=symbol)
    canvas.create_line(20, 20, 20, 80 + len(tape) * 20, arrow=tk.LAST)
    canvas.create_line(20, 20, 70 + len(word) * 50, 20, arrow=tk.LAST)  # Utiliser le mot passé en paramètre


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
