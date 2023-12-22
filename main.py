import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Text, Button
import json
import os

def load_kluizen(): # laad kluizen.json
    try:
        with open('kluizen.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_kluizen(kluizen): # slaat kluizen op
    with open('kluizen.json', 'w') as file:
        json.dump(kluizen, file, indent=4)

def kluis_kiezen(kluisnummer, kluizen): # functie om gebruiker bestaande kluis te kiezen en ww te laten invullen
    if kluisnummer in kluizen:
        code = simpledialog.askstring("Kluis Openen", f"Voer wachtwoord in voor kluis {kluisnummer}:")
        if code == kluizen[kluisnummer]:
            kluis_options(kluisnummer, kluizen, code)
        else:
            messagebox.showerror("Fout", "Verkeerde wachtwoord!")
    else:
        nieuwe_kluis(kluisnummer, kluizen)

def nieuwe_kluis(kluisnummer, kluizen): # functie om nieuwe kluis aan te maken
    code = simpledialog.askstring("Nieuwe Kluis", "Voer een code in voor de kluis (minimaal 4 tekens):")
    if code and len(code) >= 4:
        kluizen[kluisnummer] = code
        save_kluizen(kluizen)
        update_kluis_display(window, kluizen)
    else:
        messagebox.showerror("Ongeldige Code", "De ingevoerde code is niet geldig. Probeer het opnieuw.")

def kluis_options(kluisnummer, kluizen, code): # functie om opties te geven voor een bestaande kluis (kluis openen, kluis teruggeven)
    def open_kluis():
        top.destroy()
        edit_kluis_file(kluisnummer)

    def geef_kluis_terug(): # kluis teruggeven: verwijderd kluis uit kluizen.json en verwijderd bestand voor kluis (kluis_x.txt)
        if simpledialog.askstring("Kluis Teruggeven", "Voer uw wachtwoord nogmaals in:") == code:
            del kluizen[kluisnummer]
            save_kluizen(kluizen)
            update_kluis_display(window, kluizen)
            try:
                os.remove(f"kluizen/kluis_{kluisnummer}.txt")
            except FileNotFoundError:
                pass
        else:
            messagebox.showerror("Fout", "Verkeerd wachtwoord!")
        top.destroy()

    top = Toplevel()
    top.title(f"Kluis {kluisnummer} Opties")
    Button(top, text="Kluis Teruggeven", command=geef_kluis_terug).pack()
    Button(top, text="Kluis Openen", command=open_kluis).pack()

def edit_kluis_file(kluisnummer): # functie om bestand voor kluis te openen (kluis_x.txt) en te bewerken
    top = Toplevel()
    top.title(f"Kluis {kluisnummer} Inhoud")
    text = Text(top)
    text.pack(expand=True, fill='both')
    
    kluis_file_path = f"kluizen/kluis_{kluisnummer}.txt"
    
    try:
        with open(kluis_file_path, 'r') as file:
            text.insert('1.0', file.read())
    except FileNotFoundError:
        pass

    def save_and_close():
        with open(kluis_file_path, 'w') as file:
            file.write(text.get("1.0", "end-1c"))
        top.destroy()

    Button(top, text="Opslaan en Sluiten", command=save_and_close).pack() # slaat bestand op, en sluit het vervolgens
    Button(top, text="Sluiten (Niet Opslaan)", command=top.destroy).pack() # sluit bestand zonder op te slaan

def update_kluis_display(window, kluizen):
    for i in range(1, 13):
        frame = tk.Frame(window, borderwidth=2, relief="ridge", width=150, height=150, bg="darkgrey")
        frame.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
        label = tk.Label(frame, text=f"Kluis {i}\n{'Bezet' if i in kluizen else 'Vrij'}", bg="darkgrey", fg="white")
        label.pack(expand=True, fill='both')
        frame.bind("<Button-1>", lambda event, k=i: kluis_kiezen(k, kluizen))
        label.bind("<Button-1>", lambda event, k=i: kluis_kiezen(k, kluizen))

def main_menu():
    global window
    window = tk.Tk()
    window.title("Bagagekluis Verhuursysteem")
    window.configure(bg="black")
    kluizen = load_kluizen()
    update_kluis_display(window, kluizen)
    window.mainloop()

if __name__ == "__main__":
    main_menu()