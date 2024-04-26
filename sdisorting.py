def check_string_in_list(input_string, strings):
    return input_string in strings

# Ζητάμε από τον χρήστη να δώσει όλα τα strings μαζί
print("Δώσε όλα τα strings μαζί:")
input_strings = input()

# Εδώ θα πρέπει να δώσεις το string που θέλεις να ελεγχθεί
search_string = "sdi2300284"

# Καλούμε τη συνάρτηση check_string_in_list με το string που θέλουμε να ελεγχθεί και τη λίστα των strings
if check_string_in_list(search_string, input_strings):
    print(f"Το string {search_string} υπάρχει στη λίστα.")
else:
    print(f"Το string {search_string} δεν υπάρχει στη λίστα.")
