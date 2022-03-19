import random,sys, pygame as pg
from tkinter import Tk,messagebox

size = width, height = 400,600

pg.init()
Tk().wm_withdraw()

black = 0,0,0
white = 255,255,255
orange = 255,165,0
green = 0,255,0
screen = pg.display.set_mode(size)
pg.display.set_caption("Wordle")
titleFont = pg.font.SysFont("bahnschrift", 35)
textFont = pg.font.SysFont("bahnschrift", 25)

wordSet = []
with open("dict.txt","r") as file:
    for line in file.readlines():
        wordSet.append(line[:-1])
chosenWord = random.choice(wordSet)
print("Word:",chosenWord)

class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
        self.colour = white
        self.text = ""
        self.txt_surface = textFont.render(self.text, True, self.colour)

    def set_letter(self,contents):
        self.text = contents
        self.txt_surface = textFont.render(self.text, True, white)

    def draw(self):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+10)) # Blit the text.
        pg.draw.rect(screen, self.colour, self.rect, 2)  # Blit the rect.

def make_text(font1,text,x,y):  # Create text object
    tempText = font1.render(text,True,white)
    tempTextRect = tempText.get_rect()
    tempTextRect.center = (x,y)
    return (tempText,tempTextRect)

row = column = 0
boxes = []
wordleText = make_text(titleFont,"WORDLE",width/2,50)
currentAttempt = ""
for i in range(6):
    boxes.append([])
    for j in range(5):
        boxes[-1].append(InputBox(j * 50 + 70,i * 50 + 150,50,50))

while True:
    screen.fill(black)
    screen.blit(wordleText[0],wordleText[1])
    for i in boxes:
        for j in i:
            j.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if pg.key.name(event.key).isalpha() and column != 5 and len(pg.key.name(event.key)) == 1:
                currentAttempt += pg.key.name(event.key)
                boxes[row][column].set_letter(f"  {pg.key.name(event.key)}   ")
                column += 1
            elif event.key == pg.K_BACKSPACE and column != 0:
                currentAttempt = currentAttempt[:-1]
                column -= 1
                boxes[row][column].set_letter("")
            elif event.key == pg.K_RETURN and currentAttempt in wordSet:
                for pos,character in enumerate(currentAttempt):
                    if character == chosenWord[pos]:
                        boxes[row][pos].colour = green
                    elif character in chosenWord:
                        boxes[row][pos].colour = orange
                if currentAttempt == chosenWord:
                    messagebox.showinfo("Wordle","Well done! You've won")
                    break
                elif row == 5:
                    messagebox.showinfo("Wordle",f"Unlucky, the word was {chosenWord}")
                    break
                row += 1
                column = 0
                currentAttempt = ""
    pg.display.flip()