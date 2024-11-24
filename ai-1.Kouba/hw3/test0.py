import pandas as pd
import time
from csp import CSP, backtracking_search, min_conflicts, forward_checking, mac, mrv, lcv

# --------------------------- 1. Φόρτωση δεδομένων ---------------------------
df = pd.read_csv("h3-data.csv")

# --------------------------- 2. Ορισμός μεταβλητών και πεδίων ---------------------------
variables = []
for _, row in df.iterrows():
    variables.append(row["Μάθημα"])  # Θεωρία
    if row["Εργαστήριο (TRUE/FALSE)"] == True:  # Ελέγχουμε αν υπάρχει εργαστήριο
        variables.append(f"{row['Μάθημα']} (Εργαστήριο)")  # Προσθέτουμε το εργαστήριο

# Περιοχές τιμών (μέρες και χρονικές περίοδοι)
domains = {
    var: [(day, period) for day in range(1, 22) for period in ["9-12", "12-3", "3-6"]]
    for var in variables
}


# Γείτονες (όλα τα άλλα μαθήματα είναι γείτονες, εξαιρώντας περιττές συγκρίσεις)
neighbors = {
    var: [
        other for other in variables
        if other != var and not (var.endswith("(Εργαστήριο)") and other.endswith("(Εργαστήριο)"))
    ]
    for var in variables
}

# --------------------------- 3. Ανάγνωση περιορισμών ---------------------------
semester_map = {row["Μάθημα"]: row["Εξάμηνο"] for _, row in df.iterrows()}
professor_map = {row["Μάθημα"]: row["Καθηγητής"] for _, row in df.iterrows()}
difficult_courses = [
    row["Μάθημα"]
    for _, row in df.iterrows()
    if row["Δύσκολο (TRUE/FALSE)"] == True
]

# --------------------------- 4. Περιορισμοί ---------------------------
def constraints(var1, time1, var2, time2):
    day1, period1 = time1
    day2, period2 = time2

    # Debugging: Καταγραφή περιορισμών
    #print(f"Checking constraints between {var1} at {time1} and {var2} at {time2}")

    # 1. Τα μαθήματα δεν μπορούν να εξετάζονται την ίδια ώρα
    if time1 == time2:
        return False

    # 2. Μαθήματα του ίδιου εξαμήνου πρέπει να εξετάζονται σε διαφορετικές μέρες
    if semester_map.get(var1) == semester_map.get(var2) and day1 == day2:
        return False

    # 3. Δύσκολα μαθήματα πρέπει να απέχουν τουλάχιστον 2 μέρες
    if var1 in difficult_courses and var2 in difficult_courses:
        if abs(day1 - day2) < 2:
            return False

    # 4. Μαθήματα του ίδιου καθηγητή πρέπει να εξετάζονται σε διαφορετικές μέρες
    if professor_map.get(var1) == professor_map.get(var2) and day1 == day2:
        return False

    # 5. Τα εργαστήρια πρέπει να ακολουθούν τη θεωρία την ίδια μέρα
    if var1.endswith("(Εργαστήριο)") and var2 == var1.replace(" (Εργαστήριο)", ""):
        if day1 != day2 or not (
            (period1 == "12-3" and period2 == "9-12") or (period1 == "3-6" and period2 == "12-3")
        ):
            return False

    return True

# --------------------------- 5. Δημιουργία CSP ---------------------------
exam_csp = CSP(variables, domains, neighbors, constraints)

# Αρχικοποίηση των curr_domains
exam_csp.curr_domains = {var: list(exam_csp.domains[var]) for var in exam_csp.variables}

# --------------------------- 6. Αποθήκευση Προγράμματος ---------------------------
def save_schedule_to_file(filename, solution):
    if solution is None:
        with open(filename, "w") as f:
            f.write("No solution found.\n")
        return

    schedule = {}
    for course, (day, period) in solution.items():
        if day not in schedule:
            schedule[day] = []
        schedule[day].append((period, course))

    with open(filename, "w") as f:
        for day, exams in sorted(schedule.items()):
            f.write(f"Day {day}:\n")
            for period, course in sorted(exams, key=lambda x: ["9-12", "12-3", "3-6"].index(x[0])):
                f.write(f"  {period}: {course}\n")
            f.write("\n")

# --------------------------- 7. Εκτέλεση Αλγορίθμων ---------------------------

def measure_execution_time(func, *args, **kwargs):
    """
    Μετρά τον χρόνο εκτέλεσης μιας συνάρτησης.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Η συνάρτηση '{func.__name__}' χρειάστηκε {execution_time:.6f} δευτερόλεπτα.")
    return result, execution_time

# Min Conflicts για αρχική λύση
print("Running Min Conflicts...")
solution_mc, time_mc = measure_execution_time(min_conflicts, exam_csp, max_steps=1000)


if solution_mc:
    print("Initial solution found using Min Conflicts.")
    save_schedule_to_file("min_conflicts_schedule.txt", solution_mc)

# Refining solution using Forward Checking
print("Refining with Forward Checking...")
# Συνδυασμός MRV και LCV
#solution_fc, time_fc = measure_execution_time(
 #   backtracking_search, exam_csp, select_unassigned_variable=mrv, order_domain_values=lcv, inference=forward_checking
#)

solution_fc = backtracking_search(
    exam_csp,
    select_unassigned_variable=mrv,
    inference=forward_checking,
    max_depth=1000  # Προσθέτεις μέγιστο όριο.
)

save_schedule_to_file("fc_schedule.txt", solution_fc)

# Maintaining Arc Consistency
print("Refining with MAC...")
solution_mac, time_mac = measure_execution_time(
    backtracking_search, exam_csp, select_unassigned_variable=mrv, inference=mac
)
save_schedule_to_file("mac_schedule.txt", solution_mac)

# --------------------------- 8. Εκτύπωση Χρόνου ---------------------------
print(f"Χρόνος εκτέλεσης Min Conflicts: {time_mc:.6f} δευτερόλεπτα")
#print(f"Χρόνος εκτέλεσης Forward Checking: {time_fc:.6f} δευτερόλεπτα")
print(f"Χρόνος εκτέλεσης MAC: {time_mac:.6f} δευτερόλεπτα")
