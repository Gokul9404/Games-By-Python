import tkinter
from tkinter import Frame , Label, Pack, Grid, Place, Button, Tk, Entry, StringVar, ACTIVE, DISABLED, RAISED, RIDGE, SUNKEN,TOP,BOTTOM,X
import tkinter.messagebox as tmsg

# Game window
Gm_tk = Tk()
Gm_tk.title("Tic Tac Toe")
Gm_tk.geometry('610x715')
Gm_tk.resizable(0,0)
Gm_tk.config(bg="#ffe78f")
Gm_tk.wm_iconbitmap(r'E:\pyhton progs\Games\icnn.ico')

#=======================================================================================================================================
Buts = StringVar()
# Name of the Winner will be set Here
Winner_Name = StringVar()
#Global Variable for player's chance and to check tie 
player_turn = "x"
turn_no = 0
win = 1
# Score of player 1(s1) and player 2(s2)
s1, s2 = 0 , 0
#=======================================================================================================================================
# Functions used in the Game
def sub():
    '''Function to submit names of the player'''
    global player1_name, player2_name, player1_score, player2_score
    if len(p1.get())==0 or len(p2.get())==0:
        tmsg.showerror('Enter Name!',"Plaese enter the names of the player")
    else:
        player1_name.destroy()
        F1.grid_configure(padx=20)
        lbl1.config(text=f'Player 1: {str(p1.get())}', width=15, bg="#fadcac")
        lbl2.config(text=f'Player 2: {str(p2.get())}', width=15, bg="#fadcac")
        player2_name.destroy()
        Fs1 = Frame(FM, relief=RIDGE, borderwidth=10, bg='#f7d6bf')
        Fs1.grid(row=0, column=4, rowspan=2, columnspan=2, padx=30)
        player1_score = Label(Fs1,text=f'Score of Player 1:- {str(s1)}',bg="#e3dfc8",fg="#D00000",font='Pristina 15 underline',width=15)
        player1_score.grid(row=0, column=0, ipadx=8)
        player2_score = Label(Fs1,text=f'Score of Player 2:- {str(s2)}',bg="#e3dfc8",fg="#D00000",font='Pristina 15 underline',width=15)
        player2_score.grid(row=1, column=0, ipadx=8)
        chn["text"] = "Chance of Player 1 :- X"
        But_sub.destroy()

def disableButton():
    """Disable the Buttons when any player wins"""
    global But1, But2, But3, But4, But5, But6, But7, But8, But9
    But1.configure(state=DISABLED)
    But2.configure(state=DISABLED)
    But3.configure(state=DISABLED)
    But4.configure(state=DISABLED)
    But5.configure(state=DISABLED)
    But6.configure(state=DISABLED)
    But7.configure(state=DISABLED)
    But8.configure(state=DISABLED)
    But9.configure(state=DISABLED)

def rep():
    """Enable the Buttons when Replay the Game"""
    global But1, But2, But3, But4, But5, But6, But7, But8, But9, But_rep
    But1.configure(state=ACTIVE, text=" ")
    But2.configure(state=ACTIVE, text=" ")
    But3.configure(state=ACTIVE, text=" ")
    But4.configure(state=ACTIVE, text=" ")
    But5.configure(state=ACTIVE, text=" ")
    But6.configure(state=ACTIVE, text=" ")
    But7.configure(state=ACTIVE, text=" ")
    But8.configure(state=ACTIVE, text=" ")
    But9.configure(state=ACTIVE, text=" ")
    But_rep.destroy()

def btnClick(Butns):
    """Handles the player turn and calls checkForWin function"""
    global turn_no, player_turn, But1, But2, But3, But4, But5, But6, But7, But8, But9, chn
    if len(p1.get())==0 or len(p2.get())==0 or But_sub.winfo_exists():
        tmsg.showerror('Enter Name!',"Plaese submit the names of the player")
    else:
        if Butns["text"] == " " and player_turn == "x":
            Butns.config(fg='#4F6368')
            Butns["text"] = "X"
            player_turn= "o"
            checkForWin()
            chn["text"] = "Chance of Player 2 :- O"
            turn_no += 1
        elif Butns["text"] == " " and player_turn == "o":
            Butns.config(fg='#FE5F55')
            Butns["text"] = "O"
            player_turn= "x"
            checkForWin()
            chn["text"] = "Chance of Player 1 :- X"
            turn_no += 1
        else:
            tmsg.showinfo("Tic-Tac-Toe", "Button already Clicked!")

def checkForWin():
    """Checks the Conditions of winning of any Player or Condition of Tie b/w Players"""
    global Winner_Name, But1, But2, But3, But4, But5, But6, But7, But8, But9, turn_no, But_rep, But_fin, s1, s2, player1_score, player2_score, win
    if ((But1['text'] == 'X' and But2['text'] == 'X' and But3['text'] == 'X') or
        (But4['text'] == 'X' and But5['text'] == 'X' and But6['text'] == 'X') or
        (But7['text'] =='X' and But8['text'] == 'X' and But9['text'] == 'X' )or
        (But1['text'] == 'X' and But5['text'] == 'X' and But9['text'] == 'X') or
        (But3['text'] == 'X' and But5['text'] == 'X' and But7['text'] == 'X') or
        (But1['text'] == 'X' and But4['text'] == 'X' and But7['text'] == 'X') or
        (But2['text'] == 'X' and But5['text'] == 'X' and But8['text'] == 'X') or
        (But7['text'] == 'X' and But6['text'] == 'X' and But9['text'] == 'X')):
        disableButton()
        turn_no = 0
        s1 += 1
        Winner_Name = p1.get() + " Wins!"
        tmsg.showinfo("Tic-Tac-Toe", Winner_Name)
        win = 0
        player1_score['text'] = f'Score of Player 1:-{str(s1)}'

    elif(turn_no == 9):
        tmsg.showinfo("Tic-Tac-Toe", "It is a Tie")
        win = 0

    elif ((But1['text'] == 'O' and But2['text'] == 'O' and But3['text'] == 'O') or
          (But4['text'] == 'O' and But5['text'] == 'O' and But6['text'] == 'O') or
          (But7['text'] == 'O' and But8['text'] == 'O' and But9['text'] == 'O') or
          (But1['text'] == 'O' and But5['text'] == 'O' and But9['text'] == 'O') or
          (But3['text'] == 'O' and But5['text'] == 'O' and But7['text'] == 'O') or
          (But1['text'] == 'O' and But4['text'] == 'O' and But7['text'] == 'O') or
          (But2['text'] == 'O' and But5['text'] == 'O' and But8['text'] == 'O') or
          (But7['text'] == 'O' and But6['text'] == 'O' and But9['text'] == 'O')):
        disableButton()
        turn_no = 0
        s2 += 1
        Winner_Name = p2.get() + " Wins!"
        tmsg.showinfo("Tic-Tac-Toe", Winner_Name)
        win = 0
        player2_score['text'] = f'Score of Player 2:-{str(s2)}'
    if win == 0:
        F1.grid_configure(padx=0)
        But_rep = Button(FM, text=' Replay ', font='Arial 12 italic',fg='#E63946', bg='#FDFFB6', command=rep)
        But_rep.grid(row=0, column=6)
        But_fin = Button(FM, text=' Finish ', font='Arial 12 italic', fg='#E63946', bg='#FDFFB6', command=Finish)
        But_fin.grid(row=1, column=6, ipadx=4)
        win += 1

def Finish():
    '''When Finish button get clicked it will finish the Game'''
    global But_rep, But_fin
    if s1 > s2:
        tmsg.showinfo('Game Finished...',f'Winner of the Game \nPlayer 1 :- {p1.get()} \nThe game is going to Finish Itself')
    elif s2 > s1:
        tmsg.showinfo('Game Finished...',f'Winner of the Game \nPlayer 2 :- {p2.get()} \nThe game is going to Finish Itself')
    elif s2 == s1:
        tmsg.showinfo('Game Finished...',f"There is Tie Between The Player's \n The game is going to Finish Itself")
    rep()
    disableButton()
    Gm_tk.destroy()

#=======================================================================================================================================
# Entry Box frame for Player's Name Input
FM = Frame(Gm_tk, relief=RAISED, borderwidth=10, bg='#ea5455')
FM.pack(side=TOP, anchor='n', fill=X)
F1 = Frame(FM, relief=RAISED, borderwidth=10, bg='#ffaa71')
F1.grid(row=0, column=0, rowspan=2, padx=30)
# Entry Box & Label for Player 1
lbl1 = Label(F1, text="Player 1:-", font='Magneto 15 bold', bg='#ffaa71', fg='black',width=10)
lbl1.grid(row=0, column=0)
p1 = StringVar()
player1_name = Entry(F1, textvariable=p1, bd=5)
player1_name.grid(row=0, column=1)
# Entry Box & Label for Player 2
lbl2 = Label(F1, text="Player 2:-", font='Magneto 15 bold', bg='#ffaa71', fg='black',width=10)
lbl2.grid(row=1, column=0)
p2 = StringVar()
player2_name = Entry(F1, textvariable=p2, bd=5)
player2_name.grid(row=1, column=1)
# Button to the Submit names of Player
But_sub = Button(F1, text=' Submit name ', font='Times 20 bold', bg='#F4F1DE', fg='#003049', command=sub)
But_sub.grid(row=0, column=3, rowspan=2,padx=15)
#=======================================================================================================================================
# Show Who's Chance is there
chn = Label(Gm_tk, text="-------------------------------------------------------------------------", font='Harrington 15 bold', bg='#ffe78f', fg='black')
chn.pack(side=TOP, fill=X)
#=======================================================================================================================================
# Buttons to Play the Game
F2 = Frame(Gm_tk, relief=RAISED, borderwidth=10, bg='#ff5722')
F2.pack(side=BOTTOM, padx=5,pady=5)
#  O-x Button / Box 1
But1 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But1))
But1.grid(row=0, column=0,padx=2.5, pady=2.5)
# O-x Button / Box 2
But2 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But2))
But2.grid(row=0, column=1,padx=2.5, pady=2.5)
# O-x Button / Box 3
But3 = Button(F2, text=' ',font='Times 20 bold', bg='#EEF5DB',height=5, width=10, command=lambda: btnClick(But3))
But3.grid(row=0, column=2,padx=2.5, pady=2.5)
# O-x Button / Box 4
But4 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But4))
But4.grid(row=1, column=0,padx=2.5, pady=2.5)
# O-x Button / Box 5
But5 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But5))
But5.grid(row=1, column=1,padx=2.5, pady=2.5)
# O-x Button / Box 6
But6 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But6))
But6.grid(row=1, column=2,padx=2.5, pady=2.5)
# O-x Button / Box 7
But7 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But7))
But7.grid(row=2, column=0,padx=2.5, pady=2.5)
# O-x Button / Box 8
But8 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But8))
But8.grid(row=2, column=1,padx=2.5, pady=2.5)
# O-x Button / Box 9
But9 = Button(F2, text=' ', font='Times 20 bold', bg='#EEF5DB', height=5, width=10, command=lambda: btnClick(But9))
But9.grid(row=2, column=2,padx=2.5, pady=2.5)

#=======================================================================================================================================
# Play The Game In The PYTHON File Itself
if __name__ == "__main__":
    Gm_tk.mainloop()
