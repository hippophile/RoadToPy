import subprocess

# Διαδρομή προς το εκτελέσιμο αρχείο του Brave Browser στα Windows
brave_path = r"C:\\Users\\pasch\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# URLs που θέλουμε να ανοίξουμε
urls = [
    "https://chat.openai.com/chat",
    "https://webmail.noc.uoa.gr/src/login.php",
    "https://piazza.com/class/lta3e11psq7ma/post/114",
    "https://sso.uoa.gr/login?service=https%3A%2F%2Feclass.uoa.gr%2Fmodules%2Fauth%2Fcas.php%3Fnext%3D%252Fmodules%252Fauth%252Fcourses.php%253Ffc%253D388"
]

# Εκτέλεση του Brave Browser με όλα τα URLs ταυτόχρονα σε καρτέλες
subprocess.run(["cmd.exe", "/c", brave_path] + urls)
