import random

while True:
    print("\n---Guess The Integer Game---")
    print("\n1. easy (1-50).")
    print("2. normal (1-100).")
    print("3. hard (1-1000).")
    print("4. Exit")

    # Επιλογή δυσκολίας από τον χρήστη
    dif = input("\nChoose a difficulty (numbers only): ")

    msg = "\nWhat number am I thinking of?   "
    bmsg = "Your number was bigger than mine."
    smsg = "Your number was smaller than mine."
    endmsg = "Thank you for playing! Bye!"

    if dif not in ["1", "2", "3", "4"]:
        print("Please choose a valid option.\n")
        continue

    # Ορισμός τυχαίου αριθμού ανάλογα με την επιλογή δυσκολίας
    if dif == "1":
        random_number = random.randint(1, 50)
    elif dif == "2":
        random_number = random.randint(1, 100)
    elif dif == "3":
        random_number = random.randint(1, 1000)
    elif dif == "4":
        print("You exited the game successfully.\n")
        break

    attempts = 0

    # Εσωτερικός βρόχος για το μάντεμα του αριθμού
    while True:
        user_guess = input(msg)

        if not user_guess.isdigit():
            print("Please enter a valid number: ")
            continue

        user_guess = int(user_guess)
        attempts += 1

        if user_guess > random_number:
            print(bmsg)
        elif user_guess < random_number:
            print(smsg)
        else:
            print(f"Congratulations! You guessed the number in {attempts} tries.")
            break 

    play_again = input("\nDo you want to play again? (y/n): ")
    if play_again.lower() != "y":
        print(endmsg)
        break  
