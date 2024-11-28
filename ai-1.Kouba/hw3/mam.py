import pandas as pd
from csp import CSP, backtracking_search, min_conflicts, mrv, forward_checking, mac

# ---------------------------1. Loading data--------------------------
filename = "h3-data.csv" 

df = pd.read_csv(filename)

difficult_courses = df[df['Δύσκολο (TRUE/FALSE)'] == True]['Μάθημα'].tolist()
semester_map = df.set_index('Μάθημα')['Εξάμηνο'].to_dict()
professor_map = df.set_index('Μάθημα')['Καθηγητής'].to_dict()
lab_courses = df[df['Εργαστήριο (TRUE/FALSE)'] == True]['Μάθημα'].tolist()

# ---------------------------2. variables------------------------------

# Ορισμός των μεταβλητών και των τομέων

variables = df['Μάθημα'].tolist()
# Δημιουργία ξεχωριστών μεταβλητών για θεωρία και εργαστήριο


days = list(range(1, 22))  # Ημέρες εξεταστικής (1-21)
periods = ['9-12', '12-3', '3-6']  # Χρονικές περίοδοι

domains = {var: [(day, period) for day in days for period in periods] for var in variables}

# Όλα τα μαθήματα είναι γείτονες, αφού πρέπει να αποφύγουμε τις επικαλύψεις
neighbors = {var: [n for n in variables if n != var] for var in variables}

# ---------------------------3. constraints------------------------------

def constraints(course1, time1, course2, time2):
    day1, period1 = time1
    day2, period2 = time2

    # Περιορισμός 1: Ίδια μέρα και ώρα δεν επιτρέπονται
    if time1 == time2:
        return False

    # Περιορισμός 2: Ίδιο εξάμηνο, ίδια μέρα
    if semester_map.get(course1) == semester_map.get(course2) and day1 == day2:
        return False

    # Περιορισμός 3: Ίδιος καθηγητής, ίδια μέρα
    if professor_map.get(course1) == professor_map.get(course2) and day1 == day2:
        return False
    
    # Περιορισμός 4: Δύσκολα μαθήματα να έχουν τουλάχιστον 2 ημέρες απόσταση
    if course1 in difficult_courses and course2 in difficult_courses and abs(day1 - day2) < 2:
        return False

    # Περιορισμός 5: Εάν είναι εργαστήριο, να εξετάζεται μόνο σε 9-12 ή 12-3
    if course1 in lab_courses and period1 == '3-6':
        return False
    
    # Περιορισμός: Αν το μάθημα είναι εργαστήριο, το επόμενο slot να είναι κενό
    if course1 in lab_courses:
        if day1 == day2 and periods.index(period2) == periods.index(period1) + 1:
            return False
                
    return True

# ---------------------------4. CSP------------------------------

problem = CSP(variables, domains,neighbors, constraints)

# ---------------------------5. In the making------------------------------

solution_fc = backtracking_search(problem, select_unassigned_variable=mrv, inference=forward_checking)

# ---------------------------6. FC------------------------------

#solution_fc = backtracking_search(problem, inference=forward_checking)
print("Δοκιμάζεται Forward Checking:")

if solution_fc:
    print("Η λύση ήταν επιτυχής! Αποθηκεύτηκε στο αρχείο 'fc_schedule.txt'.")

    # Μετατροπή της λύσης σε DataFrame
    schedule = pd.DataFrame(
        [{'Μέρα': day, 'Ώρα': time, 'Μάθημα': course} for course, (day, time) in solution_fc.items()]
    )

    # Ορισμός της σειράς ταξινόμησης για τις ώρες
    time_order = {'9-12': 0, '12-3': 1, '3-6': 2}
    schedule['Ώρα_Σειρά'] = schedule['Ώρα'].map(time_order)

    # Ταξινόμηση με βάση τη μέρα και τη σειρά ώρας
    schedule = schedule.sort_values(by=['Μέρα', 'Ώρα_Σειρά']).drop(columns=['Ώρα_Σειρά'])

    lines = []
    for day, group in schedule.groupby('Μέρα'):
        lines.append(f"Μέρα {day}:")  # Επικεφαλίδα για την ημέρα
        for _, row in group.iterrows():
            lines.append(f"    {row['Ώρα']}: {row['Μάθημα']}" +
                         (" (ΔΥΣΚΟΛΟ)" if row['Μάθημα'] in difficult_courses else "") +
                         (" \n         +ΕΡΓΑΣΤΗΡΙΟ " if row['Μάθημα'] in lab_courses else ""))



    # Αποθήκευση σε αρχείο .txt
    with open("fc_schedule.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
else:
    print("Δεν βρέθηκε λύση για το πρόβλημα.")


#print(lab_courses)

# ---------------------------7. Dom/wdeg--------------------------

# Βάρη για τις μεταβλητές (αρχικοποίηση)
weights = {var: 1 for var in variables}

# Υλοποίηση της στρατηγικής dom/wdeg
def dom_wdeg(assignment, csp):
    def weight(var):
        # Υπολογισμός του dom/wdeg για κάθε μεταβλητή
        dom_size = len(csp.curr_domains[var]) if csp.curr_domains else len(csp.domains[var])
        return dom_size / weights[var]

    # Επιλέγουμε τη μεταβλητή με το ελάχιστο dom/wdeg
    return min((v for v in csp.variables if v not in assignment), key=weight)

# Ενημέρωση βαρών στους περιορισμούς
def increment_weights(csp, var, assignment):
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            weights[neighbor] += 1

# ---------------------------8. MAC------------------------------

solution_mac = backtracking_search(problem, select_unassigned_variable=dom_wdeg, inference=mac)
#print("Λύση με MAC:", solution_mac)
if solution_mac:
    print("Η λύση ήταν επιτυχής! Αποθηκεύτηκε στο αρχείο 'mac_schedule.txt'.")

    # Μετατροπή της λύσης σε DataFrame
    schedule = pd.DataFrame(
        [{'Μέρα': day, 'Ώρα': time, 'Μάθημα': course} for course, (day, time) in solution_fc.items()]
    )

    # Ορισμός της σειράς ταξινόμησης για τις ώρες
    time_order = {'9-12': 0, '12-3': 1, '3-6': 2}
    schedule['Ώρα_Σειρά'] = schedule['Ώρα'].map(time_order)

    # Ταξινόμηση με βάση τη μέρα και τη σειρά ώρας
    schedule = schedule.sort_values(by=['Μέρα', 'Ώρα_Σειρά']).drop(columns=['Ώρα_Σειρά'])

    lines = []
    for day, group in schedule.groupby('Μέρα'):
        lines.append(f"Μέρα {day}:")  # Επικεφαλίδα για την ημέρα
        for _, row in group.iterrows():
            lines.append(f"    {row['Ώρα']}: {row['Μάθημα']}" +
                         (" (ΔΥΣΚΟΛΟ)" if row['Μάθημα'] in difficult_courses else "") +
                         (" \n         +ΕΡΓΑΣΤΗΡΙΟ " if row['Μάθημα'] in lab_courses else ""))



    # Αποθήκευση σε αρχείο .txt
    with open("mac_schedule.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
else:
    print("Δεν βρέθηκε λύση για το πρόβλημα.")

# ---------------------------9. Min_Conflicts------------------------------

solution_min_conflicts = min_conflicts(problem, max_steps=100000)

if solution_min_conflicts:
    print("Η λύση ήταν επιτυχής! Αποθηκεύτηκε στο αρχείο 'mc_schedule.txt'.")

    # Μετατροπή της λύσης σε DataFrame
    schedule = pd.DataFrame(
        [{'Μέρα': day, 'Ώρα': time, 'Μάθημα': course} for course, (day, time) in solution_fc.items()]
    )

    # Ορισμός της σειράς ταξινόμησης για τις ώρες
    time_order = {'9-12': 0, '12-3': 1, '3-6': 2}
    schedule['Ώρα_Σειρά'] = schedule['Ώρα'].map(time_order)

    # Ταξινόμηση με βάση τη μέρα και τη σειρά ώρας
    schedule = schedule.sort_values(by=['Μέρα', 'Ώρα_Σειρά']).drop(columns=['Ώρα_Σειρά'])

    lines = []
    for day, group in schedule.groupby('Μέρα'):
        lines.append(f"Μέρα {day}:")  # Επικεφαλίδα για την ημέρα
        for _, row in group.iterrows():
            lines.append(f"    {row['Ώρα']}: {row['Μάθημα']}" +
                         (" (ΔΥΣΚΟΛΟ)" if row['Μάθημα'] in difficult_courses else "") +
                         (" \n         +ΕΡΓΑΣΤΗΡΙΟ " if row['Μάθημα'] in lab_courses else ""))



    # Αποθήκευση σε αρχείο .txt
    with open("mc_schedule.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
else:
    print("Δεν βρέθηκε λύση για το πρόβλημα.")