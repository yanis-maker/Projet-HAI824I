import rdflib
import tkinter as tk
from tkinter import filedialog

import command

def validerSource():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier source")
  sourceEntree.delete(0, tk.END)
  sourceEntree.insert(0, filepath)


def validerCible():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier cible")
  cibleEntree.delete(0, tk.END)
  cibleEntree.insert(0, filepath)


def validerAlign():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier d'alignement")
  cibleEntree.delete(0, tk.END)
  cibleEntree.insert(0, filepath)


def validerSeuil():
  valeurSeuil = seuilEntree.get()
  print(valeurSeuil)

root = tk.Tk()
root.title("Outil intégration de données")

canvas=tk.Canvas(root,height=500,width=500,bg="#263D42")
canvas.pack()

# Fichier source
labelSource = tk.Label(canvas, text="Fichier source :", bg="white")
canvas.create_window(60, 20, window=labelSource)
sourceEntree = tk.Entry(canvas, bg="white", width=50)
canvas.create_window(260, 20, window=sourceEntree)
sourceValider = tk.Button(canvas,
                          text="Add",
                          width=5,
                          height=1,
                          command=validerSource)
canvas.create_window(450, 20, window=sourceValider)

# Fichier cible
labelCible = tk.Label(canvas, text="Fichier cible :", bg="white")
canvas.create_window(60, 50, window=labelCible)
cibleEntree = tk.Entry(canvas, bg="white", width=50)
canvas.create_window(260, 50, window=cibleEntree)
cibleValider = tk.Button(canvas,
                         text="Add",
                         width=5,
                         height=1,
                         command=validerCible)
canvas.create_window(450, 50, window=cibleValider)

# Alignement
labelAlign = tk.Label(canvas, text="Fichier cible :", bg="white")
canvas.create_window(60, 80, window=labelAlign)
alignEntree = tk.Entry(canvas, bg="white", width=50)
canvas.create_window(260, 80, window=alignEntree)
alignValider = tk.Button(canvas,
                         text="Add",
                         width=5,
                         height=1,
                         command=validerAlign)
canvas.create_window(450, 80, window=alignValider)

# Seuil
labelSeuil = tk.Label(canvas, text="Seuil :", bg="white")
canvas.create_window(70, 300, window=labelSeuil)
seuilEntree = tk.Entry(canvas, bg="white", width=7)
canvas.create_window(120, 300, window=seuilEntree)
seuilValider = tk.Button(canvas,
                         text="Add",
                         width=5,
                         height=1,
                         command=validerSeuil)
canvas.create_window(170, 300, window=seuilValider)





propretyButton=tk.Button(canvas, text="Choix des propriétés", bg="white", command=command.propApp)
canvas.create_window(120,200,window=propretyButton)

mesuresButton=tk.Button(canvas,text="Choix des mesures",bg="white")
canvas.create_window(350,200,window=mesuresButton)

confirmButton=tk.Button(root,text="Confirmer")
confirmButton.pack()

root.mainloop()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
