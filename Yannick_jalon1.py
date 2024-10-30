
import tkinter as tk
from tkinter import messagebox, simpledialog

# Fonction pour créer l'automate à partir des entrées utilisateur
def create_automaton():
    try:
        # Récupérer les informations saisies par l'utilisateur
        etats = set(map(int, entry_states.get().split(',')))
        alphabet = entry_alphabet.get().split(',')
        init = int(entry_initial_state.get())
        accept = set(map(int, entry_accepting_states.get().split(',')))
        
        # Demander à l'utilisateur de saisir les transitions à l'aide de la table
        transitions = {}
        for state in etats:
            for symbol in alphabet:
                next_state = simpledialog.askinteger("Transitions", f"Transition de l'état {state} avec le symbole '{symbol}':")
                transitions[(state, symbol)] = next_state
                
        # Créer l'automate et afficher un message de succès
        automaton = (etats, alphabet, transitions, init, accept)
        messagebox.showinfo("Succès", "Automate créé avec succès!")
        return automaton
    except Exception as e:
        # En cas d'erreur, afficher un message d'erreur
        messagebox.showerror("Erreur", f"Erreur lors de la création de l'automate : {e}")

# Fonction pour simuler l'automate avec un mot donné
def simulate():
    try:
        # Récupérer le mot à analyser
        word = entry_input_word.get()
        # Créer l'automate à partir des entrées utilisateur
        automaton = create_automaton()
        if automaton is None:
            return
        
        # Extraire les informations de l'automate
        etats, alphabet, transitions, init, accept = automaton
        
        # Initialiser l'état courant à l'état initial de l'automate
        current_state = init
        # Initialiser le ruban (trace de lecture)
        tape = []
        
        # Parcourir chaque symbole du mot
        for symbol in word:
            # Vérifier si une transition est définie pour l'état courant et le symbole actuel
            if (current_state, symbol) not in transitions:
                messagebox.showerror("Erreur", f"Aucune transition définie pour l'état {current_state} avec le symbole '{symbol}'.")
                return
            
            # Mettre à jour l'état courant et ajouter la transition au ruban
            next_state = transitions[(current_state, symbol)]
            tape.append((symbol, next_state))
            current_state = next_state
        
        # Vérifier si l'état courant est un état acceptant
        if current_state in accept:
            result = "Accepté"
        else:
            result = "Rejeté"
        
        # Créer une chaîne représentant le ruban (trace de lecture)
        tape_str = " ".join([f"({symbol}, {state})" for symbol, state in tape])
        # Afficher la chaîne de ruban et le résultat (accepté ou rejeté)
        ruban.config(text=tape_str + " " + result)
    except Exception as e:
        # En cas d'erreur, afficher un message d'erreur
        messagebox.showerror("Erreur", f"Erreur lors de la simulation : {e}")

# Création de la fenêtre principale Tkinter
root = tk.Tk()
root.title("JALON 1 : Simulateur d'automate fini")

# Création des étiquettes et des champs de saisie pour les informations de l'automate
label_states = tk.Label(root, text="États (séparés par des virgules):")
label_states.grid(row=0, column=0, sticky="w")
entry_states = tk.Entry(root)
entry_states.grid(row=0, column=1)

label_alphabet = tk.Label(root, text="Alphabet (séparé par des virgules):")
label_alphabet.grid(row=1, column=0, sticky="w")
entry_alphabet = tk.Entry(root)
entry_alphabet.grid(row=1, column=1)

label_initial_state = tk.Label(root, text="État initial:")
label_initial_state.grid(row=2, column=0, sticky="w")
entry_initial_state = tk.Entry(root)
entry_initial_state.grid(row=2, column=1)

label_accepting_states = tk.Label(root, text="États acceptants (séparés par des virgules):")
label_accepting_states.grid(row=3, column=0, sticky="w")
entry_accepting_states = tk.Entry(root)
entry_accepting_states.grid(row=3, column=1)

# Bouton pour créer l'automate
btn_create_automaton = tk.Button(root, text="Créer Automate", command=create_automaton)
btn_create_automaton.grid(row=4, columnspan=2)

# Étiquette et champ de saisie pour le mot à analyser
label_input_word = tk.Label(root, text="Mot à analyser:")
label_input_word.grid(row=5, column=0, sticky="w")
entry_input_word = tk.Entry(root)
entry_input_word.grid(row=5, column=1)

# Bouton pour simuler l'automate avec le mot donné
btn_simulate = tk.Button(root, text="Simuler", command=simulate)
btn_simulate.grid(row=6, columnspan=2)

# Étiquette pour afficher le ruban (trace de lecture)
ruban = tk.Label(root, text="", borderwidth=2, relief="ridge")
ruban.grid(row=7, columnspan=2)

# Lancement de la boucle principale Tkinter
root.mainloop()

