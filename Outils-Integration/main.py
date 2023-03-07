import rdflib as rdf
import tkinter as tk

import command

root = tk.Tk()
root.title("Outils intégration de données")

canvas=tk.Canvas(root,height=500,width=500,bg="#263D42")
canvas.pack()

propretyButton=tk.Button(canvas, text="Choix des propriétés", bg="white", command=command.propApp)
canvas.create_window(250,100,window=propretyButton)

mesuresButton=tk.Button(canvas,text="Choix des mesures",bg="white")
canvas.create_window(250,175,window=mesuresButton)

mesuresButton=tk.Button(canvas,text="Choix du seuil de similarité",bg="white")
canvas.create_window(250,250,window=mesuresButton)

confirmButton=tk.Button(root,text="Confirmer")
confirmButton.pack()

root.mainloop()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
