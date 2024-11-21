from csp import CSP, backtracking_search
import pandas as pd
import random

# --------------------------- 1. Φόρτωση δεδομένων ---------------------------
df = pd.read_csv("h3-data.csv")

# --------------------------- 2. Ορισμός μεταβλητών και πεδίων ---------------------------
variables = df["Μάθημα"].tolist()

domains = {
    course: [(day, slot) for day in range(1, 22) for slot in ["9-12", "12-3", "3-6"]]
    for course in variables
}

neighbors = {course: [other_course for other_course in variables if other_course != course] for course in variables}

semester_map = {row["Μάθημα"]: row["Εξάμηνο"] for _, row in df.iterrows()}
difficult_courses = df[df["Δύσκολο (TRUE/FALSE)"] == True]["Μάθημα"].tolist()
lab_map = {row["Μάθημα"]: row["Εργαστήριο (TRUE/FALSE)"] for _, row in df.iterrows()}

# --------------------------- 3. Χαρτογράφηση Βαρών ---------------------------
weights = {}  # Τοπική αποθήκευση των βαρών

def increase_weight(var1, var2):
    """Αυξάνει το βάρος του περιορισμού μεταξύ var1 και var2."""
    if (var1, var2) not in weights:
        weights[(var1, var2)] = 1
    else:
        weights[(var1, var2)] += 1

    # Διατηρεί συμμετρικά τα βάρη
    if (var2, var1) not in weights:
        weights[(var2, var1)] = 1
    else:
        weights[(var2, var1)] += 1

# --------------------------- 4. Περιορισμοί ---------------------------
def constraints(course1, time1, course2, time2):
    if time1 == time2:
        increase_weight(course1, course2)
        return False
    if semester_map[course1] == semester_map[course2] and time1[0] == time2[0]:
        increase_weight(course1, course2)
        return False
    if course1 in difficult_courses and course2 in difficult_courses:
        if abs(time1[0] - time2[0]) <= 1:
            increase_weight(course1, course2)
            return False
    if course1 == course2 and lab_map.get(course1, False):
        if time1[1] == "12-3" and time2 != (time1[0], "3-6"):
            increase_weight(course1, course2)
            return False
    return True

# --------------------------- 5. Τοπική μέθοδος `is_solution` ---------------------------
def is_solution(csp, assignment):
    """Ελέγχει αν ένα assignment είναι λύση του CSP."""
    if len(assignment) != len(csp.variables):
        return False
    for var1 in assignment:
        for var2 in csp.neighbors[var1]:
            if var2 in assignment:
                if not csp.constraints(var1, assignment[var1], var2, assignment[var2]):
                    return False
    return True

# --------------------------- 6. Ευρετικές ---------------------------
def mrv(assignment, csp):
    return min(
        (var for var in csp.variables if var not in assignment),
        key=lambda var: len(csp.domains[var])
    )

def dom_wdeg(assignment, csp):
    def weight(var):
        return len(csp.domains[var]) / sum(weights.get((var, neighbor), 1) for neighbor in csp.neighbors[var])
    return min(
        (var for var in csp.variables if var not in assignment),
        key=weight
    )

# --------------------------- 7. Forward Checking (FC) ---------------------------
def forward_checking(csp, var, value, assignment, removals):
    """Υλοποίηση Forward Checking."""
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            for neighbor_value in csp.domains[neighbor][:]:
                if not csp.constraints(var, value, neighbor, neighbor_value):
                    csp.domains[neighbor].remove(neighbor_value)
                    if removals is not None:
                        removals.append((neighbor, neighbor_value))
            if not csp.domains[neighbor]:
                return False
    return True

# --------------------------- 8. Min-Conflicts ---------------------------
def min_conflicts(csp, max_steps=1000):
    current = {var: random.choice(csp.domains[var]) for var in csp.variables}
    for _ in range(max_steps):
        if is_solution(csp, current):
            return current
        var = random.choice([var for var in csp.variables if any(
            not csp.constraints(var, current[var], neighbor, current[neighbor])
            for neighbor in csp.neighbors[var] if neighbor in current)])
        current[var] = min(csp.domains[var], key=lambda val: sum(
            not csp.constraints(var, val, neighbor, current[neighbor])
            for neighbor in csp.neighbors[var] if neighbor in current))
    return None

# --------------------------- 9. Επίλυση και Εξαγωγή ---------------------------
def solve_and_export(csp, method, filename):
    if method == "fc":
        solution = backtracking_search(csp, inference=forward_checking, select_unassigned_variable=mrv)
    elif method == "mac":
        solution = backtracking_search(csp, inference=forward_checking, select_unassigned_variable=dom_wdeg)
    elif method == "min_conflicts":
        solution = min_conflicts(csp)
    else:
        raise ValueError("Άγνωστη μέθοδος!")

    if solution:
        grouped_schedule = {}
        for course, time in solution.items():
            day, slot = time
            grouped_schedule.setdefault(day, {}).setdefault(slot, []).append(course)

        export_data = []
        for day in sorted(grouped_schedule.keys()):
            for slot in ["9-12", "12-3", "3-6"]:
                if slot in grouped_schedule[day]:
                    courses = ", ".join(grouped_schedule[day][slot])
                    export_data.append({"Ημέρα": f"Μέρα {day}", "Χρονική Περίοδος": slot, "Μαθήματα": courses})
                else:
                    export_data.append({"Ημέρα": f"Μέρα {day}", "Χρονική Περίοδος": slot, "Μαθήματα": "-"})

        schedule_df = pd.DataFrame(export_data)
        schedule_df.to_csv(filename, index=False)
        print(f"Λύση βρέθηκε για {method.upper()} και αποθηκεύτηκε στο {filename}.")
    else:
        print(f"Δεν βρέθηκε λύση για {method.upper()}.")

# --------------------------- Εκτέλεση ---------------------------
exam_csp = CSP(variables, domains, neighbors, constraints)
import time

# Χρονόμετρο για FC
start_time = time.time()
solve_and_export(exam_csp, method="fc", filename="fc_schedule.csv")
fc_time = time.time() - start_time
print(f"Χρόνος εκτέλεσης για FC: {fc_time:.2f} δευτερόλεπτα.")

# Χρονόμετρο για MAC
start_time = time.time()
solve_and_export(exam_csp, method="mac", filename="mac_schedule.csv")
mac_time = time.time() - start_time
print(f"Χρόνος εκτέλεσης για MAC: {mac_time:.2f} δευτερόλεπτα.")

# Χρονόμετρο για Min-Conflicts
start_time = time.time()
solve_and_export(exam_csp, method="min_conflicts", filename="minconflicts_schedule.csv")
minconflicts_time = time.time() - start_time
print(f"Χρόνος εκτέλεσης για Min-Conflicts: {minconflicts_time:.2f} δευτερόλεπτα.")

