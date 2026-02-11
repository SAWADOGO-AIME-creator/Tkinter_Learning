import tkinter as tk
import requests
from bs4 import BeautifulSoup

def research_func():
    result.delete(0, tk.END) #efface les résultats précédents
    user_input = entry_toSearch.get()
    site= f"https://fr.wikipedia.org/wiki/{user_input}" 
    result.insert(tk.END, f"##### {user_input} - EN BREF #####\n")

    headers = {
        "User-Agent": "WebRadioApp/1.0 (contact: aimefictif@gmail.com)"
    }
    page_actu = requests.get(site, headers=headers)
    soup=BeautifulSoup(page_actu.text,"html.parser")

    x=soup.find(name="h2", string="En bref")
    #print(x) testons
    try:
        enbref_list_ul=x.find_next(name="ul")
        enbref_list_li=enbref_list_ul.find_all(name="li")
        
        for i in enbref_list_li:
            #print(i.text) testons
            result.insert(tk.END, i.text)
        
    except:
        result.insert(tk.END, f"/!\ Aucun résultat trouvé pour {user_input}.")


    #musique *********************
    site= f"https://fr.wikipedia.org/wiki/{user_input}_en_musique" 
    result.insert(tk.END, f"##### {user_input} - EN MUSIQUE #####\n")
    headers = {
        "User-Agent": "WebRadioApp/1.0 (contact: aimefictif@gmail.com)"
    }
    page_music= requests.get(site, headers=headers)
    soup=BeautifulSoup(page_music.text,"html.parser")

    music=soup.find(name="h3", string="En France")
    #print(x) testons
    try:
        en_music_list_ul=music.find_next(name="ul")
        en_music_list_li=en_music_list_ul.find_all(name="li")
        
        for i in en_music_list_li:
            #print(i.text) testons
            result.insert(tk.END, i.text)
        
    except:
        result.insert(tk.END, f"/!\ Aucun résultat trouvé pour {user_input}.")



#creation de la fenetre principale responsive
app = tk.Tk()
app.title("Apprentissaage du WebRadio")
app.minsize(1000, 500)
app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f'{width}x{height}+{x}+{y}')

#mon label
label_title = tk.Label(app, text="GRATAIJE", font=("Segoe Print", 20, "bold"))
label_search = tk.Label(app, text="Rechercher", font=("Arial", 12, ""))
entry_toSearch = tk.Entry(app, font=("Arial", 12), width=30)#aec un plavceholder , placeholder="Entrez une année"
btn_search = tk.Button(app, text="Go", font=("Arial", 12, "bold"), bg="#01152B", fg="#FFFFFF",command=research_func)
result=tk.Listbox(app, font=("Arial", 12), width=150)


#affichage des widgets
label_title.pack(pady=20)
label_search.pack(pady=10)
entry_toSearch.pack(pady=10)
btn_search.pack(pady=10)
result.pack(pady=10,padx=20)






#lancement de l'application
app.mainloop()

