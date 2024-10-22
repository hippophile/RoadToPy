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
    print("1. Add a contact.")
    print("2. Remove a contact.")
    print("3. Print your contacts.")
    print("4. Exit.")
    print("5. Exit and Save to a New File.")

    contacts = dict(sorted(contacts.items()))

    msg = "Choose an option by its number:  "

    option = input(msg)

    if option not in ["1", "2", "3", "4", "5"]:
        print("Invalid option. Please choose a valid option from 1 to 5.")
        continue

    if option == "5":
        new_filename = input("Enter the filename for saving the list (e.g., my_list.txt): ")
        if not new_filename.endswith(".txt"):
            new_filename += ".txt"
        save_contacts_to_file(new_filename, contacts)
        print(f"Your contacts have been saved successfully in '{new_filename}'. You can find your file in the current working directory.")
        break

    if option == "4":
        print("You have successfully exited your Contacts Dictionary. Have a nice day!")
        break

    if option == "3":
        print_list(contacts)

    elif option == "2":
        if len(contacts) == 0:
            print("Your contacts are empty. Nothing to remove.\n")
            continue

        # Δημιουργία λίστας από τα ζεύγη (κλειδί, τιμή) του λεξικού
        contact_list = list(contacts.items())

        for i, (name, phone) in enumerate(contact_list):
            print(f"{i}: {name} - {phone}")

        removal = input("What do you want to remove (numbers only): ")

        if removal.isdigit():
            removal = int(removal)
            if 0 <= removal < len(contacts):
                name_to_remove = contact_list[removal][0]

                sure = input(f"Do you want to remove '{name_to_remove}'? (y/n): ")

                if sure.lower() == 'y':
                    contacts.pop(name_to_remove)
                    print(f"'{name_to_remove}' was removed successfully.\n")
                else:
                    print("No contact was removed.\n")
            else:
                print(f"Invalid input. Please enter a number between 0 and {len(contacts)-1}.")
        else:
            print("Please enter a valid number.")

    elif option == "1":
        name = input("Enter the contact's name: ").strip()
        if not name:
            print("Contact name cannot be empty. Please try again.")
            continue

        if name in contacts:
            print(f"The contact '{name}' already exists in your contacts. If you want to update the phone number, please remove the contact first and add it again.")
            continue

        phone = input("Enter the contact's phone number: ").strip()
        if not phone:
            print("Phone number cannot be empty. Please try again.")
            continue

        contacts[name] = phone
        print(f"Added {name} with phone number {phone} to contacts.\n")
