import tkinter as tk
from tkinter import Label, Radiobutton, Button, messagebox, Entry
import os
import random
from PIL import Image, ImageDraw, ImageFont

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
questions_file = os.path.join(script_dir, "questions.txt")
history_file = os.path.join(script_dir, "quiz_history.txt")
certificate_dir = os.path.join(script_dir, "certificate")

# Ensure certificate folder exists
if not os.path.exists(certificate_dir):
    os.makedirs(certificate_dir)

#  Questions
questions = []
answers = {}  # will store correct answers for later use if needed
if os.path.exists(questions_file):
    with open(questions_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):
            question = lines[i].strip()
            options = [lines[i + 1].strip(), lines[i + 2].strip(), lines[i + 3].strip(), lines[i + 4].strip()]
            correct = lines[i + 5].strip()
            questions.append((question, options, correct))
else:
    messagebox.showerror("Error", "questions.txt file not found!")
    exit()

# Shuffle and select 30 questions
random.shuffle(questions)
selected_questions = questions[:30]

# Global Variables
score = 0
question_index = 0
user_name = ""
user_answers = [""] * len(selected_questions)  # stores the selected option for each question
question_buttons = []  # holds the navigation buttons for each question

# GUI Setup
root = tk.Tk()
root.title("Python Certification Quiz")
root.state("zoomed")  # Full-screen mode
root.configure(bg="#ffebcd")  # Light peach background

# Certificate Generation (More Colorful & Attractive)
def generate_certificate(name):
    cert_path = os.path.join(certificate_dir, f"{name}_certificate.png")

    # Create certificate image
    img = Image.new('RGB', (900, 600), "#f8f8ff")  # Light grayish-blue background
    draw = ImageDraw.Draw(img)

    for i in range(600):
        color = (255 - i // 3, 255 - i // 6, 255)
        draw.line([(0, i), (900, i)], fill=color, width=1)

    # Fonts
    font_title = ImageFont.truetype("arial.ttf", 50)
    font_subtitle = ImageFont.truetype("arial.ttf", 30)
    font_text = ImageFont.truetype("arial.ttf", 25)

    # Borders
    draw.rectangle([(30, 30), (870, 570)], outline="black", width=10)
    draw.rectangle([(40, 40), (860, 560)], outline="blue", width=6)
    draw.rectangle([(50, 50), (850, 550)], outline="red", width=3)

    # Text Content
    draw.text((230, 80), "Certificate of Achievement", font=font_title, fill="darkblue")
    draw.text((150, 200), f"This is to certify that", font=font_subtitle, fill="black")
    draw.text((320, 250), name, font=ImageFont.truetype("arial.ttf", 40), fill="#ff9200")
    draw.text((150, 300), "has successfully completed the Python Quiz.", font=font_subtitle, fill="black")
    draw.text((150, 360), f"Score: {score}/30", font=font_subtitle, fill="green")
    draw.text((150, 480), "Issued by: Python Learning Platform", font=font_text, fill="black")

    # Save Certificate
    img.save(cert_path)
    messagebox.showinfo("Certificate Generated", f"Certificate saved at:\n{cert_path}")

# Start Quiz (After Entering Name)
def start_quiz():
    global user_name, question_index, score
    user_name = name_entry.get().strip()
    if not user_name:
        messagebox.showerror("Error", "Please enter your name before starting the quiz.")
        return
    # Reset score and question index in case of restart
    score = 0
    question_index = 0
    clear_window()
    show_quiz()

# Clear Window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Navigation: Jump to specific question from grid
def go_to_question(idx):
    global question_index
    # Save current answer before moving
    user_answers[question_index] = var.get()
    update_nav_button(question_index)
    question_index = idx
    load_question(question_index)

# Update a navigation button's color based on answer selection
def update_nav_button(idx):
    
    if user_answers[idx] != "":
        question_buttons[idx].configure(bg="green")
    else:
        question_buttons[idx].configure(bg="red")

# Quiz UI
def show_quiz():
    global frame, question_label, progress_label, option_buttons, button_frame, var, question_buttons

    # Create Navigation Grid in top left corner
    nav_frame = tk.Frame(root, bg="#ffebcd")
    nav_frame.place(x=10, y=10)
    question_buttons.clear()
    for i in range(len(selected_questions)):
        btn = Button(nav_frame, text=str(i+1), width=3, font=("Arial", 10),
                     bg="red", fg="white", command=lambda i=i: go_to_question(i))
        row = i // 6  # 6 columns per row
        col = i % 6
        btn.grid(row=row, column=col, padx=2, pady=2)
        question_buttons.append(btn)

    var = tk.StringVar(root)
    var.set("")

    # Main quiz frame (centered)
    frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=5, highlightbackground="#ff4500", highlightthickness=3)
    frame.place(relx=0.5, rely=0.55, anchor="center")

    question_label = Label(frame, font=("Arial", 16, "bold"), bg="#ffffff", wraplength=800, fg="#333")
    question_label.pack(pady=15)

    progress_label = Label(root, text="Progress: 0/30", font=("Arial", 14), bg="#ffebcd", fg="#000")
    progress_label.place(relx=0.5, rely=0.15, anchor="center")

    option_buttons = []
    for _ in range(4):
        rb = Radiobutton(frame, variable=var, font=("Arial", 14), bg="#ffffff", fg="#00008b", selectcolor="#ffdab9")
        rb.pack(anchor="w", padx=15, pady=8)
        option_buttons.append(rb)

    button_frame = tk.Frame(frame, bg="#ffffff")
    button_frame.pack(pady=25)

    Button(button_frame, text="Previous", width=12, font=("Arial", 14), bg="#ffa500", fg="white", command=prev_question).pack(side="left", padx=15)
    Button(button_frame, text="Next", width=12, font=("Arial", 14), bg="#32cd32", fg="white", command=next_question).pack(side="left", padx=15)
    Button(button_frame, text="End Test", width=12, font=("Arial", 14), bg="#dc143c", fg="white", command=end_test).pack(side="right", padx=15)

    Button(root, text="Back", width=15, font=("Arial", 14), bg="#d32f2f", fg="white", command=show_main_menu).place(relx=0.5, rely=0.9, anchor="center")

    load_question(0)

# Load Question
def load_question(index):
    question, options, correct = selected_questions[index]
    question_label.config(text=f"Question {index + 1}: {question}")
    progress_label.config(text=f"Progress: {index + 1}/30")
    # Set previous selection if any
    var.set(user_answers[index])
    for i in range(4):
        option_buttons[i].config(text=options[i], value=options[i])
    answers[index] = correct

# Previous Question
def prev_question():
    global question_index
    # Save current answer
    user_answers[question_index] = var.get()
    update_nav_button(question_index)
    if question_index > 0:
        question_index -= 1
        load_question(question_index)

# Next Question
def next_question():
    global question_index, score
    user_answers[question_index] = var.get()
    update_nav_button(question_index)
    # Optionally, check answer correctness here if needed:
    if var.get() == answers[question_index]:
        score += 1
    if question_index < len(selected_questions) - 1:
        question_index += 1
        load_question(question_index)
    else:
        end_test()

# End Test
def end_test():
    user_answers[question_index] = var.get()
    update_nav_button(question_index)
    # Final check on current question (if not already counted)
    if var.get() == answers[question_index]:
        pass  # score already updated in next_question; adjust as needed
    if score > 0:
        generate_certificate(user_name)
    else:
        messagebox.showinfo("Quiz Completed", f"Your score: {score}/30\nScore must be greater than 20 to get a certificate.")
    show_main_menu()

# Name Entry Screen
def enter_name_screen():
    clear_window()

    frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=5, highlightbackground="#ff4500", highlightthickness=3)
    frame.place(relx=0.5, rely=0.45, anchor="center")

    Label(frame, text="Enter Your Name:", font=("Arial", 20), bg="#ffffff").pack(pady=20)

    global name_entry
    name_entry = Entry(frame, font=("Arial", 18))
    name_entry.pack(pady=10)

    Label(frame, text="Note: Score at least 20 marks to get a certificate", font=("Arial", 15)).pack(pady=20)

    Button(frame, text="Start Quiz", width=15, font=("Arial", 16), bg="#1e88e5", fg="white", command=start_quiz).pack(pady=20)

# Home Screen
def show_main_menu():
    clear_window()
    Label(root, text="Python Certification Quiz", font=("Arial", 28, "bold"), bg="#ffebcd").pack(pady=40)
    Button(root, text="Start Certification Quiz", width=25, font=("Arial", 16), bg="#1e88e5", fg="white", command=enter_name_screen).pack(pady=20)
    Button(root, text="Exit", width=15, font=("Arial", 14), bg="red", fg="white", command=root.destroy).pack(pady=20)

# Load Home Screen
show_main_menu()

# Run GUI
root.mainloop()
