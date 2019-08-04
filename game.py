#This program will let two users play Mancala or let one user play Mancala against a program.
#8/4/2019
#CC by SA (Creative Commons Attribution ShareAlike)

#These are the mancala boards. row1 belongs to player 2 and row 2 belongs to player 1. The game moves clockwise
row1 = [4, 4, 4, 4, 4, 4]
row2 = [4, 4, 4, 4, 4, 4]

#translate will be used for the movement of the peices. It builds the relationship between row1 and row2. For eample,
#0 on row2 is the same as 5 on row1
translate = [5, 4, 3, 2, 1, 0]
#Scoreboard for the game
player1 = 0
player2 = 0

#Initial key to start the game
playing = 1

#Play is a function that will actually make the moves. It just needs to know the column and row of the move it needs to
#make. Warning, columns start with 0 (Can be changed if needed).
def play(col, row):
    #We will use startRow and otherRow to edit the game board. The process will make more sense if you think about
    #each move being made from player 1's point of view. startRow and otherRow will always shift to this point of view
    if row == 2:
        startRow = row2
        otherRow = row1
        player = player1
    else:
        startRow = row1.copy() #use copy because we need to reverse the order of startRow and not change row1
        otherRow = row2.copy()
        startRow.reverse()
        otherRow.reverse()
        player = player2
        col = translate[col]

    number = startRow[col] #The number of marbles

    startRow[col] = 0 #Empty the hole we picked
    index = col + 1 #start counting at the hole next to the one we picked
    start = 1
    while start:

        #This first loop will go through the first row
        while (number > 0) & (index < len(startRow)):
            startRow[index] += 1
            index += 1
            number += -1

        #At this point, we need to check if we made it to the end. We will have made it to the end if we still have
        #marbles (number > 0).
        if number > 0:
            player += 1 #Since we still have marbles, we add one to our points
            index = 5 #now index will start at 5 because we have to start adding from 5 to 0 (clockwise) on otherRow
            number += -1

            #first check if we still have marbles. If we do not, than that means the last marble landed on the point
            #hole, which earns the player another turn. Thus, play will return 1 (true)
            if number == 0:
                results(row, player, startRow, otherRow) #call results to make the final changes to the board
                return 1

            #This loop happens if we still have marbles. It starts running through otherRow
            while (number > 0) & (index >= 0):
                otherRow[index] += 1
                number += -1
                index += -1 #notice we count backwards

            #We need to check if we still have marbles. If we do not, this turn finishes without an additional one
            if number == 0:
                results(row, player, startRow, otherRow)
                return 0
            else:
                index = 0

        #This elif will activate if we do not have marbles. We need to check if the last hole we landed on was empty.
        #if it was (has one) then we can steal the other player's marbles.
        elif startRow[index -1] == 1:
            player += otherRow[index-1]
            otherRow[index-1] = 0
            results(row, player, startRow, otherRow)
            return 0
        else:
            results(row, player, startRow, otherRow)
            return 0

#results will make the final changes to the game board
def results(row, player, startRow, otherRow):
    #use global variables because we want to change things outside the function
    global row1
    global row2
    global player1
    global player2

    #first we check who made the move. We can tell by which row was entered.
    if row == 2:
        row2 = startRow
        row1 = otherRow
        player1 = player
    else:
        row2 = otherRow
        row2.reverse()
        row1 = startRow
        row1.reverse()
        player2 = player

#checkGame will make sure no one has an empty row. If someone has an empty row, the player with marbles in there row
#will gain all of them as points. This function will then return false if that is the case
def checkGame():
    #use global variables because we might need to change variables outside of this function
    global playing
    global player1
    global player2
    global row1
    global row2

    #use these variables to go through the rows
    count = 0
    index = 0

    while index < len(row1):
        count += row1[index]
        index += 1

    #If count was 0, than row1 was empty.
    if count == 0:
        playing = 0
        index = 0
        #Since count was 0, we need to count all the marbles in row2 and give them to player 1
        while index < len(row2):
            count += row2[index]
            index += 1
        player1 += count
        return 0
    #If count was not 0, we check if row2 was 0. If it was, we give all of row1 to player 2
    else:
        score = count
        count = 0
        playing = 1
        index = 0
        while index < len(row2):
            count += row2[index]
            index += 1
        if count == 0:
            playing = 0
            player2 += score
            return 0

#adamsMove will determine which of the choices will give the most points
def adamsMove():
    #we use global variables because we have to use play to determine the best moves. This will cause changes to the
    #game board, so we have to undo them.
    global adamPlayer #adamPlayer will tell us if Adam(the computer) is player 1 or 2
    global player1
    global player2
    global row1
    global row2

    choices = [0, 0, 0, 0, 0, 0] #This list will have the outcome of each choice
    index = 0

    #This loop will try each choice and save the results in choices. Then it will undo the changes
    while index < len(choices):
        player1History = player1
        player2History = player2
        row1History = row1.copy()
        row2History = row2.copy()

        repeat = play(index, adamPlayer) #We need to know if Adam will have an additional move.
        #If Adam has an additional move, we will use adamsMove again to determine the best way to use the additional
        #move
        if repeat:
            play(adamsMove(),adamPlayer)

        if adamPlayer == 2:
            choices[index] = player1
        else:
            choices[index] = player2
        #reset the board back to normal
        player1 = player1History
        player2 = player2History
        row1 = row1History
        row2 = row2History
        index += 1
    index = 0

    max = 0 #will be used to find the best move

    #This loop will go through choices and set max as the best move
    while index < len(choices):
        if choices[index] > max:
            max = choices[index]
        index += 1

    return choices.index(max) #return the index of the best move.

#ask the user if they want to play against Adam
isAdamPlaying = input("Do you want to play against Adam? Y/N : ")

if isAdamPlaying.lower() == "y":
    #Which player will Adam be?
    adamPlayer = int(input("Is Adam player one (first move) or player two? 1/2 :"))

    #play thinks of row 1 as player 2. So we switch 1 and 2 for Adam
    if adamPlayer == 1:
        adamPlayer = 2
    else:
        adamPlayer = 1

print(row1)
print(row2)
print("Player 1: " + str(player1))
print("Player 2: " + str(player2))

#This loop will run the game.
while playing:
    turn = 1
    while (turn & playing):
        if isAdamPlaying.lower() == "y":
            if adamPlayer == 2:
                move = adamsMove()
            else:
                move = int(input("Player 1, enter your column: "))
        else:
            move = int(input("Player 1, enter your column: "))
        turn = play(move,2)
        print(row1)
        print(row2)
        print("Player 1: " + str(player1))
        print("Player 2: " + str(player2))
        checkGame()

    turn = 1
    while (turn & playing) == 1:
        if isAdamPlaying.lower() == "y":
            if adamPlayer == 1:
                move = adamsMove()
            else:
                move = int(input("Player 2, enter your column: "))
        else:
            move = int(input("Player 2, enter your column: "))
        turn = play(move,1)
        print(row1)
        print(row2)
        print("Player 1: " + str(player1))
        print("Player 2: " + str(player2))
        checkGame()
print("The game is complete")
print("Player 1: " + str(player1))
print("player 2: " + str(player2))