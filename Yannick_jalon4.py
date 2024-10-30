import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import Canvas

# Variables globales pour stocker les informations de l'automate
etats = set()
alphabet = ['a', 'b']
transitions = {}
init = None
accept = set()
automate_type = None

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
        if state in init:
            arrow_label = tk.Label(transition_window, text="→", bg=bg_color)
            arrow_label.grid(row=i + 1, column=0, sticky="nse")
    
    # Fonction pour saisir les transitions dans la table
    def enter_transitions(transitions):
        try:
            for i in range(1, len(etats) + 1):
                for j in range(1, len(alphabet) + 1):
                    cell_value = cells[i][j].get()
                    if cell_value:
                        next_states = set(map(int, cell_value.split(',')))
                        if not next_states.issubset(etats):
                            messagebox.showerror("Erreur", "Les états suivants doivent appartenir aux états définis.")
                            return
                        transitions[(table[i][0], table[0][j])] = next_states
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

    # Configurer les poids des lignes et des colonnes pour le redimensionnement
    for i in range(len(etats) + 1):
        transition_window.grid_rowconfigure(i, weight=1)
    for j in range(len(alphabet) + 1):
        transition_window.grid_columnconfigure(j, weight=1)

def read_word():
    word = simpledialog.askstring("Lire un mot", "Entrez le mot à lire :")
    if word is None:
        return
    
    if automate_type == "AFD":
        current_state = init
        for symbol in word:
            if (current_state, symbol) in transitions:
                current_state = transitions[(current_state, symbol)]
            else:
                messagebox.showinfo("Résultat", f"Le mot '{word}' est rejeté par l'automate.")
                return
        
        if current_state in accept:
            messagebox.showinfo("Résultat", f"Le mot '{word}' est accepté par l'automate.")
        else:
            messagebox.showinfo("Résultat", f"Le mot '{word}' est rejeté par l'automate.")
    
    elif automate_type == "AFN":
        current_states = init
        for symbol in word:
            next_states = set()
            for state in current_states:
                if (state, symbol) in transitions:
                    next_states.update(transitions[(state, symbol)])
            if not next_states:
                messagebox.showinfo("Résultat", f"Le mot '{word}' est rejeté par l'automate.")
                return
            current_states = next_states
        
        if current_states & accept:
            messagebox.showinfo("Résultat", f"Le mot '{word}' est accepté par l'automate.")
        else:
            messagebox.showinfo("Résultat", f"Le mot '{word}' est rejeté par l'automate.")
    else:
        messagebox.showerror("Erreur", "L'automate n'a pas été défini.")

def complete_automate():
    global transitions, etats, alphabet
    poubelle = max(etats) + 1
    etats.add(poubelle)
    
    for state in etats:
        for symbol in alphabet:
            if (state, symbol) not in transitions:
                transitions[(state, symbol)] = poubelle
            elif automate_type == "AFN" and not transitions[(state, symbol)]:
                transitions[(state, symbol)].add(poubelle)
    
    messagebox.showinfo("Succès", "Automate complété avec succès!")

def prune_automate():
    global transitions, etats, init, accept

    # Trouver les états accessibles
    accessible_states = set()
    stack = list(init) if automate_type == "AFN" else [init]
    while stack:
        state = stack.pop()
        if state not in accessible_states:
            accessible_states.add(state)
            for symbol in alphabet:
                if (state, symbol) in transitions:
                    next_states = transitions[(state, symbol)]
                    if isinstance(next_states, set):
                        stack.extend(next_states)
                    else:
                        stack.append(next_states)
    
    # Garder seulement les états accessibles
    etats = etats & accessible_states
    accept = accept & etats
    transitions = {k: v for k, v in transitions.items() if k[0] in etats}

    messagebox.showinfo("Succès", "Automate émondé avec succès!")

def show_transitions():
    global transitions, etats, alphabet
    
    # Créer une nouvelle fenêtre pour afficher les transitions
    transition_window = tk.Toplevel()
    transition_window.title("Table des transitions")
    transition_window.geometry("400x300")

    # Couleurs
    header_color = "lightblue"
    cell_color = "white"
    accept_color = "lightgreen"  # Couleur pour les états acceptants

    # Créer une table pour les transitions
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
        if (automate_type == "AFD" and state == init) or (automate_type == "AFN" and state in init):
            arrow_label = tk.Label(transition_window, text="→", bg=bg_color)
            arrow_label.grid(row=i + 1, column=0, sticky="nse")

    # Remplir la table avec les transitions
    for (state, symbol), next_state in transitions.items():
        row = list(etats).index(state) + 1
        col = alphabet.index(symbol) + 1
        if isinstance(next_state, set):
            value = ",".join(map(str, next_state))
        else:
            value = str(next_state)
        label = tk.Label(transition_window, text=value, bg=cell_color, padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=row, column=col, sticky="nsew")

    # Configurer les poids des lignes et des colonnes pour le redimensionnement
    for i in range(len(etats) + 1):
        transition_window.grid_rowconfigure(i, weight=1)
    for j in range(len(alphabet) + 1):
        transition_window.grid_columnconfigure(j, weight=1)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Automate Fini")
root.geometry("600x400")

# Création des boutons
btn_set_alphabet = tk.Button(root, text="Définir l'alphabet (si different de a et b !)", command=set_alphabet)
btn_set_alphabet.pack(pady=10)

btn_define_afd = tk.Button(root, text="Définir un AFD", command=define_afd)
btn_define_afd.pack(pady=10)

btn_define_afn = tk.Button(root, text="Définir un AFN", command=define_afn)
btn_define_afn.pack(pady=10)

btn_read_word = tk.Button(root, text="Lire un mot", command=read_word)
btn_read_word.pack(pady=10)

btn_complete = tk.Button(root, text="Compléter l'automate", command=complete_automate)
btn_complete.pack(pady=10)

btn_prune = tk.Button(root, text="Émonder l'automate", command=prune_automate)
btn_prune.pack(pady=10)

btn_show_transitions = tk.Button(root, text="Afficher les transitions", command=show_transitions)
btn_show_transitions.pack(pady=10)

# Lancer la boucle principale
root.mainloop()
