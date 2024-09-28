shop_list = []

# Αποθήκευση της λίστας σε αρχείο κειμένου
def save_list_to_file(filename, list):
    with open(filename, 'w') as file:
        for item in list:
            file.write(f"{item}\n")

def print_list(list):
    if len(list) == 0:
        print("Sorry, your list is empty.")
    else:
        print("\nYour Shopping List:\n")
        for i, item in enumerate(list):
            print(f"{i}: {item}")
        print("\n")

while True:
    print("---Your Shopping List Menu---")
    print("1. Add something to your list.")
    print("2. Remove something from your list.")
    print("3. Print your list.")
    print("4. Exit.")
    print("5. Exit and Save to a New File.")

    msg = "Choose an option by its number:  "

    option = input(msg)

    if option not in ["1", "2", "3", "4", "5"]:
        print("Please choose a valid option.\n")
        continue

    if option == "5":
        new_filename = input("Enter the filename for saving the list (e.g., my_list.txt): ")
        if not new_filename.endswith(".txt"):
            new_filename += ".txt"  # Προσθήκη της κατάληξης .txt αν δεν υπάρχει
        save_list_to_file(new_filename, shop_list)  # Αποθήκευση της λίστας σε νέο αρχείο
        print(f"The list was saved successfully in the file: {new_filename}")
        break

    if option == "4":
        print("You exited your list successfully.\n")
        break

    if option == "3":
        print_list(shop_list)

    elif option == "2":
        if len(shop_list) == 0:
            print("Your list is empty. Nothing to remove.\n")
            continue

        for i in range(len(shop_list)):
            print(f"{i}: {shop_list[i]}")

        removal = input("What do you want to remove (numbers only): ")

        # Έλεγχος αν το input είναι αριθμός και αν είναι έγκυρος δείκτης
        if removal.isdigit() and 0 <= int(removal) < len(shop_list):
            removal = int(removal)  # Μετατροπή σε ακέραιο αφού έχουμε ελέγξει

            sure = input(f"Do you want to remove '{shop_list[removal]}'? (y/n): ")

            if sure.lower() == 'y':
                print(f"'{shop_list[removal]}' was removed successfully.\n")
                shop_list.pop(removal)
            else:
                print("No item was removed.\n")
        else:
            print("Invalid number. Please enter a valid index.\n")

    elif option == "1":
        addition = input("Write your addition: ")
        shop_list.append(addition)
        print(f"\n'{addition}' was added to your list.\n")