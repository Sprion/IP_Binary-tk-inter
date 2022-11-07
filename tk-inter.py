#permet d'import la librairie
from tkinter import *

#fonction pour voir si l'ip est valide ou non
def validAdress(arr):
    if len(arr) != 4 or any(not i.isnumeric() for i in arr) or any(int(i) > 255 for i in arr): return False
    return True

#fonction pour voir si le masque est valide pour une adresse ipv4
def has_error(mask):
    possible_values = [0, 128, 192, 224, 240, 248, 252, 254, 255]
    if mask[0] != 255 or mask[1] not in possible_values or mask[2] not in possible_values or mask[3] not in possible_values:
        return True
    elif mask[0] < mask[1] or mask[1] < mask[2] or mask[2] < mask[3]:
        return True
    elif (mask[0] < 255 and mask[1] != 0) or (mask[1] < 255 and mask[2] != 0) or (mask[2] < 255 and mask[3] != 0):
        return True
    else:
        return False

#calcul la plage d'adresse
def plage_from_ip(ip, mask):
    magic_number = 256 - (mask[3] if mask[3] != 0 else (mask[2] if mask[2] != 0 else (mask[1] if mask[1] != 0 else mask[0])))
    last_bit = 3 if mask[3] != 0 else (2 if mask[2] != 0 else (1 if mask[1] != 0 else 0))
    significative_bit = ip[last_bit]
    temp = 0;

    while significative_bit >= temp:
        temp += magic_number

    upper_significative_bit = temp - 1
    lower_significative_bit = temp - magic_number

    upper_range = [ip[0], ip[1], ip[2], upper_significative_bit] if last_bit == 3 else [ip[0], ip[1], upper_significative_bit, 255] if last_bit == 2 else [ip[0], upper_significative_bit, 255, 255] if last_bit == 1 else [upper_significative_bit, 255, 255, 255]
    lower_range = [ip[0], ip[1], ip[2], lower_significative_bit] if last_bit == 3 else [ip[0], ip[1], lower_significative_bit, 0] if last_bit == 2 else [ip[0], lower_significative_bit, 0, 0] if last_bit == 1 else [lower_significative_bit, 0, 0, 0]

    return [lower_range, upper_range]

#fonction pour calculer l'adresse ip
def binary(arr):
    return ''.join([bin(int(i))[2:].zfill(8) for i in arr])

#fonction pour calculer etlogique
def etlog(ip, mask):
    return [ip[i] & mask[i] for i in range(4)]

#fonction calcul le nombre de machines
def nbMachines(mask):
    return 2**binary(mask).count('0')-2
    
#fonction pour calculer le cidr 
def CIDR(mask):
    return binary(mask).count('1')
    
#fonction pour définr la classe du réseau 
def classe(ip):
    return "Classe A" if ip[0] < 128 else ("Classe B" if ip[0] < 192 else ("Classe C" if ip[0] < 224 else ("Classe D" if ip[0] < 240 else "Classe E")))

#fonction pour définir si il s'agit d'un réseau public ou privé
def prive(ip):
    if ip[0] == 10 or (ip[0] == 172 and ip[1] in range(16,32)) or (ip[0] == 192 and ip[1] == 168 and ip[2] < 255): return "Privé"
    return "Public"

#fonction pour enlever l'affichage des variables error, LbinaryIP, LbinaryMask, Lplage, Lcidr, Lmachines, Lclass, Lpublic
def clear():
    global error, LbinaryIP, LbinaryMask, Lplage, Lcidr, Lmachines, Lclass, Lpublic
    if error: 
        error.grid_forget()
    if LbinaryIP: 
        LbinaryIP.grid_forget()
    if LbinaryMask: 
        LbinaryMask.grid_forget()
    if Lplage: 
        Lplage.grid_forget()
    if Lcidr: 
        Lcidr.grid_forget()
    if Lmachines: 
        Lmachines.grid_forget()
    if Lclass: 
        Lclass.grid_forget()
    if Lpublic: 
        Lpublic.grid_forget()

#fonction pour calculer toute l'ip
def calcul():
    
    clear()
    global error
    ipText = Eip.get()
    ip = ipText.split('.')
    maskText = Emask.get()
    mask = maskText.split('.')

    #on regarde avec la fonction validadress(ip,mask) si il y a un defaut on arret sinon on passe a la suite
    if not validAdress(ip) or not validAdress(mask):
        error.configure(text = "L'ip ou le mask n'as pas la bonne forme.", fg = "red")
        error.grid(row = 3, column = 0)
        return
    else:
        #on défie le mask et l'ip
        ip = [int(i) for i in ip]
        mask = [int(i) for i in mask]
        
        #avec la fonction has_error on vérifie si le mask est juste 
        if has_error(mask):
            error.configure(text = "Le masque est Invalide.", fg="red")
            error.grid(row = 3, column = 0)
            return
    
    #calcul de la plage
    plage = plage_from_ip(ip, mask)
    plageText = '.'.join([str(i) for i in plage[0]]) + " à " + '.'.join([str(i) for i in plage[1]])

    #affiche l'ip en binaire
    global LbinaryIP
    LbinaryIP.configure(text="L'ip "+ipText+" en binaire est : "+binary(ip))
    LbinaryIP.grid(row = 3, column = 0)

    #affiche le mask en binaire
    global LbinaryMask
    LbinaryMask.configure(text="Le mask "+maskText+" en binaire est : "+binary(mask))
    LbinaryMask.grid(row = 4, column = 0)

    #affiche la classe de l'adresse ip avec la fonction classe(ip)
    global Lclass3
    Lclass.configure(text="L'adresse IP "+ipText+" est une adresse IP de "+classe(ip))
    Lclass.grid(row = 5, column = 0)

    #affiche si il s'agit d'une classe privé ou public
    global Lpublic
    Lpublic.configure(text="L'adresse IP "+ipText+" est une adresse IP : " +prive(ip))
    Lpublic.grid(row = 6, column = 0)

    #affiche le nombre de machine que nous pouvons connecter
    global Lmachines
    Lmachines.configure(text="Dans ce réseau, il est possible d'adresser "+str(nbMachines(mask))+" machines.")
    Lmachines.grid(row = 7, column = 0)
    
    #affiche le cidr
    global Lcidr
    Lcidr.configure(text="La notation CIDR du nom du réseau IP est "+'.'.join([str(i) for i in etlog(ip, mask)])+"/"+str(CIDR(mask))+".")
    Lcidr.grid(row = 8, column = 0)
    
    #affiche la plage 
    global Lplage
    Lplage.configure(text="La plage d'adresse utilisable est de "+plageText+".")
    Lplage.grid(row = 9, column = 0)

    

# Partie avec l'import tkinter
master = Tk()
# Premier label
Title = Label(master, text = "Calculatrice IP")
Title.config(font=("Courier", 20))
Title.grid(row = 0, column = 0)

# second label
l1 = Label(master, text = "Entrer une adresse IP :")
l1.grid(row = 1, column = 0)

# Premier champ de saisie
Eip = Entry(master)
Eip.grid(row = 1, column = 1)

# troixième label
l2 = Label(master, text = "Entrer le masque du réseau :")
l2.grid(row = 2, column = 0)

# Deuxième champ de saisie
Emask = Entry(master)
Emask.grid(row = 2, column = 1)

# Initialisation des résultats
Lplage = Label(master, text = "")
Lcidr = Label(master, text = "")
LbinaryIP = Label(master, text = "")
LbinaryMask = Label(master, text = "")
Lmachines = Label(master, text = "")
Lclass = Label(master, text = "")
Lpublic = Label(master, text = "")
error = Label(master, text = "")

# Les deux boutons 
BQuit = Button(master, text ="Quitter", command = master.destroy)
BQuit.grid(row = 20, column = 0)
BCalcul = Button(master, text ="Calculer", command = calcul)
BCalcul.grid(row = 20, column = 1)
mainloop()
