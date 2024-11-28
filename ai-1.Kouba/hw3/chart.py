import matplotlib.pyplot as plt

# Δεδομένα
algorithms = ["Forward Checking", "MAC", "Min-Conflicts"]
execution_times = [0.0384, 0.0103, 0.0609]
constraints_checked = [35819, 3515, 60643]

# Γράφημα για τον χρόνο εκτέλεσης
plt.figure(figsize=(8, 5))
plt.bar(algorithms, execution_times)
plt.title("Χρόνος Εκτέλεσης (s) ανά Αλγόριθμο")
plt.ylabel("Χρόνος Εκτέλεσης (s)")
plt.show()

# Γράφημα για τους ελέγχους περιορισμών
plt.figure(figsize=(8, 5))
plt.bar(algorithms, constraints_checked, color='orange')
plt.title("Έλεγχοι Περιορισμών ανά Αλγόριθμο")
plt.ylabel("Αριθμός Ελέγχων Περιορισμών")
plt.show()
