sum = 0
  # Αρχικοποίηση του αθροιστή
for i in range(1000):  # Επανάληψη από το 0 έως το 999
    if i % 3 == 0 or i % 5 == 0:  # Ελέγχος αν ο αριθμός είναι πολλαπλάσιο του 3 ή του 5
        sum += i  # Προσθήκη του αριθμού στον αθροιστή

print(sum)  # Εκτύπωση του τελικού αθροίσματος