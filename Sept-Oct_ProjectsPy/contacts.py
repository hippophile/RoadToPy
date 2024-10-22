contacts = {}

def save_contacts_to_file(filename, contacts):
    with open(filename, 'w') as file:
        for name, phone in contacts.items():
            file.write(f"{name}: {phone}\n")

def print_list(contacts):
    if len(contacts) == 0:
        print("\n\n---Sorry, your Contacts Dictionary is empty---\n\n")
    else:
        print("\nYour Contacts Dictionaries:\n")
        for i, item in enumerate(contacts):
            print(f"{i}: {item} - {contacts[item]}")
        print("\n")

while True:
    print("---Your Contacts Dictionary Menu---")
    print("1. Add something to your contacts.")
    print("2. Remove something from your contacts.")
    print("3. Print your contacts.")
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
        save_contacts_to_file(new_filename, contacts)  # Αποθήκευση της λίστας σε νέο αρχείο
        print(f"The list was saved successfully in the file: {new_filename}")
        break

    if option == "4":
        print("You exited your Contacts Dictionary successfully.\n")
        break

    if option == "3":
        print_list(contacts)