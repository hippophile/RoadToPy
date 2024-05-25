import random

title = "Rock, Paper, Scissors"
title02 = "\nLet's Play Rock, Paper, Scissors"

player = 0
computer = 0
games_played = 0

def game():
    global player, computer, games_played
    
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    
    while True:  # Βρόχος επανάληψης για έγκυρη είσοδο
        player_choice = input("\nChoose rock, paper or scissors: ").lower()  # Μετατρέπουμε σε πεζά για συνέπεια
        if player_choice in choices:
            break
        else:
            print("Invalid input. Please choose only 'rock', 'paper', or 'scissors'.")
    
    print(f"\nComputer chose: {computer_choice}")
    print(f"Player chose: {player_choice}\n")
    
    games_played += 1
    
    if player_choice == computer_choice:
        player += 1
        computer += 1
        result = "It's a tie!"
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        player += 1
        result = "Player wins!"
    else:
        computer += 1
        result = "Computer wins!"
    
    print(result, "\nThe score is: Player", player, "Computer", computer)
    

print(title02)

turns = int(input("How many turns should the game end? "))

while games_played < turns:
    print(game())
