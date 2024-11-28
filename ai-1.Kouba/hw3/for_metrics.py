import pandas as pd
import time
from csp import CSP, backtracking_search, min_conflicts, mrv, forward_checking, mac

# ---------------------------1. Loading data--------------------------
filename = "h3-data.csv"

df = pd.read_csv(filename)

difficult_courses = df[df['Δύσκολο (TRUE/FALSE)'] == True]['Μάθημα'].tolist()
semester_map = df.set_index('Μάθημα')['Εξάμηνο'].to_dict()
professor_map = df.set_index('Μάθημα')['Καθηγητής'].to_dict()
lab_courses = df[df['Εργαστήριο (TRUE/FALSE)'] == True]['Μάθημα'].tolist()

# ---------------------------2. Variables------------------------------
variables = df['Μάθημα'].tolist()
days = list(range(1, 31))  # Ημέρες εξεταστικής (1-100)
periods = ['9-12', '12-3', '3-6']  # Χρονικές περίοδοι
domains = {var: [(day, period) for day in days for period in periods] for var in variables}
neighbors = {var: [n for n in variables if n != var] for var in variables}

# ---------------------------3. Constraints------------------------------
def constraints(course1, time1, course2, time2):

    problem.constraint_checks += 1  # Καταγραφή ελέγχου περιορισμού
    day1, period1 = time1
    day2, period2 = time2

    if time1 == time2:
        return False
    if semester_map.get(course1) == semester_map.get(course2) and day1 == day2:
        return False
    if professor_map.get(course1) == professor_map.get(course2) and day1 == day2:
        return False
    if course1 in difficult_courses and course2 in difficult_courses and abs(day1 - day2) < 2:
        return False
    if course1 in lab_courses and period1 == '3-6':
        return False
    if course1 in lab_courses:
        if day1 == day2 and periods.index(period2) == periods.index(period1) + 1:
            return False
    return True

# ---------------------------4. CSP Setup------------------------------
problem = CSP(variables, domains, neighbors, constraints)
problem.node_expansions = 0  # Αριθμός επεκτάσεων κόμβων
problem.constraint_checks = 0  # Αριθμός ελέγχων περιορισμών

# ---------------------------5. Run and Record Metrics------------------------------
results = []

# Forward Checking
problem.node_expansions = 0
problem.constraint_checks = 0
start_time = time.time()
solution_fc = backtracking_search(
    problem, 
    select_unassigned_variable=mrv, 
    inference=forward_checking
)
end_time = time.time()

results.append({
    "Algorithm": "Forward Checking",
    "Execution Time (s)": end_time - start_time,
    "Nodes Expanded": problem.node_expansions,
    "Constraints Checked": problem.constraint_checks
})

# MAC
problem.node_expansions = 0
problem.constraint_checks = 0
start_time = time.time()
solution_mac = backtracking_search(
    problem, 
    select_unassigned_variable=mrv, 
    inference=mac
)
end_time = time.time()

results.append({
    "Algorithm": "MAC",
    "Execution Time (s)": end_time - start_time,
    "Nodes Expanded": problem.node_expansions,
    "Constraints Checked": problem.constraint_checks
})

# Min-Conflicts
problem.node_expansions = 0
problem.constraint_checks = 0
start_time = time.time()
solution_min_conflicts = min_conflicts(
    problem, 
    max_steps=100000
)
end_time = time.time()

results.append({
    "Algorithm": "Min-Conflicts",
    "Execution Time (s)": end_time - start_time,
    "Nodes Expanded": problem.node_expansions,
    "Constraints Checked": problem.constraint_checks
})

# ---------------------------6. Display Results------------------------------
results_df = pd.DataFrame(results)
print(results_df)

# Αποθήκευση σε αρχείο
results_df.to_csv("csp_metrics_results.csv", index=False)
