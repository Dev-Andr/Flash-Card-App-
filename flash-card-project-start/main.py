from tkinter import *
import pandas
import random
import json

green = "#"

t, v = None, None
j = 10
unknown = []


def update_text():
    print("HAHA")
    global j, t
    if j >= 0:
        t = window.after(1000, update_text)  # 1000 milliseconds = 1 second
        canvas.itemconfig(lang, text=f"French [{j}]")
        j -= 1
    else:
        j, t = 10, None
        canvas.itemconfig(img, image=srcc)
        canvas.itemconfig(lang, text="English")
        canvas.itemconfig(word, text=english[v])
        french.pop(v)
        english.pop(v)


def show():
    if not t: return
    global j
    j = -1
    window.after_cancel(t)
    update_text()


def gen():
    if t: return
    i = random.randint(1, len(french))
    global v
    v = i
    canvas.itemconfig(word, text=french[i])
    canvas.itemconfig(img, image=src)

    update_text()


def cross():
    if v is None: return
    if t: return
    unknown.append(canvas.itemcget(word, "text"))
    gen()


words = pandas.read_csv("data/french_words.csv").to_dict()
french = [v for i, v in words["French"].items()]
english = [v for i, v in words["English"].items()]

window = Tk()
window.title("Frenglish")
window.config(padx=50, pady=50, bg=green)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=green)
src = PhotoImage(file="images/card_back.png")
srcc = PhotoImage(file="images/card_front.png")

img = canvas.create_image(400, 263, image=src)

lang = canvas.create_text(400, 150, text="French (Press any button)", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 270, text="English (to start)", font=("Ariel", 70, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

imgT = PhotoImage(file="images/right.png")
b_tick = Button(image=imgT, highlightthickness=0, bg=green, command=gen)
b_tick.grid(column=1, row=1)

imgC = PhotoImage(file="images/wrong.png")
b_cross = Button(image=imgC, highlightthickness=0, bg=green, command=cross)
b_cross.grid(column=0, row=1)

b_show = Button(text="SHOW", bg=green, command=show, font=("Jokerman", 20, "bold"))
b_show.grid(column=0, row=1, columnspan=2)

fr = french.copy()
en = english.copy()


def save():
    val = {fr[en.index(i)]:i for i in unknown}

    try:
        with open("to_learn.json", 'r') as f:
            d = json.load(f)
            d.update(val)
    except FileNotFoundError:
        d = val

    with open("to_learn.json", 'w') as f:
        json.dump(d, f, indent=4)
    window.destroy()



window.protocol("WM_DELETE_WINDOW", save)
window.mainloop()
