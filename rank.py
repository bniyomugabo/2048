#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from ezTK import *
from random import*
from ezCLI import*


def ranking():
    global end

    
    end = Win(title='historique', bg='#FFF', grow=False)
    
    fr1 = Frame(end, flow="S")
    Label(fr1, text='Classement', width=40, font='Arial 30', border=2, bg="#faf8ef",fg="#776e65")
    
    end.ranks = Frame(end, fold = 2,op=2)
    colors = ("#012424","#0F4747","#115757","#146969","#C2BD3C","#403E04","#666309","#757209","#BAB620","#BAB620")
    
    for i in range(20):
        Label(end.ranks, text='joueur', width=10, font='Arial 20 ',fg ='#EDEDE8', bg= colors,state=i ,border=2)
    fr4 = Frame(end, flow="E")
    end.home = Button(fr4, text='Acceuil', font='Arial 30 bold', fg="#053603", bg=colors,command=end.exit)
    end.follow = Button(fr4, text='continue', font='Arial 30 bold', fg=colors, bg='#00F',command=nextlevel)
    arrangement()
    
    end.loop()
    
def playerRanks(name:str,score:int):  # on met à jour les données (scores et addiction des donnes de nouveau joueur)
    csv = read_csv('ranking.csv')
    names = csv[1]
    scores = csv[2]
    confirm = True
    for player in range(len(names)):
        if names[player] == name:
            confirm = False
            if scores [player] < score :
                scores[player] = score
                
    if confirm:
        names.append(name)
        scores.append(0)
    permit = 'START'
    matrix = [permit,names,scores]
    write_csv('ranking.csv', matrix)


def arrangement():
    csv = read_csv('ranking.csv')
    names = csv[1]
    scores = csv[2]
    winners = []
    n = 0
    while n < 10:
        for i in range(len(scores)):
            if max(scores[1:len(scores)]) == scores[i]:
                winners.append(i)
                scores[i] = 0
                break
        n += 1
        
    csv = read_csv('ranking.csv')
    for i in range(10):
        place = winners [i]
        end.ranks[i][0]['text'] = csv[1][place]
        end.ranks[i][1]['text'] = csv[2][place]


        
    
    
def nextlevel ():
    csv = read_csv('ranking.csv')
    permit = 'NEXT'
    names = csv[1]
    scores = csv[2]
    matrix = [permit, names, scores]
    write_csv('ranking.csv', matrix)
    end.exit()

if __name__ == '__main__':
    ranking()


# In[ ]:




