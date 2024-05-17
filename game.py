#!/usr/bin/env python
# coding: utf-8

# In[2]:


from ezTK import *
from random import *
from rank import*
import random
info = {
    'level': 4,
    'player': 0,
    'mode': 0,
    'right': 0
}


def main(niveau:int,player:str,best:int,start:bool):
    global win, counter, home, end
    
    
    if start :
        home = Win(title=f'Acceuil 2048', op=5, flow='S',
                font='Arial 15 ', bg='#3A6B35', fg='#CBD18F')

        Selection = Frame(home, op=0, grow=False, flow='S')
        mode = ('Eclair', 'Sombre')
        Label(Selection, text='Apparence', font='Arial 20 bold',
            anchor='W', grow=False, width=50)
        home.mode = Spinbox(Selection, values=mode,
                            fg='#E3B448', width=5, wrap=False)

        levels = tuple(f"Niveau  {i} " for i in range(1, 7))
        Label(Selection, text='Niveau', font='Arial 20 bold', anchor='W', grow=False)
        home.level = Spinbox(Selection, values=levels,
                            fg='#E3B448', width=5, wrap=False)

        name = Frame(home, op=0, grow=False)
        Label(name, text='Joueur/    votre nom',
              font='Arial 20 bold', anchor='W', grow=False)
        home.name = Entry(name)

        Start = Frame(home, op=0, grow=False)
        Button(Start, text='GO!', font='Arial 20 bold',
            command=update, grow=False)
        Button(Start, text='Classement', font='Arial 20 bold',
            command=ranking, grow=False)

        home.loop()

    ######################################################################################################

    win = Win(title=f"2048 {info['player']}", key=on_key, border=2, bg='#faf8ef', grow=False)
    n = info['level']
    

    # on va compter des fois que les buttons de direction est utilisé
    counter = {
        'up': 0,
        'down': 0,
        'left': 0,
        'right': 0
    }

    # information sur le jeu
    fr1 = Frame(win, flow="S")
    colorBG = ("#faf8ef", "#000")
    colorFG = ("#776e65", "#FFF")
    
    Label(fr1, text="2048", font='Arial 50 bold', bg=colorBG,state=0, fg=colorFG)
    Label(fr1, text="Enjoy your free time!!\n with 2048 game",
          bg=colorBG,state=0, fg=colorFG, font='Arial 10 bold')
    
    win.info = Frame(win, flow='E')

    win.scores = Frame(win.info, flow='S')
    Label(win.scores, text='score', bg="#bbada0",
          fg="#ede1d2", font='Arial 20 bold')
    win.score = Label(win.scores, text='0', bg="#bbada0",
                      fg="#ede1d2", font='Arial 20')  # les points

    best = Frame(win.info, flow='S')
    Label(best, text='Best', bg="#bbada0", fg="#ede1d2", font='Arial 20 bold')
    win.best = Label(best, text='0', bg="#bbada0", fg="#ede1d2",
                     font='Arial 20')  # le meilleurs point

    Button(win, text="Nouveau Jeu", bg='#8f7a66', fg="#053603",
           font='Arial 20 bold', command=newGame)  # on lance un nouveau jeu

    win.field = Frame(win, bg="#9D9E9E", op=2, fold=n,
                      grow=False)  # espace principale de jeu
    colors = ("#ccc0b3", "#eee4da", "#ede0c8", "#f59563",
              "#f67c5f", "#f65e3b", "#edcf72", "#edcc61", "#b784ab")

    for c in range(n*n):
        Label(win.field, bg=colors, border=1, fg="#053603",
              text=' ', font='Arial 30 bold', width=5, state=0)

    for i in range(2):  # on va choisir deux labele et y place <2 ou 4>
        rw = randrange(n)
        cl = randrange(n)
        vl = random.choice([2, 4])
        win.field[rw][cl]['text'] = vl
    # Button(win, text='Terminer',font = 'Arial 20 bold' , command=endgame, grow=False)
    #backgroundcolors()
    csv = read_csv('ranking.csv')
    if csv[0][0] == 'START':
        win.loop()
        
    ranking()
    
    if csv[0][0] == 'NEXT':
        permit = 'START'
        names = csv[1]
        scores = csv[2]
        matrix = [permit, names, scores]
        write_csv('ranking.csv', matrix)
        info['level'] +=1
        main(1, f"level{info['level']}", 0, False)
        

    


def update():
    levels = tuple(f"Niveau  {i} " for i in range(1, 7))
    for i in range(len(levels)):
        if levels[i] == home.level.state:
            info['level'] = i+4
    info['player'] = home.name.state
    info['mode'] = home.mode.state
    playerRanks(info['player'], 0)
    home.exit()


# In[5]:


def on_key(widget: object, code: str, mod: tuple):
    # print(code)
    moves = ('Up', 'Down', 'Right', 'Left')
    if code not in moves:
        return None
    elif code == 'Up':
        count('up')
        return top()
    elif code == 'Down':
        count('down')
        return down()
    elif code == 'Right':
        count('right')
        return right()
    else:
        count('left')
        return left()


# In[6]:


def colorsAdjust():
    rows, cols = win.field.widgets
    for row in range(rows):
        for col in range(cols):
            if win.field[row][col]['text'] != ' ':
                content = int(win.field[row][col]['text'])
                #print(f"content={content}")
                if content >= 2:
                    win.field[row][col].state = 1
                if content >= 4:
                    win.field[row][col].state = 2
                if content >= 8:
                    win.field[row][col].state = 3
                if content >= 32:
                    win.field[row][col].state = 4
                if content >= 64:
                    win.field[row][col].state = 5
                if content >= 128:
                    win.field[row][col].state = 6
                if content >= 4096:
                    win.field[row][col].state = 7
            else:
                win.field[row][col].state = 0

# In[]
"""def backgroundcolors():
    print(win.widgets)
    for cl in win.widgets:
        print(cl)
        win[cl]['bg'] = "#000"


"""

# In[8]:


def count(direction: str):
    moves = ('up', 'down', 'right', 'left')
    for i in moves:
        if direction == i:
            counter[i] = counter[i] + 1
        else:
            counter[i] = 0


# In[9]:


def newTwo():
    rows, cols = win.field.widgets
    emptyspace = 0
    k = ()
    for row in range(rows):
        for col in range(cols):
            if win.field[row][col]['text'] == ' ':
                k += ((row, col),)
                emptyspace += 1
    #print(emptyspace)
    if emptyspace > 1:
        index = randrange(emptyspace)
        row, col = k[index]
        #print(f"cord {k[index]}")
        win.field[row][col]['text'] = 2
    elif emptyspace == 1:
        row, col = k[0]
        win.field[row][col]['text'] = 2
        del win[3]


# In[10]:


def right():
    #print('right')
    rows, cols = win.field.widgets
    label = win.field
    before = int(win.score['text'])
    for row in range(rows):
        for col in range(cols-1):
            if label[row][col+1]['text'] == ' ':
                label[row][col + 1]['text'] = label[row][col]['text']
                label[row][col]['text'] = ' '
                for cl in range(col, 0, -1):
                    label[row][cl]['text'] = label[row][cl - 1]['text']
                    label[row][cl - 1]['text'] = ' '

            else:
                if label[row][col]['text'] != ' ':
                    first = int(label[row][col]['text'])
                    second = int(label[row][col + 1]['text'])
                    if first == second:
                        label[row][col + 1]['text'] = f"{2 * first}"
                        label[row][col]['text'] = ' '
                        for cl in range(col, 0, -1):
                            label[row][cl]['text'] = label[row][cl - 1]['text']
                            label[row][cl - 1]['text'] = ' '

                        win.score['text'] = int(
                            win.score['text']) + (2 * first)

    after = int(win.score['text'])  # verifier l'augmentation des points
    best = int(win.best['text'])  # meilleur scores des joueur/euse
    win.best['text'] = after if best < after else best
    playerRanks(info['player'], after)
    

    """regret pour afficher nouveau chiffre"""
    if after > before:
        newTwo()
    elif counter['right'] == 1:
        newTwo()
    else:
        for row in range(rows):
            if label[row][cols-1]['text'] == ' ':
                newTwo()
                break

    colorsAdjust()


# In[11]:


def left():

    rows, cols = win.field.widgets
    label = win.field
    before = int(win.score['text'])
    for row in range(rows):
        for col in range(cols-1, 0, -1):
            if label[row][col - 1]['text'] == ' ':
                label[row][col - 1]['text'] = label[row][col]['text']
                label[row][col]['text'] = ' '
                for cl in range(col, cols-1):
                    label[row][cl]['text'] = label[row][cl+1]['text']
                    label[row][cl+1]['text'] = ' '

            else:
                if label[row][col]['text'] != ' ':
                    first = int(label[row][col]['text'])
                    second = int(label[row][col - 1]['text'])
                    if first == second:
                        label[row][col - 1]['text'] = f"{2 * first}"
                        label[row][col]['text'] = ' '
                        for cl in range(col, cols - 1):
                            label[row][cl]['text'] = label[row][cl + 1]['text']
                            label[row][cl + 1]['text'] = ' '
                        win.score['text'] = int(
                            win.score['text']) + (2 * first)

    after = int(win.score['text'])  # verifier l'augmentation des points
    best = int(win.best['text'])  # meilleur scores des joueur/euse
    win.best['text'] = after if best < after else best
    playerRanks(info['player'], after)

    """regret pour afficher nouveau chiffre"""
    if after > before:
        newTwo()
    elif counter['left'] == 1:
        newTwo()
    else:
        for row in range(rows):
            if label[row][0]['text'] == ' ':
                newTwo()
                break

    colorsAdjust()


# In[12]:


def top():
    #print('top')
    rows, cols = win.field.widgets
    label = win.field
    before = int(win.score['text'])
    for col in range(cols):
        for row in range(rows-1, 0, -1):
            if label[row-1][col]['text'] == ' ':
                label[row-1][col]['text'] = label[row][col]['text']
                label[row][col]['text'] = ' '
                for r in range(row, rows-1):
                    label[r][col]['text'] = label[r + 1][col]['text']
                    label[r + 1][col]['text'] = ' '

            else:
                if label[row][col]['text'] != ' ':
                    first = int(label[row][col]['text'])
                    second = int(label[row-1][col]['text'])
                    if first == second:
                        label[row-1][col]['text'] = f"{2 * first}"
                        label[row][col]['text'] = ' '
                        for r in range(row, rows - 1):
                            label[r][col]['text'] = label[r + 1][col]['text']
                            label[r + 1][col]['text'] = ' '

                        win.score['text'] = int(
                            win.score['text']) + (2 * first)

    after = int(win.score['text'])  # verifier l'augmentation des points
    best = int(win.best['text'])  # meilleur scores des joueur/euse
    win.best['text'] = after if best < after else best
    playerRanks(info['player'], after)

    """regret pour afficher nouveau chiffre"""
    if after > before:
        newTwo()
    elif counter['up'] == 1:
        newTwo()
    else:
        for col in range(cols):
            if label[0][col]['text'] == ' ':
                newTwo()
                break

    colorsAdjust()


# In[13]:


def down():
    #print('down')
    rows, cols = win.field.widgets
    label = win.field
    before = int(win.score['text'])
    for col in range(cols):
        for row in range(rows-1):
            if label[row + 1][col]['text'] == ' ':
                label[row+1][col]['text'] = label[row][col]['text']
                label[row][col]['text'] = ' '
                for r in range(row, 0, -1):
                    label[r][col]['text'] = label[r - 1][col]['text']
                    label[r - 1][col]['text'] = ' '

            else:
                if label[row][col]['text'] != ' ':
                    first = int(label[row][col]['text'])
                    second = int(label[row+1][col]['text'])
                    if first == second:
                        label[row + 1][col]['text'] = f"{2 * first}"
                        label[row][col]['text'] = ' '
                        for r in range(row, 0, -1):
                            label[r][col]['text'] = label[r - 1][col]['text']
                            label[r - 1][col]['text'] = ' '

                        win.score['text'] = int(
                            win.score['text']) + (2 * first)

    after = int(win.score['text'])  # verifier l'augmentation des points
    best = int(win.best['text'])  # meilleur scores des joueur/euse
    win.best['text'] = after if best < after else best
    playerRanks(info['player'], after)

    """regret pour afficher un nouveau chiffre"""
    if after > before:
        newTwo()
    elif counter['down'] == 1:
        newTwo()
    else:
        for col in range(cols):
            if label[rows-1][col]['text'] == ' ':
                newTwo()
                break

    colorsAdjust()


# In[ ]:


def newGame():
    rows, cols = win.field.widgets
    for row in range(rows):
        for col in range(cols):
            win.field[row][col]['text'] = ' '
            win.field[row][col]['bg'] = '#ccc0b3'
    for i in range(2):
        a = randrange(rows)
        b = randrange(cols)
        win.field[a][b]['text'] = 2


if __name__ == '__main__':
    main(1,'BRUCE',0,True)
