import re
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox
import random
import string

def check_strength(password):
    errors = {
        "Too short": len(password) < 8,
        "Missing lowercase": not re.search(r"[a-z]", password),
        "Missing uppercase": not re.search(r"[A-Z]", password),
        "Missing number": not re.search(r"\d", password),
        "Missing special char": not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    }

    passed = all(not value for value in errors.values())
    return passed, errors

def check_pwned(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1pwd[:5]
    suffix = sha1pwd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("Error fetching from API")

    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()?"
    password = ''.join(random.choice(characters) for _ in range(length))
    entry.delete(0, tk.END)
    entry.insert(0, password)

def on_check():
    password = entry.get()

    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    strong, errors = check_strength(password)
    result = ""

    if strong:
        result += "✅ Password strength: STRONG\n"
    else:
        result += "❌ Password is WEAK. Issues:\n"
        for issue, found in errors.items():
            if found:
                result += f" - {issue}\n"

    try:
        count = check_pwned(password)
        if count:
            result += f"\n⚠️ Found in {count} breaches!"
        else:
            result += "\n✅ No breach found."
    except Exception as e:
        result += f"\nError checking breach: {e}"

    output_label.config(text=result)

def toggle_password():
    global show_password
    show_password = not show_password
    if show_password:
        entry.config(show='')
        eye_button.config(text="🙈 Hide")
    else:
        entry.config(show='*')
        eye_button.config(text="👁 Show")

def copy_to_clipboard():
    password = entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No Password", "Nothing to copy.")

# ----- GUI Setup -----
root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("500x400")
root.resizable(False, False)

show_password = False

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)

entry_frame = tk.Frame(root)
entry_frame.pack()

entry = tk.Entry(entry_frame, show='*', font=("Arial", 14), width=30)
entry.pack(side=tk.LEFT)

eye_button = tk.Button(entry_frame, text="👁 Show", command=toggle_password, font=("Arial", 10))
eye_button.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Check Password", command=on_check, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Generate Password", command=generate_password, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Copy Password", command=copy_to_clipboard, bg="#9C27B0", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)

output_label = tk.Label(root, text="", font=("Arial", 11), justify="left", wraplength=460)
output_label.pack(pady=15)

root.mainloop()
