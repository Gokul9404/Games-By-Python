# Game gm_board using in the program
gm_board = ['-','-','-',
            '-','-','-',
            '-','-','-']
# Starting Player
player = "x"
# Winner constant
winner = None
# Game is going on
Game_on = True
#__________________________Below Functios are Used to Play the Game and Update the Board_______________________________________________
# Show The Game Board
def show_gm_board():
    for x in range(3):
        p = (x*3)
        print(" ", p+1," "," ", p+2 ," "," ", p+3 ,"        ","|",gm_board[p+0],"|","|",gm_board[p+1],"|","|",gm_board[p+2],"|")

# Change the Cuurent Player for other Players Chance
def player_change(current_player):
    global player
    if current_player == "x":
        player = "o"
    elif current_player == "o":
        player = "x"
    return player

# Take Player's Input to put their Mark Onto The Board
def inputt():
    global c
    c1 = input("At which you want to place your mark [b/w 1-9]:-")
    no = ["1",'2','3','4','5','6','7','8','9']
    if c1 not in  no:
        print("-------------------------")
        print("      Invalid Input!     ")
        print("   Inter valid Character ")
        print("-------------------------")
        inputt()
    else:
        c = int(int(c1) - 1)
        # Check valid place or not
        if gm_board[c]=='o' or gm_board[c] == "x":
            print("The place is already occupied!")
            print("Please anthoer Place")
            inputt()
        else:
            update_gm_board()

# Update the Game Board After User's Input
def update_gm_board():
    global c
    gm_board[c] = player
    player_change(player)

# Run the Game until or Game get Finished/Over
def play():
    while Game_on: 
        show_gm_board()
        print(f"{player}'s chance is there")
        inputt()
        check_Finish()

#_______________________Below Functios are Used to Check whether the Game need to be Finished or not____________________________________
def check_Finish():
    Check_win()
    check_tie()

# Checks for a winner
def Check_win():
    global winner, Game_on, winnner
    row_win = check_rows()
    column_win = check_columns()
    daigonal_win = check_diagonals()
    if row_win:
        winner = row_win
    elif column_win:
        winner = column_win
    elif daigonal_win:
        winner = daigonal_win
    else:
        winner = None
        return None
    # If any Player won then showing it
    if winner == "o" or winner == "x":
        Game_on, winnner = False, True
        print()
        show_gm_board()
        print()
        " ------------ Game Over!! ------------ "
        print(f"The Winner of the Game is :--- {winner}")
        print()
        print()

# Check the rows for a win
def check_rows():
  global Game_on
  row_1 = gm_board[0] == gm_board[1] == gm_board[2] != "-"
  row_2 = gm_board[3] == gm_board[4] == gm_board[5] != "-"
  row_3 = gm_board[6] == gm_board[7] == gm_board[8] != "-"
  if row_1 or row_2 or row_3:
    Game_on = False
  if row_1:
    return gm_board[0] 
  elif row_2:
    return gm_board[3] 
  elif row_3:
    return gm_board[6] 
  else:
    return None

# Check the columns for a win
def check_columns():
  global Game_on
  column_1 = gm_board[0] == gm_board[3] == gm_board[6] != "-"
  column_2 = gm_board[1] == gm_board[4] == gm_board[7] != "-"
  column_3 = gm_board[2] == gm_board[5] == gm_board[8] != "-"
  if column_1 or column_2 or column_3:
    Game_on = False
  if column_1:
    return gm_board[0] 
  elif column_2:
    return gm_board[1] 
  elif column_3:
    return gm_board[2] 
  else:
    return None

# Check the diagonals for a win
def check_diagonals():
  global Game_on
  diagonal_1 = gm_board[0] == gm_board[4] == gm_board[8] != "-"
  diagonal_2 = gm_board[2] == gm_board[4] == gm_board[6] != "-"
  if diagonal_1 or diagonal_2:
    Game_on = False
  if diagonal_1:
    return gm_board[0] 
  elif diagonal_2:
    return gm_board[2]
  else:
    return None

# Check if there is a tie
def check_tie():
  global Game_on, winnner
  if "-" not in gm_board and not winnner:
    Game_on = False
    show_gm_board()
    print(" ------------ Game Over!! ------------ ")
    print("There is a tie Between both the Players")
    print(" ------------ Game Over!! ------------ ")
    return True
  else:
    return False

# Play The Game 
if __name__ == "__main__":
    play()
   