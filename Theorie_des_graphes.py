# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 18:27:41 2022
ISIMA: théorie des graphes: Dijkstra
@author: besqu
"""

class Graph():
    
    def __init__(self, liaisons_villes, idc_villes):
        self.list=liaisons_villes
        self.idc=idc_villes
        
        #exportation des données du graphe
        fichier=open("idc_villes.txt", "w")
        fichier.write(str(idc_villes))
        fichier.close
        fichier=open("listeadj.txt", "w")
        fichier.write(str(liaisons_villes))
        fichier.close
        
        self.mat=Graph.create_mat_adj(self)
        
        
    def create_mat_adj(self):
        """
        Description
        -------
        Crée une matrice d'adjacence à partir d'une liste d'adjacence'
        
        Returns
        -------
        mat : list
            matrice d'adjacence issue de la liste d'adjacence du graphe fournie.

        """
        
        #on crée une matrice vide de la taille de notre liste d'adjacence (nbr de sommet)
        mat = [[ '' for j in range(len(self.list))] for i in range(len(self.list))]
        # on remplit notre matrice avec nos données (liaisons et tps de parcours)
        for k in self.list:
            for n in self.list[k]:
                mat[k][n]=self.list[k][n]
            
        return mat


    def print_matrice(self):
        """
        Description
        -------
        affiche la matrice d'adjacence du graphe
        """          
        return self.mat
    
    def matrice_txt(self):
        """
        Description
        Crée un fichier .txt avec la matrice d'adjacence en contenu
        """
        fichier=open("matrice.txt", "w")
        fichier.write(str(Graph.print_matrice(self)))
        fichier.close
        
    
    def get_code_ville(self, ville):
        """
        Description
        -------
        Renvoie le code d'une ville à l'aide de la liste des indices
        
        Parameters
        ----------
        ville : str
            ville dont on veut savoir le code.

        Raises
        ------
        ValueError
            si la ville n'existe pas dans les données.

        Returns
        -------
        x:
            code de la ville
        -1:
            si la ville n'existe pas
        """
        #on parcours notre liste d'indices

        for x in self.idc:
            if self.idc[x]==ville:
                return x

        raise ValueError ('La ville n\'existe pas ou est mal orthographiée')        
        return -1
    
    def get_ville(self, code):
        """
        Description
        -------
        Renvoie la ville correspondante à un code
        
        Parameters
        ----------
        code : int
            ville codée

        Raises
        ------
        ValueError
            si le code ne correspond à aucune ville

        Returns
        -------
        str
            ville correspondant a l'indice fourni.

        """

        if code in self.idc:
            return self.idc[code]
        else:
            raise ValueError ('La ville n\'existe pas')
    
    def get_tps_parcours(self, ville1, ville2):
        """
        Description
        -------
        Renvoie le temps de trajet entre deux sommets du graphe (villes)
        
        Parameters
        ----------
        ville1 : int ou str
            ville de départ
        ville2 : int ou str
            ville d'arrivée

        Raises
        ------
        ValueError
            si la ville n'est pas présente dans la liste ou si le trajet n'existe pas

        Returns
        -------
        int
            temps de parcours entre les deux villes.

        """
        #on transforme les villes en code si entrée str
        
        if type(ville1)==str:
            tmp1=self.get_code_ville(ville1)
        else:
            tmp1=ville1
        
        
        if type(ville2)==str:
            tmp2=self.get_code_ville(ville2)
        else:
            tmp2=ville2
            
        if tmp1!=-1 and tmp2!=-1 and tmp1<=len(self.list) and tmp2<=(len(self.list)):
            if self.mat[tmp1][tmp2]!='':
                temp="Le temps de trajet est de " + str(self.mat[tmp1][tmp2]//60) + " h " + str(self.mat[tmp1][tmp2]%60) + " min"
                return temp
            else:
                raise ValueError("Le trajet entre les deux villes n'existe pas")
        else:
            raise ValueError("Une des villes n'est pas présente dans la base de données")
        
            
    def set_tps_parcours (self, ville1, ville2, temps, reverse=True):
        """
        Description
        -------
        Met à jour un temps de parcours entre deux villes
        
        Parameters
        ----------
        ville1 : int ou str
            ville de départ
        ville2 : int ou str
            ville d'arrivée'
        temps : int ou '' si on supprime le trajet
            nouveau temps
        reverse : bool
            si on applique le changement aux ''deux sens'' de l'arête

        Raises
        ------
        ValueError
            si la ville de départ ou celle d'arrivée n'est pas existante
        """
        
        #on récupère les codes numériques des villes si entrée str
        if type(ville1)==str:
            tmp1=self.get_code_ville(ville1)
        else:
            tmp1=ville1
        
        if type(ville2)==str:
            tmp2=self.get_code_ville(ville2)
        else:
            tmp2=ville2
                    
        #si les villes existent dans le graphe, on maj le temps de parcours
        if tmp1!=-1 and tmp2!=-1:
            self.mat[tmp1][tmp2]=temps
            self.list[tmp1][tmp2]=temps
            if reverse==True:
                self.mat[tmp2][tmp1]=temps
                self.list[tmp2][tmp1]=temps
            if temps=='':
                del self.list[tmp1][tmp2]
        else:
            raise ValueError("Une des villes n'est pas présente dans la base de données")
        return 'Done'    


    def dijkstra (self, villedepart):
        """
        Description
        -------
        Cherche le plus court trajet entre deux sommets d'un graphe

        Parameters
        ----------
        villedepart : int ou str
            sommet d'origine du départ de notre parcours

        Asserts
        ----------
        on vérifie si il n'y a aucun temps négatif auquel cas Dijkstra ne fonctionne pas

        Returns
        -------
        temps, precedent

        temps: temps parcours minimum entre ville départ et celle d'arrivée
        chemin: sommets parcourus pour le trajet le plus court

        """
        if type(villedepart)==str:
            villedepart=self.get_code_ville(villedepart)
            
        #Initialisation
        assert all(self.list[u][v] >=0 for u in self.list.keys() for v in self.list[u].keys())

        parcours= {x:None for x in self.list.keys()} #aucun chemin est établi
        dejaTraite= {x:False for x in self.list.keys()} #tous les sommets sont init à False car pas visités
        temps= {x:float('inf') for x in self.list.keys()} #temps à infini pr montrer que l'on a pas traité l'arête
        temps[villedepart]=0
        todo=[(0, villedepart)] #on init le premier trajet autour de la ville de départ
        
        #parcours
        while todo:
            temps_nd, nd = todo.pop()
            if not dejaTraite[nd]:  #on vérifie si le trajet a déjà été traité
                dejaTraite[nd]=True
                
            for voisin in self.list[nd].keys():
                nv_parcours=temps_nd + self.list[nd][voisin] #on additionne les temps de parcours
                if nv_parcours < temps[voisin]:  #on compare si inférieur au temps minimal
                    temps[voisin]=nv_parcours
                    parcours[voisin]=nd
                    todo.append((nv_parcours, voisin))
            todo.sort(reverse=True) #on trie les trajets par ordre du plus long au plus court
        return temps, parcours
    
    def trajet_rapide(self, chemin, affichage=True):
        """
        Description
        -------
        Renvoie le trajet le plus court entre deux sommets à l'utilisateur

        Parameters
        ----------
        chemin: list
            liste des villes par lequel on doit passer
        affichage : bool
            On choisis ou non d'afficher le texte de conclusion. Vrai par défaut.

        Raises
        ------
        ValueError
            Si une des villes est mal renseignée par utilisateur

        Returns
        -------
        temps[villearr]: int
            retourne le temps de parcours minimum.
        trajet : list
            retourne un tableau des sommets (villes) à parcourir.
        """
        
        #on transforme les villes en code décimal si entrée en str
        for k in range(len(chemin)):
            if type(chemin[k])==str:
                chemin[k]=self.get_code_ville(chemin[k])
            else:
                if not chemin[k] in self.idc:
                    raise ValueError ("La ville" ,k, " n'existe pas")
                    
        #on initialise nos variables
        trajet=[]
        temps=[]
        dk_chemin=[]
        temps_parcours=0
        # on appelle la méthode dijkstra entre chaque villes rentrées
        for n in range (len(chemin)-1):
        
            x,y= self.dijkstra(chemin[n])
            temps.append(x)
            dk_chemin.append(y)
            
        #on parcours la liste des sommets parcourus pour sortir le trajet minimum
        #de la forme: {0: 2, 1: 2, 2: 13, 3: 13, 4: 12, 5: 12, 6: 14, 7: 14, 8: 14}
        
        for m in range (1,len(chemin)):
        
            trajet_tmp=[]
            tmp=chemin[m]
            while dk_chemin[m-1][tmp]!=None:
                tmp=dk_chemin[m-1][tmp]
                trajet_tmp.append(self.get_ville(tmp))
            trajet_tmp.reverse()
            for k in trajet_tmp:
                trajet.append(k)
                    
            temps_parcours+=temps[m-1][chemin[m]]
            
            #on ajoute la ville d'arrivée à notre trajet
        trajet.append(self.get_ville(chemin[len(chemin)-1])) 
        
        if affichage==True:
            ch_trajet=''
            temps_parcours="Le temps de trajet est de " + str(temps_parcours//60) + " h " + str(temps_parcours%60) + " min"
            for k in trajet:
                ch_trajet+=str(k)+', '
            trajet='Le trajet à suivre est '+ch_trajet[:-2]
          
        return temps_parcours, trajet
    
    def matrice_complete(self):
            
        """
        Description
        -------
        remplit toute la matrice d'adjacence avec les trajets les plus courts'
        """
        
        #on appelle la fonction dijkstra pour tous les trajets entre tous les sommets du graphe
        for u in range(len(self.list)):
            for v in range(len(self.list)):
                temps, _=self.trajet_rapide([u, v], False)
                self.mat[u][v]=temps
                self.list[u][v]=temps
        return 'Done'
                
    def matrice_excel(self, nom_fichier,separateur=';'):
        """
        Parameters
        ----------
        nom_fichier : str
            nom du fichier à créer
        separateur : str, optional
            The default is ';'.

        Returns
        -------
        'Done'
        
        DESCRIPTION.
        Crée un fichier csv qui peut s'ouvrir dans excel de la matrice complete

        """
        fichier=open(nom_fichier+'.csv','w')      
        mat=[["","Sainte-Florine","Brioude","Mazeyrat-d'Allier","Langeac","Cussac-sur-Loire","Le Chambon sur Lignon","Tence","Sainte-Sigolène","Bas-en-Basset","Saint-Julien-Chapteuil","Monistrol-sur-Loire","Craponne-sur-Arzon","Le Puy-en-Velay","Saint-Paulien","Yssingeaux","Aurec-sur-Loire"]]
        ligne=0
        for k in self.mat:
            mat.append(k)
        for x in mat:
            o=1
            if ligne<=16:
                fichier.write(mat[0][ligne]+separateur)
            for n in x:
                n=str(n)
                if o<len(x) and n!="":
                    fichier.write(n+separateur)
                else:
                    fichier.write(n)
                o+=1
            ligne+=1
            fichier.write('\n') #fin de ligne après chaque liste
        fichier.close()
        return 'Done'

""""""""""""""""""""""""

idc_villes={0:"Sainte-Florine",1:"Brioude",2:"Mazeyrat-d'Allier",
            3:"Langeac",4:"Cussac-sur-Loire",5:"Le Chambon sur Lignon",
            6:"Tence",7:"Sainte-Sigolène",8:"Bas-en-Basset",9:"Saint-Julien-Chapteuil",
            10:"Monistrol-sur-Loire",11:"Craponne-sur-Arzon",12:"Le Puy-en-Velay",
            13:"Saint-Paulien",14:"Yssingeaux",15:"Aurec-sur-Loire"}

hloire={
        0: {1:17, 11:64},
        1: {0:17, 2:23, 11:51},
        2: {1:23, 3:8, 11:42, 13:26},
        3: {2:8, 4:46, 13:30},
        4: {3:46, 5:47, 12:15 ,13:30},
        5: {4:47, 6:11, 9:25, 12:42, 14:26},
        6: {5:11, 7:26, 14:23},
        7: {6:26, 10:11, 14:24, 15:24},
        8: {9:32, 10:9, 11:32, 14:21, 15:13},
        9: {5:25, 8:32, 11:47, 12:19, 13:27, 14:16},
        10: {7:11, 8:9, 14:17, 15:14},
        11: {0:64, 1:51, 2:42, 8:32, 9:47, 13:20},
        12: {4:15, 5:42, 9:19, 13:17, 14:29},
        13: {2:26, 3:30, 4:30, 9:27, 11:20, 12:17},
        14: {5:26, 6:23, 7:24, 8:21, 9:16, 10:17, 12:29},
        15: {7:24, 8:13, 10:14}
        }


""""""""""""""""""""""""
"""hlo.trajet_rapide([0,1,2,3,4,5,6,7,10,15,8,9,14,12,13,11,0])  
 'Le temps de trajet est de 6 h 34 min',
 "Le trajet à suivre est Sainte-Florine, Brioude, Mazeyrat-d'Allier, Langeac, Cussac-sur-Loire, Le Chambon sur Lignon, Tence, Sainte-Sigolène, Monistrol-sur-Loire, Aurec-sur-Loire, Bas-en-Basset, Saint-Julien-Chapteuil, Yssingeaux, Le Puy-en-Velay, Saint-Paulien, Craponne-sur-Arzon, Sainte-Florine")       
"""
graphe=Graph(hloire, idc_villes)
print(graphe.trajet_rapide(["Langeac", "Aurec-sur-Loire"]))