import tkinter as tk


def propApp():
    new_window=tk.Tk()
    new_window.title("Choix des prorpiétés")

    canvas = tk.Canvas(new_window, height=750, width=750, bg="#263D42")
    canvas.pack()

    label=tk.Label(canvas,text="Veuillez cocher les propriétés à comparer",bg="#263D42",fg="white")
    canvas.create_window(250,50,window=label)



    tk.mainloop()
