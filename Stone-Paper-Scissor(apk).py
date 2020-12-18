import tkinter
from tkinter import Frame , Label, Pack, Grid, Place, Button, Tk, Entry, StringVar, ACTIVE, DISABLED, RAISED, RIDGE, SUNKEN, TOP, LEFT, RIGHT,X, GROOVE, BOTTOM, FLAT
import tkinter.messagebox as tmsg
import random

# Frame , Label, Pack, Grid, Place, Button, Tk, Entry, StringVar, ACTIVE, DISABLED, RAISED, RIDGE, SUNKEN, TOP, LEFT, RIGHT,X
# Game window
sps_tk = Tk()
sps_tk.title("Stone Paper Scissors")
sps_tk.geometry('610x715')
sps_tk.resizable(0,0)
sps_tk.config(bg="#F1FAEE")
#=======================================================================================================================================
# List used by Computer
sps_lst = ["Stone","Paper", "Scissor"]
#=======================================================================================================================================
# Scores
sps_Player_score = 0
sps_Comp_score = 0
#=======================================================================================================================================
def sps_btnClick(Butns):
    """Handles the player turn and calls checkForWin function"""
    global sps_But1, sps_But2, sps_But3, sps_C_c, sps_lblf, sps_lbl3
    # Computer's Choice
    sps_C_c = random.choice(sps_lst)
    u = " "
    sps_lbl3["text"] =""
    if (Butns["text"] == "Stone" and sps_C_c == "Paper") or (Butns["text"] == "Paper" and sps_C_c == "Scissor") or (Butns["text"] == "Scissor" and sps_C_c == "Stone"):
        sps_lose()
    elif (Butns["text"] == "Stone" and sps_C_c == "Scissor") or (Butns["text"] == "Paper" and sps_C_c == "Stone") or (Butns["text"] == "Scissor" and sps_C_c == "Paper"):
        sps_won()
    elif Butns["text"] ==  sps_C_c:
        sps_tie()
    if Butns["text"] == "Stone":
        u = "Stone"
    elif Butns["text"] == "Paper":
        u = "Paper"
    elif Butns["text"] == "Scissor":
        u = "Scissor"
    sps_lblf["text"] =f"These are the input below \n \n Computer's choice is \n {sps_C_c} \n And user's choice is \n {u}"

def sps_lose():
    global sps_lbl2, sps_Comp_score
    sps_Comp_score += 1 
    sps_lbl2["text"]= f"Computer Score :- {sps_Comp_score}"

def sps_won():
    global sps_lbl1, sps_Player_score
    sps_Player_score += 1
    sps_lbl1["text"] = f"Player Score :- {sps_Player_score}"

def sps_tie():
    global sps_lbl3
    sps_lbl3["text"] =" There is a Tie \n Between Player and Computer"

def sps_fin():
    global sps_Player_score, sps_Comp_score
    if sps_Player_score > sps_Comp_score:
        tmsg.showinfo("Winner","Player wins the game")
    elif sps_Player_score < sps_Comp_score:
        tmsg.showinfo("Winner","Computer wins the game")
    elif sps_Player_score == sps_Comp_score:
        tmsg.showinfo("Tie!!","No-one Wins \nTie b/w Player and Computer")
    sps_tk.destroy()

#=======================================================================================================================================
# Frame to Show Result
sps_F0 = Frame(sps_tk, relief=RIDGE, borderwidth=10, bg='#FDFFB6')
sps_F0.pack(side=TOP, fill=X)
sps_lbl1 = Label(sps_F0, text=f"Player Score :- {sps_Player_score}", font='Magneto 15 bold', bg='#9BF6FF', fg='black', width=20)
sps_lbl1.grid(row=0, column=0)
sps_lbl2 = Label(sps_F0, text=f"Computer Score :- {sps_Comp_score}", font='Magneto 15 bold', bg='#9BF6FF', fg='black', width=20)
sps_lbl2.grid(row=1, column=0)
sps_lbl3 = Label(sps_F0, text="", font='Magneto 10 bold underline', bg='#FDFFB6', fg='black')
sps_lbl3.grid(row=0, column=1, rowspan=2, padx=25)
#=======================================================================================================================================
sps_F1 = Frame(sps_tk, relief=GROOVE, borderwidth=10, bg='#FFB4A2')
sps_F1.pack(side=TOP, fill=X,padx=5,pady=5)
sps_lbl = Label(sps_F1, text=f" Player please select any option ", font='Magneto 15 bold', fg='#b8f2e6', bg='#D62828', height=1, width=20)
sps_lbl.pack(side=TOP, fill=X)
#=======================================================================================================================================
# Buttons to Play the Game
sps_F2 = Frame(sps_tk, relief=GROOVE, borderwidth=10, bg='#E63946')
sps_F2.pack(side=LEFT,padx=10)
# Stone Button 
sps_But1 = Button(sps_F2, text='Stone', font='Times 20 bold italic', bg='#EEF5DB', height=5, width=12, command=lambda: sps_btnClick(sps_But1))
sps_But1.grid(row=0, column=0,padx=2.5, pady=2.5)
# Paper Button
sps_But2 = Button(sps_F2, text= 'Paper', font='Times 20 bold italic', bg='#EEF5DB', height=5, width=12, command=lambda: sps_btnClick(sps_But2))
sps_But2.grid(row=1, column=0,padx=2.5, pady=2.5)
# Scissor Button 
sps_But3 = Button(sps_F2, text='Scissor',font='Times 20 bold italic', bg='#EEF5DB',height=5, width=12, command=lambda: sps_btnClick(sps_But3))
sps_But3.grid(row=2, column=0,padx=2.5, pady=2.5)
#=======================================================================================================================================
# Frame to show computers choice
sps_F = Frame(sps_tk, relief=FLAT)
sps_F.pack(side=RIGHT)
sps_F3 = Frame(sps_F, relief=SUNKEN, borderwidth=5, bg='#E63946')
sps_F3.grid(row=0, column=0)
sps_lblf = Label(sps_F3, text="Please select \n Any option", font='Magneto 15 bold', fg='#8d99ae', bg='#fec89a', height=20, width=25)
sps_lblf.pack(side=RIGHT, fill=X)
# Button to finish the game
sps_B = Button(sps_F, text="Finish the Game",font='Times 10 bold italic', bg='#EEF5DB', fg="#E63946", height=2, width=20, command=sps_fin)
sps_B.grid(row=1, column=0)
#=======================================================================================================================================
sps_tk.mainloop()