import rdflib
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.ttk import *
import tkinter.ttk as ttk

import command
import bridge
import parseRdf

pont = bridge.Bridge()

propertySelected = []


def selectionProp():
    select = listbox_properties.get()
    if(select not in propertySelected):
      propertySelected.append(select)
      varProperties.set("\n".join(propertySelected))
      #label_propSelected.config(text="Propriétés sélectionnées :\n" + varProperties.get())
      listbox_propSelect['values'] = propertySelected
      print("Vous avez sélectionné : ", propertySelected)

def validerSource():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier source")
  sourceEntree.delete(0, tk.END)
  sourceEntree.insert(0, filepath)
  pont.setFichierSource(filepath)


def validerCible():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier cible")
  cibleEntree.delete(0, tk.END)
  cibleEntree.insert(0, filepath)
  pont.setFichierCible(filepath)


def validerAlign():
  filepath = filedialog.askopenfilename(title="Ouvrir un fichier d'alignement")
  cibleEntree.delete(0, tk.END)
  cibleEntree.insert(0, filepath)
  pont.setFichierAlign(filepath)


def validerSeuil():
  valeurSeuil = seuilEntree.get()
  pont.setSeuil(valeurSeuil)


def on_checked(checkbox_var, checkbox_int):
    if checkbox_var.get():
        pont.addListSimilarity(checkbox_int)


root = tk.Tk()
root.title("Outil intégration de données")

canvas = tk.Canvas(root, height=500, width=500, bg="#263D42")
canvas.pack()

# Fichier source
labelSource = tk.Label(canvas, text="Fichier source :", bg="#263D42", fg="#FFFF00")
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
labelCible = tk.Label(canvas, text="Fichier cible :", bg="#263D42", fg="#FFFF00")
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
labelAlign = tk.Label(canvas, text="Fichier cible :", bg="#263D42", fg="#FFFF00")
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
labelSeuil = tk.Label(canvas, text="Seuil :", bg="#263D42", fg="#FFFF00")
canvas.create_window(70, 300, window=labelSeuil)
seuilEntree = tk.Entry(canvas, bg="white", width=7)
canvas.create_window(120, 300, window=seuilEntree)
seuilValider = tk.Button(canvas,
                         text="Add",
                         width=5,
                         height=1,
                         command=validerSeuil)
canvas.create_window(170, 300, window=seuilValider)

#propretyButton = tk.Button(canvas,
#                           text="Choix des propriétés",
#                           bg="white",
#                           command=command.propApp)
#canvas.create_window(120, 200, window=propretyButton)

# Création du texte "choix des propriétés"
label_properties = tk.Label(root, text="Choix des propriétés :", bg="#263D42", fg="#FFFF00")
canvas.create_window(120, 200,window=label_properties)
#label_properties.pack()

# Création de la liste déroulante contenant les propriétés communes
listbox_properties = combo = ttk.Combobox(root, values=parseRdf.getAllProperty())
canvas.create_window(120, 220,window=listbox_properties)

varProperties = StringVar()
#label_propSelected = tk.Label(root, text="Propriétés selectionné : \n"+varProperties.get(), bg="#263D42", fg="#FFFF00")
label_propSelected = tk.Label(root, text="Propriétés selectionné : ", bg="#263D42", fg="#FFFF00")
canvas.create_window(120, 240,window=label_propSelected)

listbox_propSelect = ttk.Combobox(root, values = propertySelected)
canvas.create_window(120, 260,window=listbox_propSelect)
#Bouton pour ajouter une propriété a selectionner
addPorpertyButton = tk.Button(canvas, text="Add", bg="white", command=selectionProp)
canvas.create_window(210, 220, window=addPorpertyButton)


varIdentity = tk.BooleanVar()
varQgrams = tk.BooleanVar()
varJaccard = tk.BooleanVar()
varJaro = tk.BooleanVar()
varJaroWinkler = tk.BooleanVar()
varLevenshtein = tk.BooleanVar()
varMongeElkan = tk.BooleanVar()

# A faire dans une boucle car plus propre si le temps
checkIdentity = tk.Checkbutton(canvas, text="Identity",
                               variable=varIdentity,
                               bg="#263D42", fg="#FFFF00",
                               command=lambda: on_checked(varIdentity, 2))
canvas.create_window(350, 200, window=checkIdentity)

checkQgrams = tk.Checkbutton(canvas, text="Qgrams",
                             variable=varQgrams,
                             bg="#263D42", fg="#FFFF00",
                             command=lambda: on_checked(varQgrams, 4))
canvas.create_window(350, 220, window=checkQgrams)

checkJaccard = tk.Checkbutton(canvas, text="Jaccard",
                              variable=varJaccard,
                              bg="#263D42", fg="#FFFF00",
                              command=lambda: on_checked(varJaccard, 6))
canvas.create_window(350, 240, window=checkJaccard)

checkJaro = tk.Checkbutton(canvas, text="Jaro",
                           variable=varJaro,
                           bg="#263D42", fg="#FFFF00",
                           command=lambda: on_checked(varJaro, 0))
canvas.create_window(350, 260, window=checkJaro)

checkJaroWinkler = tk.Checkbutton(canvas,
                                  text="JaroWinkler",
                                  bg="#263D42", fg="#FFFF00",
                                  variable=varJaroWinkler,
                                  command=lambda: on_checked(varJaroWinkler, 1))
canvas.create_window(350, 280, window=checkJaroWinkler)

checkLevenshtein = tk.Checkbutton(canvas,
                                  text="Levenshtein",
                                  variable=varLevenshtein,
                                  bg="#263D42", fg="#FFFF00",
                                  command=lambda: on_checked(varLevenshtein, 3))
canvas.create_window(350, 300, window=checkLevenshtein)

checkMongeElkan = tk.Checkbutton(canvas,
                                 text="Monge-Elkan",
                                 variable=varMongeElkan,
                                 bg="#263D42", fg="#FFFF00",
                                 command=lambda: on_checked(varMongeElkan, 5))
canvas.create_window(350, 320, window=checkMongeElkan)

confirmButton = tk.Button(root, text="Confirmer")
confirmButton.pack()

root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
