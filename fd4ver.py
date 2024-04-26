import tkinter as tk

def main():
    # Δημιουργία κύριου παραθύρου
    root = tk.Tk()
    root.title("Μήνυμα")

    # Ρύθμιση του παραθύρου
    root.geometry("300x200")  # Διαστάσεις παραθύρου

    # Δημιουργία ετικέτας με κείμενο
    label = tk.Label(root, text="ΦΔ 4ever", font=("Helvetica", 24, "bold"), fg="red")
    label.pack(expand=True)

    # Εκκίνηση της εφαρμογής
    root.mainloop()

if __name__ == "__main__":
    main()
 

 # CHAT GPT