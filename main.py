import sqlite3
from math import sqrt
import random
from tkinter import *
from PIL import Image, ImageTk

# Connection à la base de données :
bdd = sqlite3.connect("database/animalcrossing.db")
curseur = bdd.cursor()

class Perso():
    def __init__(self, id):
        requete = """SELECT perso_name FROM perso WHERE perso_id = ?;"""
        curseur.execute(requete, [id])
        self.name = curseur.fetchall()[0][0]

        self.address = 'personnages/' + self.name + '.png'

        requete = """ SELECT gender_name FROM perso
        Join gender ON perso.gender_id=gender.gender_id
        WHERE perso_name =?;"""
        curseur.execute(requete,[self.name])
        sex = curseur.fetchall()[0][0]

        #On admet que le sexe de base est femelle
        self.female = True
        if sex == "male" :
            self.female = False

        requete =""" SELECT species_name FROM species
        Join perso ON perso.species_id=species.species_id
        Where perso_name = ?;"""
        curseur.execute(requete,[self.name])
        self.race = curseur.fetchall()[0][0]

        requete =""" SELECT hobby_name FROM hobby
        Join perso ON perso.hobby_id=hobby.hobby_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.hobby = curseur.fetchall()[0][0]

        requete= """ SELECT color_name FROM colors
        Join rel_perso_color ON rel_perso_color.color_id=colors.color_id
        Join perso ON rel_perso_color.perso_id=perso.perso_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.color = curseur.fetchall()[0][0]

        requete= """ SELECT style_name FROM styles
        Join rel_perso_style ON rel_perso_style.style_id=styles.style_id
        Join perso ON rel_perso_style.perso_id=perso.perso_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.style = curseur.fetchall()[0][0]

        requete= """ SELECT fear_name FROM fear
        Join perso ON perso.fear_id=fear.fear_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.fear = curseur.fetchall()[0][0]

        requete= """ SELECT coffee_sugar_name FROM coffee_sugar
        Join perso ON perso.coffee_sugar_id=coffee_sugar.coffee_sugar_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.coffeeSugar = curseur.fetchall()[0][0]

        # On utiliseras ? 
        requete= """ SELECT coffee_beans_name FROM coffee_beans
        Join perso ON perso.coffee_beans_id=coffee_beans.coffee_beans_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.coffeeBeans = curseur.fetchall()[0][0]

        # On utiliseras ? 
        requete= """ Select skill_name FROM skill
        Join perso ON perso.skill_id=skill.skill_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.skill = curseur.fetchall()[0][0]

        requete= """ Select personality_name FROM personality
        Join perso ON perso.personality_id=personality.personality_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.personality = curseur.fetchall()[0][0]

        requete= """ SELECT cloth_name FROM clothes
        Join perso ON perso.cloth_id=clothes.cloth_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.cloth = curseur.fetchall()[0][0]

        # On utiliseras ? 
        requete= """ SELECT goal_name FROM goal
        Join perso ON perso.goal_id=goal.goal_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.goal = curseur.fetchall()[0][0]

        requete= """SELECT siblings_name FROM siblings
        Join perso ON perso.siblings_id=siblings.siblings_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.situation = curseur.fetchall()[0][0]

        requete= """SELECT coffee_milk_name FROM coffee_milk
        Join perso ON perso.coffee_milk_id=coffee_milk.coffee_milk_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.coffeeMilk = curseur.fetchall()[0][0]

        # On utiliseras ? 
        requete= """SELECT song_name FROM song
        Join perso ON perso.song_id=song.song_id
        Where perso_name=?;"""
        curseur.execute(requete,[self.name])
        self.song = curseur.fetchall()[0][0]

def choixDesPersonnages(n):
    dicPersos = {}
    lstNum = []
    num = random.randint(1,381)
    for i in range(n):
        while num in lstNum:   # on ne pourras pas retirer le même numéros
            num = random.randint(1,381)
        lstNum.append(num)
        character = Perso(num)
        dicPersos[character.name] = character   #On ajoute le nom du personnage en clé puis son instance en valeur
    return dicPersos

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        #initialisation des paramètres de la fenêtre
        self.title("Whoz that ?")
        self.state('zoomed') #plein écran de la fenetre
        self.iconbitmap("images/Ico_Whoz_that.ico")
        self.configure(bg='pink')

        # définition des futures fenetres
        self.home = Frame(self, background='pink')
        self.option = Frame(self, background ='pink')
        self.information= Frame(self, background='pink')
        self.game = Frame(self, background='pink')
        self.endScreen= Frame(self, background= 'pink')

        # difficulté choisis de base
        self.difficulty = 36
        self.nbQuestions = 0
        self.nbLifes = 3

        self.rulesActivated = False
        self.parametreActivated = False
        self.win = False

        # Initialisation du tchat
        self.q1 = ""
        self.r1 = ""
        self.q2 = ""
        self.r2 = ""
        self.q3 = ""
        self.r3 = ""
        self.dialogue = StringVar()

        #Initialisation des personnages dela grille
        self.dicCharacter = choixDesPersonnages(self.difficulty)
        #Le PC choisis son personnage parmis ceux affichés
        self.characPC = random.choice(list(self.dicCharacter.values()))

        self.main()

    def updateTchat(self, question, response):
        # On fait remonter d'un cran chaque question et réponse
        self.q1 = self.q2
        self.r1 = self.r2
        self.q2 = self.q3
        self.r2 = self.r3
        self.q3 = question 
        self.r3 = response

        qAndR = self.q1 + '\n' + self.r1 + '\n' + self.q2 + '\n' + self.r2 + '\n' + self.q3 + '\n' + self.r3

        self.dialogue.set(qAndR)

    def supprimerSex(self):
        question = "Is it a girl ?"
        #On incrémente le nombre de question
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0
        if self.characPC.female : #Si le personnage de l'IA est une femelle
            for persos in list(self.dicCharacter.values()):
                if not persos.female : #n supprime tous les males
                    self.buttons[counter].destroy()
                counter += 1
            response = "Yes, it's a girl !"
        
        else : #Si le personnage de l'IA est un male
            for persos in list(self.dicCharacter.values()):
                if persos.female : #On supprime les femelles
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, it's a boy. "
        self.updateTchat(question, response) #On mets à jour le tchat 

    def supprimerRace(self, race):
        question = "Is it a " + race + ' ?'
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}" #On met à jour le nombre de questions posées
        counter = 0
        if race == self.characPC.race : #si on choisit la bonne race
            for perso in list(self.dicCharacter.values()):
                if perso.race != self.characPC.race : #on supprime les persos avec une race différente
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, it's a " + race + " !"
        
        else :   #si la race n'est pas la bonne 
            for perso in list(self.dicCharacter.values()):
                if perso.race == race :      #on supprime les persos de la race choisie
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, it is not a " + race 
        self.updateTchat(question, response)

    def supprimerHobbies(self, hobby):
        question = 'Does he like to ' + hobby + ' ?'
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if hobby == self.characPC.hobby : #si on choisit le bon hobby
            for perso in list(self.dicCharacter.values()):
                if perso.hobby != self.characPC.hobby : #on supprime les persos avec un hobby différent
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he likes to " + hobby + " !"
        
        else :   #si ce n'est pas le bon hobby 
            for perso in list(self.dicCharacter.values()):
                if perso.hobby == hobby :      #on supprime les persos du hobby choisi
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he doesn't like to " + hobby
        self.updateTchat(question, response)


    def supprimerSucre(self, sugar):
        question = "Does he put " + sugar + " in his coffee ? "
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if sugar == self.characPC.coffeeSugar : 
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeSugar != self.characPC.coffeeSugar : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he puts " + sugar + " in his coffee !"
        
        else :  
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeSugar == sugar :
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he does not put " + sugar + " in his coffee"
        self.updateTchat(question, response)

    def supprimerCouleur(self, color):
        question = 'Is ' + color + ' his favorite color ?'
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if color == self.characPC.color : 
            for perso in list(self.dicCharacter.values()):
                if perso.color != self.characPC.color : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, " + color + " is his favorite color !"
        
        else :   
            for perso in list(self.dicCharacter.values()):
                if perso.color == color :      
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, " + color + " isn't his favorite color"
        self.updateTchat(question, response)

    def supprimerStyle(self, style):
        question = "Is it " + style + " ?"
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if style == self.characPC.style :
            for perso in list(self.dicCharacter.values()):
                if perso.style != self.characPC.style :
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he is " + style + ' !'
        
        else :
            for perso in list(self.dicCharacter.values()):
                if perso.style == style :
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he is not " + style
        self.updateTchat(question, response)

    def supprimerPeur(self, fear):
        question = "Is he afraid of " + fear + " ?"
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if fear == self.characPC.fear :
            for perso in list(self.dicCharacter.values()):
                if perso.fear != self.characPC.fear : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he is afraid of " + fear + " !"
        
        else :
            for perso in list(self.dicCharacter.values()):
                if perso.fear == fear :
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he isn't afraid of " + fear
        self.updateTchat(question, response)

    def supprimerBoisson(self, drink):
        question = "Did he drink " + drink + " ?"
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if drink == self.characPC.coffeeBeans :
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeBeans != self.characPC.coffeeBeans : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he drinks " + drink + " !"
        
        else :
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeBeans == drink :
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he doesn't drink " + drink
        self.updateTchat(question, response)

    def supprimerPersonnalite(self, personality):
        question = "Is he " + personality + " ?"
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if personality == self.characPC.personality :
            for perso in list(self.dicCharacter.values()):
                if perso.personality != self.characPC.personality : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he is " + personality + " !"
        
        else :  
            for perso in list(self.dicCharacter.values()):
                if perso.personality == personality :   
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he isn't " + personality
        self.updateTchat(question, response)

    def supprimerVetement(self, cloth):
        question = "Is he wearing " + cloth + " ?"
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if cloth == self.characPC.cloth : 
            for perso in list(self.dicCharacter.values()):
                if perso.cloth != self.characPC.cloth : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he wears " + cloth + " !"
        
        else :
            for perso in list(self.dicCharacter.values()):
                if perso.cloth == cloth :
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he doesn't wear " + cloth
        self.updateTchat(question, response)

    def supprimerSituation(self, situation):
        question = 'Is he ' + situation + ' ?'
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if situation == self.characPC.situation :
            for perso in list(self.dicCharacter.values()):
                if perso.situation != self.characPC.situation :
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he is " + situation + " !"
        
        else :   #si la race n'est pas la bonne 
            for perso in list(self.dicCharacter.values()):
                if perso.situation == situation :      #on supprime les persos de la race choisie 
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he isn't " + situation
        self.updateTchat(question, response)

    def supprimerLait(self, milk ):
        question = 'Does he put ' + milk + ' in his coffee ?'
        self.nbQuestions += 1
        self.textQ['text'] = f"Number of questions asked : {self.nbQuestions}"
        counter = 0   
        if milk == self.characPC.coffeeMilk :
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeMilk != self.characPC.coffeeMilk : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "Yes, he puts " + milk + "in his coffee !"
        
        else : 
            for perso in list(self.dicCharacter.values()):
                if perso.coffeeMilk == milk : 
                    self.buttons[counter].destroy()
                counter +=1
            response = "No, he doesn't put " + milk + "in his coffee"
        self.updateTchat(question, response)

    def jouer(self, difficulty):
        self.configure(bg='pink')

        self.difficulty = difficulty

        #Initialisation des personnages dela grille
        self.dicCharacter = choixDesPersonnages(difficulty)
        #Le PC choisis son personnage parmis ceux affichés
        self.characPC = random.choice(list(self.dicCharacter.values()))

        #On retire les widgets de la page d'accueil
        self.home.pack_forget()
        self.option.pack_forget()
        #On place les compteurs de vies et de questions
        self.textQ = Label(self, text=f"Number of questions asked : {self.nbQuestions}", bg='pink')
        self.textQ.place(x=0, y=0)
        
        self.textL = Label(self, text=f"Number of lifes : {self.nbLifes}", bg='pink')
        self.textL.place(x=0, y=15)

        self.game.pack(expand = YES)
        self.menuBar = Menu(self)

        self.tchat = Label(self.game, textvariable=self.dialogue, background='pink')

        # differentes questions
        sex = Menu(self.menuBar, tearoff=0)
        sex.add_command(label="Is it a girl ?", command=self.supprimerSex)

        animalRace = Menu(self. menuBar, tearoff=0) #sujet de la question
        requete = """SELECT species_name FROM species"""
        curseur.execute(requete)
        lstRaces = curseur.fetchall()    #liste de toutes les races possibles
        for race in lstRaces : #On ajoute toutes les races sous forme de questions 
            animalRace.add_command(label=f'Is it a {race[0]} ?' , command=lambda race = race[0] : self.supprimerRace(race)) #lambda est une 'minifonction'
           
        hobbies = Menu(self.menuBar, tearoff= 0)   #sujet de la question
        requete = """SELECT hobby_name FROM hobby"""
        curseur.execute(requete)
        lstHobbies = curseur.fetchall() #liste de tout les hobbies
        for hobby in lstHobbies :  #On ajoute tous les hobbies sous forme de question
            hobbies.add_command(label=f'Does he likes to {hobby[0]} ?' , command=lambda hobby = hobby[0] : self.supprimerHobbies(hobby))
        
        sucre = Menu(self.menuBar, tearoff= 0) #sujet de la question
        lstCoffeeSugar = []
        for perso in list(self.dicCharacter.values()):
            while perso.coffeeSugar not in lstCoffeeSugar : #On ajoute les différents attributs des personnages présents sur la grille
                lstCoffeeSugar.append(perso.coffeeSugar)
        for cuillere in lstCoffeeSugar :  #Puis on les ajoute sous forme de questions
            sucre.add_command(label=f'Does he put {cuillere} in his coffee?' , command=lambda sugar = cuillere : self.supprimerSucre(sugar))
        
        colors = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT color_name FROM colors"""
        curseur.execute(requete)
        lstColor = curseur.fetchall()
        for couleur in lstColor :
            colors.add_command(label=f'Is {couleur[0]} his favorite color ?' , command=lambda couleur = couleur[0] : self.supprimerCouleur(couleur))
        
        styles = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT style_name FROM styles"""
        curseur.execute(requete)
        lstStyle = curseur.fetchall()
        for style in lstStyle :
            styles.add_command(label=f'Is it {style[0]} ?' , command=lambda styles = style[0] : self.supprimerStyle(styles))
        
        fear = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT fear_name FROM fear"""
        curseur.execute(requete)
        lstFear = curseur.fetchall()
        for peur in lstFear :
            fear.add_command(label=f'Is he afraid of {peur[0]} ?' , command=lambda peur = peur[0] : self.supprimerPeur(peur))

        drink = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT coffee_beans_name FROM coffee_beans"""
        curseur.execute(requete)
        lstDrink = curseur.fetchall()
        for boissons in lstDrink :
            drink.add_command(label=f'Did he drinks {str(boissons[0])} ?' , command=lambda Boisson = boissons[0] : self.supprimerBoisson(Boisson))
        
        personnality = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT personality_name FROM personality"""
        curseur.execute(requete)
        lstPersonality = curseur.fetchall()
        for personalite in lstPersonality :
            personnality.add_command(label=f'Is he {personalite[0]} ?' , command=lambda personnalites = personalite[0] : self.supprimerPersonnalite(personnalites))
        
        clothes = Menu(self.menuBar, tearoff= 0)
        lstClothes = []
        for perso in list(self.dicCharacter.values()) :
            while perso.cloth not in lstClothes :
                lstClothes.append(perso.cloth)
        for vetement in lstClothes :
            clothes.add_command(label=f'Is he wearing {vetement} ?' , command=lambda vetement = vetement : self.supprimerVetement(vetement))

        situations = Menu(self.menuBar, tearoff= 0)   
        lstSituation = []
        for perso in list(self.dicCharacter.values()) :
            while perso.situation not in lstSituation :
                lstSituation.append(perso.situation)
        for situation in lstSituation :
            situations.add_command(label=f'Is he {situation} ?' , command=lambda sibling = situation : self.supprimerSituation(sibling))
        
        milk = Menu(self.menuBar, tearoff= 0)
        requete = """SELECT coffee_milk_name FROM coffee_milk"""
        curseur.execute(requete)
        lstMilk = curseur.fetchall()
        for lait in lstMilk :
            milk.add_command(label=f'Does he put {lait[0]} in his coffee ?' , command=lambda milk = lait[0] : self.supprimerLait(milk))

        # differents sujets de question
        self.menuBar.add_cascade(label="Gender", menu=sex)
        self.menuBar.add_cascade(label="Race", menu=animalRace)
        self.menuBar.add_cascade(label="Hobbies", menu=hobbies)
        self.menuBar.add_cascade(label="Sugar", menu=sucre)
        self.menuBar.add_cascade(label="Color", menu=colors)
        self.menuBar.add_cascade(label="Style", menu=styles)
        self.menuBar.add_cascade(label="Fear", menu=fear)
        self.menuBar.add_cascade(label="Drink", menu=drink)
        self.menuBar.add_cascade(label="Personality", menu=personnality)
        self.menuBar.add_cascade(label="Clothes", menu=clothes)
        self.menuBar.add_cascade(label="Situation", menu=situations)
        self.menuBar.add_cascade(label="Milk in coffee ", menu=milk)

        self.config(menu=self.menuBar)

        #Préparation de l'affichage des personnages
        colonne = 0
        ligne = 0
        fact = 0.45 #facteur de grossissment de l'image
        images=[Image.open(self.dicCharacter[keys].address) for keys in self.dicCharacter] #Ouverture des images avec PIL

        self.grille = Label(self.game)

        #récupération de leurs taille initiale multiplié par le facteur de croissance
        self.w=[int(image.size[0]*fact) for image in images]
        self.h=[int(image.size[1]*fact) for image in images]

        # On met les images redimensionnées dans une liste
        for i in range(self.difficulty):
            self.imageResizes=[image.resize((self.w[i],self.h[i])) for image in images]
        self.img = [ImageTk.PhotoImage(img) for img in self.imageResizes]

        # création des boutons
        self.buttons=[Button(self.grille, image=image, relief='flat', command = lambda idx=self.img.index(image): self.trouve(idx)) for image in self.img]

        # Affichage sous forme de tableau en fonction de la difficulté choisie
        for i in range(self.difficulty):
            colonne +=1
            if colonne == sqrt(self.difficulty)+1:  #Lorsque l'on remplie un côté du carré
                colonne = 1
                ligne += 1
            self.buttons[i].grid(column=colonne, row = ligne)
        self.grille.pack(side=LEFT, padx=150)
        self.tchat.pack(side=RIGHT)

    def endGame(self):
        #On supprime les différents widgets qui sont générés par le jeu
        self.game.pack_forget()
        self.menuBar.destroy()
        self.label.pack_forget()
        self.button.pack_forget()
        self.buttonRouage.pack_forget()
        self.buttonInfo.pack_forget()
        self.information.pack_forget()
        self.textQ.destroy()
        self.textL.destroy()
        self.tchat.destroy()
        self.grille.destroy()

        self.game.pack_forget()
        self.endScreen.pack(expand=YES)

        self.screenWin = Label(self.endScreen, text= "Vous avez perdu !", background='pink')

        if self.win:
            self.screenWin = Label(self.endScreen, text = "Vous avez gagné! \n Il vous restait : " + str(self.nbLifes) + 'vie(s)', background='pink')

        self.screenWin.pack()

        #On réinitialise les différentes varaibles utiles pour jouer
        self.nbQuestions = 0
        self.nbLifes = 7

        self.game.pack_forget()
        self.endScreen.pack(expand=YES)

        self.retourMenu = PhotoImage(file='images/MAISON (2).png')
        self.menu = Button(self.endScreen, image=self.retourMenu, relief= 'flat', command= self.main, bg='pink') 
        self.menu.pack()

    def trouve(self, idx):
        name = list(self.dicCharacter.keys())[idx]
        #On vérifie que le nom du personnage sur lequel on a cliqué correspond à celui choisit par l'IA
        if self.characPC.name == name : 
            self.win = True
            self.endGame()
             
        else :
            self.nbLifes -= 1
            self.textL['text'] = f"Number of lifes : {self.nbLifes}"
            if self.nbLifes == 0:  #Si le joueur n'as plus de vies la partie est perdu
                self.endGame()
            self.buttons[idx].destroy()  #On supprime le personnages sur lequel on a cliqué pour ne pas le choisir à nouveau

    def main(self):
        #On supprime tout ce qui pourrait se réafficher
        self.endScreen.pack_forget()
        if self.rulesActivated :
            self.label.pack_forget()
            self.button.pack_forget()
            self.buttonRouage.pack_forget()
            self.buttonInfo.pack_forget()
            self.information.pack_forget()
            self.regleDeJeu.pack_forget()
            self.regleQuestions.pack_forget()
            self.regleVie.pack_forget()
            self.regleVictoire.pack_forget()
            self.buttonRetour.pack_forget()
    
            
        if self.parametreActivated :
            self.buttonEasy.destroy()
            self.buttonMedium.destroy()
            self.buttonHard.destroy()

        # boite accueil
        self.information.pack_forget()
        self.option.pack_forget()
        self.home.pack(fill = BOTH)
        
        # logo du jeu
        self.logo = PhotoImage(file='images/Logo_Whoz_that.png')
        self.label = Label(self.home, image=self.logo, bg='pink') 
        self.label.pack()

        # bouton pour lancer le jeu
        self.boutonPlay = PhotoImage(file='images/Play_Button.png')
        self.button = Button(self.home, image=self.boutonPlay, relief="flat", command= lambda difficulty = 36 : self.jouer(difficulty), bg='pink')
        self.button.pack()

        # parametre
        self.rouageClick= PhotoImage(file='images/rouage-1.png')
        self.buttonRouage = Button(self.home, image=self.rouageClick, relief="flat", command=self.parametre,bg='pink')
        self.buttonRouage.place(x=self.winfo_screenheight()+537 , y= 0)

        #information sur le jeu
        self.infoClick= PhotoImage(file='images/Informations-1 (1).png')
        self.buttonInfo = Button(self.home, image=self.infoClick, relief="flat", command=self.regles,bg='pink')
        self.buttonInfo.place(x=self.winfo_screenheight()- 765 , y= 0)
        
    def parametre(self):
        #page des paramètres
        self.parametreActivated = True
        self.option.pack(expand=YES)
        self.home.pack_forget()

        # Bouton de difficulté facile
        self.buttonEasy = Button(self.option, text= "EASY", relief="flat", command= lambda difficulty = 16 : self.jouer(difficulty),bg='pink')
        self.buttonEasy.pack()

        # Bouton de difficulté médium
        self.buttonMedium = Button(self.option, text= "MEDIUM", relief="flat", command= lambda difficulty = 25 : self.jouer(difficulty),bg='pink')
        self.buttonMedium.pack()

        # Bouton de difficulté difficile
        self.buttonHard = Button(self.option,text= "HARD", relief="flat", command= lambda difficulty = 36 : self.jouer(difficulty),bg='pink')
        self.buttonHard.pack()

    def regles(self):
        self.rulesActivated = True
        self.information.pack(expand= YES)
        self.home.pack_forget()
        

        self.retourClick= PhotoImage(file='images/FLECHE RETOUR-1 (1).png')
        self.buttonRetour = Button(self.information, image=self.retourClick, relief="flat", command=self.main,bg='pink')
        self.buttonRetour.place(x=self.winfo_screenheight()- 765 , y=-0)
          

        #Règles du jeu: Création de bouton avec un texte que l'on désactive pour laisser seulement le texte
        self.regleDeJeu= Label(self.information, text= "Les règles sont simples: ", relief= "flat", bg='pink' )
        self.regleDeJeu.pack()
        
        self.regleQuestions= Label(self.information, text= "- Les Questions: Pour poser des questions il vous suffit d'utiliser la fenetre au dessus du jeu avec les catégories de question, ensuite choisissez votre questions et posez la à l'ordianteur. A chaque questions le compteur de questions augmentera. ", relief= "flat", bg='pink' )
        self.regleQuestions.pack()
        
        self.regleVie= Label(self.information, text= "- Les Vies: Vous avez un certains nombres de vie en fonction de la difficulté du niveau, à chaque mauvais personnage cliqué vous perdrez une vie. Si vous arrivez à 0 vous avez perdu. ", relief= "flat", bg='pink' )
        self.regleVie.pack()
        
        self.regleVictoire= Label(self.information, text= " Comment gagner ? : C'est très simple pour remporter la partie il vous suffit de trouver le personnage choisit par l'ordinateur sans perdre toutes vos vies et avec le moins de questions possibles.  ", relief= "flat", bg='pink' )
        self.regleVictoire.pack()

        self.retourClick= PhotoImage(file='images/FLECHE RETOUR-1 (1).png')
        self.buttonRetour = Button(self.information, image=self.retourClick, relief="flat", command=self.main,bg='pink')
        self.buttonRetour.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()


bdd.close()

