from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk


STARTING = 0

deck = list()
cellColor = ['White', 'Brown']

pieceColors = ['White', 'Black']
MOVE = STARTING
PATH = "images/"

HISTORY = list()
HistoryPointer = -1
KILLS = list()

names = ['Rock', 'Knight', 'Bishop', 'Queen']

def RESTART():
    while len(deck) > 0: deck.pop(0)
    for i in range(0, 8):
        row = list()
        for j in range(0, 8):
            row.append(Cell(figureNames[i][j], j, i, figureColors[i][j], root))
        deck.append(row)
    global MOVE, HistoryPointer
    MOVE = STARTING
    HISTORY = []
    HistoryPointer = -1

def kill(i1, j1, mode=0):
    deck[i1][j1].color = 'empty'
    deck[i1][j1].name = 'empty'
    if mode == 0 or mode == 2:
        deck[i1][j1].photo = ImageTk.PhotoImage(Image.open(PATH + "emptyempty.png"))
        deck[i1][j1].button['image'] = deck[i1][j1].photo

class BackUpValue:
    def __init__(self, value):
        self.fromx = value.fromx
        self.fromy = value.fromy
        self.x = value.x
        self.y = value.y
        self.name = value.name
        self.cntOfMoves = value.cntOfMoves
        self.color = value.color
        self.photo = value.photo


def move(i1, j1, i, j, mode=0):
    global HISTORY, HistoryPointer
    HistoryPointer += 1
    if HistoryPointer == len(HISTORY):
        HISTORY.append([])
    # mode == 2 If and Only If move is the second part of Rocking
    if mode == 2:
        HISTORY[HistoryPointer] = [[i1, j1], [i, j], 0]
    else:
        if deck[i][j].color != deck[i1][j1].color and deck[i][j].color != 'empty':
            HISTORY[HistoryPointer] = [[i1, j1], [i, j], 0, 0]
            KILLS.append(BackUpValue(deck[i][j]))
        else:
            HISTORY[HistoryPointer] = [[i1, j1], [i, j]]
    print(HISTORY)
    if mode == 0 or mode == 2:
        deck[i][j].photo = deck[i1][j1].photo
        deck[i][j].button['image'] = deck[i][j].photo
        deck[i][j].fromx, deck[i][j].fromy = j1, i1
        deck[i][j].cntOfMoves = deck[i1][j1].cntOfMoves + 1
    deck[i][j].name, deck[i][j].color = deck[i1][j1].name, deck[i1][j1].color
    kill(i1, j1, mode)

def choose(name, i, j, img, window):
    window.destroy()
    deck[i][j].name = name
    deck[i][j].photo = img
    deck[i][j].button['image'] = deck[i][j].photo


def change(i, j):
    global photos, names
    c = 0
    if deck[i][j].color == 'Black': c = 1
    window = Toplevel(deck[i][j].root)
    rockLabel = Label(window, image = photos[c][0])
    rockLabel.pack(side = RIGHT)
    rockLabel.bind('<Button-1>', lambda event: choose('Rock', i, j, photos[c][0], window))
    knightLabel = Label(window, image = photos[c][1])
    knightLabel.pack(side = RIGHT)
    knightLabel.bind('<Button-1>', lambda event: choose('Knight', i, j, photos[c][1], window))
    bishopLabel = Label(window, image = photos[c][2])
    bishopLabel.pack(side = RIGHT)
    bishopLabel.bind('<Button-1>', lambda event: choose('Bishop', i, j, photos[c][2], window))
    queenLabel = Label(window, image = photos[c][3])
    queenLabel.pack(side = RIGHT)
    queenLabel.bind('<Button-1>', lambda event: choose('Queen', i, j, photos[c][3], window))
    window.grab_set()

def isCheck(color):
    for i in range(0, 8):
        for j in range(0, 8):
            if deck[i][j].color != color and deck[i][j].color != 'empty':
                for p in deck[i][j].underAtack():
                    if p.color == color and p.name == 'King':
                        return True
    return False

was = []

def trymove(i, j, i1, j1, mode):
    global was
    if mode == 0:
        was = [deck[i1][j1].name, deck[i1][j1].color]
        deck[i1][j1].name, deck[i1][j1].color = deck[i][j].name, deck[i][j].color
        deck[i][j].name, deck[i][j].color = 'empty', 'empty'
    else:
        deck[i][j].name, deck[i][j].color = deck[i1][j1].name, deck[i1][j1].color
        deck[i1][j1].name, deck[i1][j1].color = was[0], was[1]

LIST = []
pressed = []

def press(i, j):
    if len(pressed) == 0:
        global MOVE
        if deck[i][j].color != pieceColors[MOVE]:
            return
        global LIST
        LIST = []
        under = deck[i][j].underMove()
        for p in under:
            trymove(i, j, p.y, p.x, 0)
            check = isCheck(deck[p.y][p.x].color)
            trymove(i, j, p.y, p.x, 1)
            if check == False:
                p.button['background'] = 'green'
                LIST.append(p)
        under = deck[i][j].underAtack()
        for p in under:
            trymove(i, j, p.y, p.x, 0)
            check = isCheck(deck[p.y][p.x].color)
            trymove(i, j, p.y, p.x, 1)
            if check == False and p.color != deck[i][j].color and p.color != 'empty':
                p.button['background'] = 'red'
                LIST.append(p)
        if deck[i][j].name == 'King' and deck[i][j].cntOfMoves == 0:
            okr = False
            okl = False
            if j == 4:
                if isFree(i, j+1, deck[i][j].color) and isFree(i, j+2, deck[i][j].color) and deck[i][j+3].name == 'Rock' and deck[i][j+3].color == deck[i][j].color and deck[i][j+3].cntOfMoves == 0:
                    okr = True
                if isFree(i, j-1, deck[i][j].color) and isFree(i, j-2, deck[i][j].color) and isFree(i, j-3, deck[i][j].color) and deck[i][0].name == 'Rock' and deck[i][0].color == deck[i][j].color and deck[i][0].cntOfMoves == 0:
                    okl = True
            else:
                if isFree(i, j-1, deck[i][j].color) and isFree(i, j-2, deck[i][j].color) and deck[i][j-3].name == 'Rock' and deck[i][j-3].color == deck[i][j].color and deck[i][j-3].cntOfMoves == 0:
                    okl = True
                if isFree(i, j+1, deck[i][j].color) and isFree(i, j+2, deck[i][j].color) and isFree(i, j+3, deck[i][j].color) and deck[i][7].name == 'Rock' and deck[i][7].color == deck[i][j].color and deck[i][0].cntOfMoves == 0:
                    okr = True
            if okl == True:
                deck[i][j-2].button['background'] = 'green'
                LIST.append(deck[i][j-2])
            if okr == True:
                deck[i][j+2].button['background'] = 'green'
                LIST.append(deck[i][j+2])
        deck[i][j].button['background'] = 'yellow'
        pressed.append([i, j])
    else:
        i1, j1 = pressed[0][0], pressed[0][1]
        if (len(LIST) == 0):
            deck[i1][j1].button['background'] = cellColor[(i1 + j1)%2]
            pressed.pop(0)
            press(i, j)
            return
        if i1 == i and j1 == j: return
        found = 0
        for p in LIST:
            if deck[i][j] == p:
                found = 1
                break
        if found == 0:
            pressed.pop(0)
            for p in LIST:
                p.button['background'] = cellColor[(p.x + p.y)%2]
            while len(LIST):
                LIST.pop(0)
            deck[i1][j1].button['background'] = cellColor[(i1+j1)%2]
            press(i, j)
            return
        move(i1, j1, i, j)
        if deck[i][j].name == 'King':
            if i == i1:
                if j - j1 == 2:
                    move(i, 7, i, j-1, 2)
                elif j - j1 == -2:
                    move(i, 0, i, j+1, 2)
        if deck[i][j].name == 'Pawn':
            if i == 0 or i == 7:
                change(i, j)
        for p in LIST:
            p.button['background'] = cellColor[(p.x + p.y)%2]
        while len(LIST):
            LIST.pop(0)
        deck[i1][j1].button['background'] = cellColor[(i1+j1)%2]
        pressed.pop(0)
        MOVE = 1 - MOVE
        if isCheck(pieceColors[MOVE]):
            Ok = False
            for i in range(0, 8):
                for j in range(0, 8):
                    if deck[i][j].color == pieceColors[MOVE]:
                        press(i, j)
                        if LIST != []:
                            Ok = True
                        deck[i][j].background = cellColor[(i+j)%2]
                        deck[i][j].button['background'] = deck[i][j].background
                        while len(LIST) > 0:
                            y = LIST[0].y
                            x = LIST[0].x
                            deck[y][x].background = cellColor[(y+x)%2] 
                            deck[y][x].button['background'] = deck[y][x].background
                            LIST.pop(0)
                    if Ok: break
                if Ok: break
            if not Ok:
                if not messagebox.askyesno(message = 'Checkmate!\nWanna play one more time?', title = 'Oops..'):
                    root.destroy()
                else:
                    RESTART()
        '''for i in range(0, 8):
            for j in range(0, 8):
                print(f"{deck[i][j].name[0]} ", end='')
            print()
        print()'''

def isFree(y, x, color):
    if deck[y][x].name != 'empty': return False
    for i in range(0, 8):
        for j in range(0, 8):
            if deck[i][j].color != color:
                for p in deck[i][j].underMove():
                    if p == deck[y][x]: return False
                for p in deck[i][j].underAtack():
                    if p == deck[y][x]: return False
    return True

def Back(event):
    print("Going back in time...")
    global HistoryPointer, HISTORY, MOVE
    if HistoryPointer == len(HISTORY) or HistoryPointer < 0: return
    need = False
    needRestore = False
    BackUp = None
    if len(HISTORY[HistoryPointer]) != 3:
        MOVE = 1 - MOVE
        if len(HISTORY[HistoryPointer]) == 4:
            needRestore = True
            BackUp = KILLS[len(KILLS)-1]
            KILLS.pop(len(KILLS)-1)
    else: need = True
    From = HISTORY[HistoryPointer][0]
    To = HISTORY[HistoryPointer][1]
    HistoryPointer -= 1
    tmp = []
    for i in range(0, HistoryPointer+1):
        tmp.append(HISTORY[i])
    
    move(To[0], To[1], From[0], From[1])
    
    HISTORY = tmp
    HistoryPointer -= 1
    deck[From[0]][From[1]].cntOfMoves -= 2
    if needRestore:
        print("Restoring")
        i, j = To[0], To[1]
        print(BackUp)
        deck[i][j].fromx = BackUp.fromx
        deck[i][j].fromy = BackUp.fromy
        deck[i][j].x = BackUp.x
        deck[i][j].y = BackUp.y
        deck[i][j].name = BackUp.name
        deck[i][j].cntOfMoves = BackUp.cntOfMoves
        deck[i][j].color = BackUp.color
        deck[i][j].photo = BackUp.photo
        deck[i][j].button['image'] = deck[i][j].photo
    if need: Back(0)


class Cell:
    def __init__(self, name, posx, posy, color, root):
        self.fromx = posx
        self.fromy = posy
        self.x = posx
        self.y = posy
        self.name = name
        self.cntOfMoves = 0
        self.color = color
        self.root = root
        self.photo = ImageTk.PhotoImage(Image.open(PATH + self.color + self.name + ".png"))
        self.button = Label(self.root)
        self.button.bind('<Button-1>', self.Press)
        self.button['background'] = cellColor[(self.x+self.y)%2]
        self.button['image'] = self.photo
        self.button.place(relx=0.125*self.x, rely=0.125*self.y, relwidth=0.125, relheight=0.125)
    def underAtack(self):
        res = []
        if self.name == 'Pawn':
            if self.color == pieceColors[STARTING]:
                if self.x < 7 and self.y > 0:
                    res.append(deck[self.y-1][self.x+1])
                if self.x > 0 and self.y > 0:
                    res.append(deck[self.y-1][self.x-1])
            else:
                if self.x < 7 and self.y < 7:
                    res.append(deck[self.y+1][self.x+1])
                if self.x > 0 and self.y < 7:
                    res.append(deck[self.y+1][self.x-1])
        elif self.name == 'Rock':
            i, j = self.y-1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
            i, j = self.y+1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i += 1
            i, j = self.y, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                j -= 1
            i, j = self.y, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                j += 1
        elif self.name == 'Bishop':
            i, j = self.y-1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
                j -= 1
            i, j = self.y+1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i += 1
                j -= 1
            i, j = self.y+1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                j += 1
                i += 1
            i, j = self.y-1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
                j += 1
        elif self.name == 'Queen':
            i, j = self.y, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                j += 1
            i, j = self.y, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                j -= 1
            i, j = self.y-1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
            i, j = self.y+1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i += 1
            i, j = self.y-1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
                j -= 1
            i, j = self.y-1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i -= 1
                j += 1
            i, j = self.y+1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i += 1
                j -= 1
            i, j = self.y+1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty':
                    if deck[i][j].color != self.color:
                        res.append(deck[i][j])
                    break
                i += 1
                j += 1
        elif self.name == 'Knight':
            i, j = self.y-1, self.x-2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x+2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y-2, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y-2, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x-2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x+2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+2, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+2, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
        elif self.name == 'King':
            i, j = self.y-1, self.x
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color != self.color and deck[i][j].color != 'empty':
                res.append(deck[i][j])
        return res
    def underMove(self):
        res = []
        if self.name == 'Pawn':
            if self.color == pieceColors[STARTING]:
                i, j = self.y-1, self.x
                if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                    res.append(deck[i][j])
                    i -= 1
                    if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty' and self.cntOfMoves == 0:
                        res.append(deck[i][j])
            else:
                i, j = self.y+1, self.x
                if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                    res.append(deck[i][j])
                    i += 1
                    if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty' and self.cntOfMoves == 0:
                        res.append(deck[i][j])
        elif self.name == 'Rock':
            i, j = self.y-1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                i -= 1
            i, j = self.y+1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                i += 1
            i, j = self.y, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                j -= 1
            i, j = self.y, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                j += 1
        elif self.name == 'Bishop':
            i, j = self.y-1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                i -= 1
                j -= 1
            i, j = self.y+1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                i += 1
                j -= 1
            i, j = self.y+1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                j += 1
                i += 1
            i, j = self.y-1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].name == 'empty':
                    res.append(deck[i][j])
                else:
                    break
                i -= 1
                j += 1
        elif self.name == 'Queen':
            i, j = self.y, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                j += 1
            i, j = self.y, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                j -= 1
            i, j = self.y-1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i -= 1
            i, j = self.y+1, self.x
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i += 1
            i, j = self.y-1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i -= 1
                j -= 1
            i, j = self.y-1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i -= 1
                j += 1
            i, j = self.y+1, self.x-1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i += 1
                j -= 1
            i, j = self.y+1, self.x+1
            while True:
                if i < 0 or i > 7 or j < 0 or j > 7: break
                if deck[i][j].color != 'empty': break
                res.append(deck[i][j])
                i += 1
                j += 1
        elif self.name == 'Knight':
            i, j = self.y-1, self.x-2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x+2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y-2, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y-2, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x-2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x+2
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+2, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+2, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
        elif self.name == 'King':
            i, j = self.y-1, self.x
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x+1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y+1, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
            i, j = self.y-1, self.x-1
            if i > -1 and i < 8 and j < 8 and j > -1 and deck[i][j].color == 'empty':
                res.append(deck[i][j])
        return res
    def Press(self, event):
        press(self.y, self.x)
        return


root = Tk()

root.geometry('500x500')
root.resizable(0, 0)
root.title('Chess beta')

root.bind_all('<Return>', Back)

photos = []
for color in pieceColors:
    lst = []
    for name in names:
        lst.append(ImageTk.PhotoImage(Image.open(PATH + color + name + '.png')))
    photos.append(lst)


QueenKing = ['Queen', 'King']

figureNames = [
        ['Rock', 'Knight', 'Bishop', QueenKing[STARTING], QueenKing[1-STARTING], 'Bishop', 'Knight', 'Rock'],
        ['Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn'],
        ['Rock', 'Knight', 'Bishop', QueenKing[STARTING], QueenKing[1-STARTING], 'Bishop', 'Knight', 'Rock']
    ]

figureColors = [
        [pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING]],
        [pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING], pieceColors[1-STARTING]],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
        [pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING]],
        [pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING], pieceColors[STARTING]]
    ]

for i in range(0, 8):
    row = list()
    for j in range(0, 8):
        row.append(Cell(figureNames[i][j], j, i, figureColors[i][j], root))
    deck.append(row)
root.mainloop()