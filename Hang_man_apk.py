import tkinter, random
from tkinter import Frame , Label, Pack, Grid, Place, Button, Tk, Text , ACTIVE, DISABLED, RAISED, RIDGE, SUNKEN, TOP, LEFT
from tkinter import RIGHT,X, GROOVE, END, BOTTOM, FLAT, Y, StringVar
import tkinter.messagebox as tmsg

#=======================================================================================================================================
stages = [  # final state: head, torso, both arms, and both legs
                "--------\n|      |\n |     O\n |     \\|/\n|      |\n |     / \\\n ",
                # head, torso, both arms, and one leg
                "--------\n|      |\n |     O\n |     \\|/\n|      |\n|      /\n",
                # head, torso, and both arms
                "--------\n|      |\n |     O\n |     \\|/\n|      |\n|       \n",
                # head, torso, and one arm
                "--------\n|      |\n |     O\n|     \\|\n|      |\n|       \n",
                # head and torso
                "--------\n|      |\n |     O\n|      |\n|      |\n|       \n",
                # head
                "--------\n|      |\n |     O\n|       \n|       \n|       \n",
                # initial empty state
                "--------\n|      ||\n|        \n|        \n|        \n|        "
    ] 

word_list = [ 'wares','soup','mount','extend','brown','expert','tired','humidity','backpack','crust','dent','market','knock','windy','coin','coming','leave','reverse','fake','renewed','goodness','featured','curse','shocked','shove','marked','interact','kidnap','noble','proton','effort','showcase','coil','breeder','pathway','hearing','drain','bill','medal','sarcasm','monopoly','lighter','repair','worship','vent','hybrid','buffet','lively' ] 

tries = 6
#=======================================================================================================================================
def extraaa():
    global hng_lblf12
    # Extra
    hng_lblf7 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf7.grid(row=6,column=0)
    hng_lblf8 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf8.grid(row=7,column=0)
    hng_lblf9 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf9.grid(row=8,column=0)
    hng_lblf10 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf10.grid(row=9,column=0)
    hng_lblf11 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf11.grid(row=10,column=0)
    hng_lblf12 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
    hng_lblf12.grid(row=11,column=0)
#=======================================================================================================================================
# Function Used in apk
def get_word():
    word = random.choice(word_list)
    return word.upper()

def spd_word():
    global Word , guessed_letters, guessed_words 
    guessed_letters = []
    guessed_words = []
    Word = get_word()

def show_word():
    global Word, wordgues
    wordgues = len(Word)*"-"
    hng_lblf5["text"]= wordgues
    hng_lblf6["text"]= f"Length of the Word:-{str(len(Word))}"

def check_word():
    global hng_ent,wordgues, tries,hng_lblf12, hng_lblf5, Word, hng_lblf7, hng_lblf3, guessed_letters, guessed_words,hng_Buts 
    if tries>0 or hng_lblf3["text"] != stages[0]:
        word_as_list= []
        guess = str(hng_ent.get(1.0,1.11)).upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                tmsg.showinfo("Already Guessed", "You had already guessed the Letter")
            elif guess not in Word:
                hng_lblf12["text"] = "Letter is not in the Word"
                tries -= 1
                guessed_letters.append(guess)
            else:
                hng_lblf12["text"] = f"Good job, {guess} is in the word!"
                guessed_letters.append(guess)
                word_as_list = list(wordgues)
                indices = [i for i, letter in enumerate(Word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                wordgues = "".join(word_as_list)
                hng_lblf5["text"]= wordgues
                finalcheck(wordgues)
        elif len(guess) == len(Word) and guess.isalpha():
                if guess in guessed_words:
                    tmsg.showinfo("Already Guessed", "You had already guessed the Word")
                elif guess != Word:
                    hng_lblf12["text"] = f"{guess} is not the word!"
                    tries -= 1
                    guessed_words.append(guess)
                elif guess == Word:
                    hng_lblf5["text"]= guess
                    finalcheck(guess)
        hng_lblf7["text"] =f"No of tries left :-{tries}"
        hng_lblf3["text"] = stages[tries]
        hng_ent.delete(1.0, END)
    else:
        tmsg.showwarning("Tries over!!", "Your chances are over \n Try again later")
    if tries == 0 or hng_lblf3["text"] == stages[0]:
        tmsg.showinfo("Lose!", f"You lose the Game \n Word to be Guesed was '{Word}'")
        retry_but()

def finalcheck(wordguess):
    global Word, hng_lblf12
    if Word == wordguess:
        hng_lblf12["text"] = f"Congratulations, \n You Guessed the word!"
        retry_but()
        
def retry_but():    
    global hng_entf, hng_Buts , hng_Butrs
    hng_Buts.config(state=DISABLED)
    hng_Butrs = Button(hng_entf, text=' Retry ', font='Times 10 italic', bg='#EEF5DB', height=1, width=10, command=retryy)
    hng_Butrs.pack(side=BOTTOM, anchor='e')

def retryy():
    global hng_Butrs, hng_Buts, tries
    tries = 6
    hng_Buts.config(state=ACTIVE)
    hng_Butrs.destroy()
    play_Hangman()
#=======================================================================================================================================
def play_Hangman():
    spd_word()
    show_word()   
    hng_tk.mainloop()
#=======================================================================================================================================
hng_tk = Tk()
hng_tk.title("Hang Man")
hng_tk.geometry('610x715+50+50')
hng_tk.resizable(0,0)
hng_tk.config(bg="#f0efeb")
#=======================================================================================================================================
# Show Hang Man
hng_F_ = Frame(hng_tk, relief=FLAT)
hng_F_.pack(side=BOTTOM,fill=X)
hng_F = Frame(hng_F_, relief=SUNKEN, borderwidth=10, bg='#E63946')
hng_F.grid(row=0,column=1,rowspan=14)
hng_lblf3 = Label(hng_F, text=stages[tries], font='Arial 52 bold', fg='#003049', bg='#f1faee', height=8, width=8)
hng_lblf3.pack()
#=======================================================================================================================================
#=======================================================================================================================================
# Guess the Word Frame
hng_lblf7 = Label(hng_F_, text=f"No of tries left :-{tries}", font='Gabriola 20', fg='#003049', bg='#f0efeb', width=20)
hng_lblf7.grid(row=0,column=0)
hng_lblf4 = Label(hng_F_, text="Guess the Word", font='Harrington 15 bold', fg='#003049', bg='#f0efeb', width=20)
hng_lblf4.grid(row=1,column=0)
hng_lblf5 = Label(hng_F_, text="", font='Castellar 10 bold', fg='#003049', bg='#f0efeb')
hng_lblf5.grid(row=2,column=0)
#=======================================================================================================================================
# Enter the Guess
hng_entf = Frame(hng_F_, relief=GROOVE, borderwidth=2, bg='#E63946', height=8, width=8)
hng_entf.grid(row=3,column=0)
hng_ent = Text(hng_entf, font='lucida 10', height=1, width=25)
hng_ent.pack(side=TOP, fill=X)
hng_Buts = Button(hng_entf, text=' Check ', font='Times 10 italic', bg='#EEF5DB', height=1, width=10, command=check_word)
hng_Buts.pack(side=BOTTOM, anchor='e')
hng_lblf6 = Label(hng_F_, text="", font='Gabriola 20', fg='#003049', bg='#f0efeb')
hng_lblf6.grid(row=4,column=0)
#=======================================================================================================================================
#=======================================================================================================================================
# Top Frame
hng_F1 = Frame(hng_tk, relief=GROOVE, bg='#EEF5DB', borderwidth=2)
hng_F1.pack(side=TOP,fill=X)
hng_lbl0 = Label(hng_F1, text="Welcome to the Hang-Man ", font='Algerian 15', fg='#e63946', bg='#fec89a')
hng_lbl0.pack(ipady=10)
#=======================================================================================================================================
extraaa()   
play_Hangman()
