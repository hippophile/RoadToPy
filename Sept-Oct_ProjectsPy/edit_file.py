with open("random.txt", "r") as f:
    text = f.read()

print("\nThe file is saying:\n")
print(f'"{text}"')

# count the words in the file 
split_text = text.split()
words = len(split_text)

if words == 1:
    print(f"\nThere is {words} word in this text file\n")
else:
    print(f"\nThere are {words} words in this text file\n")

# count the lines in the file
split_lines = text.splitlines()
lines = len(split_lines)

if lines == 1:
    print(f"There is {lines} line in this text file\n")
else:
    print(f"There are {lines} lines in this text file\n")

# count the chars in th file
characters = len(text)

if characters == 1:
    print(f"There is {characters} character in this text file\n")
else:
    print(f"There are {characters} characters in this text file\n")

# count the words of each kind
word_to_find = input("For what word are you most curius about? : ").strip()

if not word_to_find:
    print("You stupid fuck.\n")
    quit()

    
word_to_find = word_to_find.lower()
words_in_text = text.lower().split()

count = words_in_text.count(word_to_find)

if count == 1:
    print(f"\nThe word: {word_to_find} was found {count} time\n")
else:
    print(f"\nThe word: {word_to_find} was found {count} times\n")

new_word = input(f"\nOkay now replace {word_to_find} with one of your choice : ")

new_text = text.replace(word_to_find,new_word ) 

print("\nYou just destoyed my text!!!\n") 
print(new_text)

choice = input("\nDo you wanna add something more to my text? (y/n)").lower()

while choice == 'y':
    additional_text = input("\nOkay what do you wanna add? : ").strip()
    new_text += "\n" + additional_text

    with open("random.txt", "w") as f:
        f.write(new_text)
    choice = input("\nDo you want to add more? (y/n): ").lower()

if choice == 'n':
    print("\nOh okay, goodbye :)\n")

print("\nYour changes have been saved!")