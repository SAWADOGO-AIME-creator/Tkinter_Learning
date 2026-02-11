import tkinter

maFenetre = tkinter.Tk()
maFenetre.title("Compteur")

compteur = 0

def onClick():
    global compteur
    compteur += 1
    monLabel.config(text=str(compteur))

monLabel = tkinter.Label(maFenetre, text=str(compteur))
monButton = tkinter.Button(maFenetre, text="Compteur", command=onClick)

monLabel.pack()
monButton.pack()

maFenetre.mainloop()