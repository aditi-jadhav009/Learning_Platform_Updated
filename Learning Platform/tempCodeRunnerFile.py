import tkinter as tk
from tkinter import Label, Radiobutton, Button, messagebox, Entry
import os
import random
from PIL import Image, ImageDraw, ImageFont

# Paths
base_dir = r"C:\D\PYTHON\Learning_Platform_Updated\Learning Platform\certificate"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

questions_file = os.path.join(os.path.dirname(__file__), "questions.txt")

# Load Questions
questions = []
answers = {}
if os.path.exists(questions_file):
    with open(questions_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 5):
            question = lines[i].strip()
            options = [lines[i + 1].strip(), lines[i + 2].strip(), lines[i + 3].strip()]
            correct = lines[i + 4].strip()
            questions.append((question, options, correct))
else:
    messagebox.showerror("Error", "questions.txt file not found!")
    exit()

# Shuffle and select 10 questions
random.shuffle(questions)
selected_questions = questions[:10]

# Variables
score = 0
question_index = 0
user_name = ""

# GUI Setup
root = tk.Tk()
root.title("Python Certification Quiz")
root.attributes('-fullscreen', True)  # Full-screen mode
root.configure(bg="#e3f2fd")

# Certificate Generation
def generate_certificate(name):
    cert_path = os.path.join(base_dir, f"{name}_certificate.png")

    img = Image.new('RGB', (900, 600), "#ffffff")
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("arial.ttf", 50)
    font_subtitle = ImageFont.truetype("arial.ttf", 30)
    font_text = ImageFont.truetype("arial.ttf", 25)

    draw.rectangle([(40, 40), (860, 560)], outline="black", width=8)
    draw.rectangle([(50, 50), (850, 550)], outline="blue", width=5)

    draw.text((270, 80), "Certificate of Achievement", font=font_title, fill="black")
    draw.text((150, 200), f"This is to certify that {name}", font=font_subtitle, fill="black")
    draw.text((150, 260), "has successfully completed the Python Quiz.", font=font_subtitle, fill="black")
    draw.text((150, 320), f"Score: {score}/10", font=font_subtitle, fill="black")
    draw.text((150, 450), "Issued by: Python Learning Platform", font=font_text, fill="black")

    img.save(cert_path)
    messagebox.showinfo("Certificate Generated", f"Certificate saved at:\n{cert_path}")

# Start Quiz (After Entering Name)
def start_quiz():
    global user_name
    user_name = name_entry.get().strip()
    if not user_name:
        messagebox.showerror("Error", "Please enter your name before starting the quiz.")
        return

    clear_window()
    show_quiz()

# Clear Window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Quiz UI
def show_quiz():
    global question_label, progress_label, option_buttons, var

    var = tk.StringVar(root)
    var.set(None)

    Label(root, text=f"Welcome, {user_name}!", font=("Arial", 20, "bold"), bg="#e3f2fd").pack(pady=20)

    question_label = Label(root, font=("Arial", 18, "bold"), bg="#ffffff", fg="#333", wraplength=600, padx=20, pady=10, relief="solid", borderwidth=2)
    question_label.pack(pady=15)

    progress_label = Label(root, text="Progress: 0/10", font=("Arial", 14), bg="#e3f2fd", fg="#000")
    progress_label.pack()

    option_buttons = []
    for _ in range(3):
        rb = Radiobutton(root, variable=var, font=("Arial", 14), bg="#e3f2fd", fg="#00008b", selectcolor="#ffdab9")
        rb.pack(anchor="w", padx=15, pady=5)
        option_buttons.append(rb)

    Button(root, text="Next", width=12, font=("Arial", 14), bg="#32cd32", fg="white", command=next_question).pack(pady=15)
    load_question(0)

# Load Question
def load_question(index):
    question, options, correct = selected_questions[index]
    question_label.config(text=f"Q{index + 1}: {question}")
    progress_label.config(text=f"Progress: {index + 1}/10")
    var.set(None)
    for i in range(3):
        option_buttons[i].config(text=options[i], value=options[i])
    answers[index] = correct

# Next Question
def next_question():
    global question_index, score
    if var.get() == answers[question_index]:
        score += 1
    if question_index < 9:
        question_index += 1
        load_question(question_index)
    else:
        end_test()

# End Test
def end_test():
    generate_certificate(user_name)
    show_main_menu()

# Home Screen
def show_main_menu():
    clear_window()

    Label(root, text="Python Certification Quiz", font=("Arial", 28, "bold"), bg="#e3f2fd").pack(pady=40)

    Button(root, text="Start Certification Quiz", width=25, font=("Arial", 16), bg="#1e88e5", fg="white", command=enter_name_screen).pack(pady=20)
    Button(root, text="Download Quiz Certificate", width=25, font=("Arial", 16), bg="#43a047", fg="white", command=download_certificate).pack(pady=10)
    Button(root, text="Exit", width=15, font=("Arial", 14), bg="red", fg="white", command=root.destroy).pack(pady=20)

# Name Entry Screen
def enter_name_screen():
    clear_window()

    Label(root, text="Enter Your Name:", font=("Arial", 20), bg="#e3f2fd").pack(pady=20)
    global name_entry
    name_entry = Entry(root, font=("Arial", 18))
    name_entry.pack(pady=10)

    Button(root, text="Start Quiz", width=15, font=("Arial", 16), bg="#1e88e5", fg="white", command=start_quiz).pack(pady=20)

# Download Certificate
def download_certificate():
    cert_path = os.path.join(base_dir, f"{user_name}_certificate.png")
    if os.path.exists(cert_path):
        os.system(f'start {cert_path}')
    else:
        messagebox.showerror("Error", "No certificate found. Complete the quiz first.")

# Load Home Screen
show_main_menu()

# Run GUI
root.mainloop()
