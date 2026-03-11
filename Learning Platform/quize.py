import os
import random
import tkinter as tk
from tkinter import Button, Label, Radiobutton, messagebox

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "questions.txt")
history_file = os.path.join(script_dir, "quiz_history.txt")

# Ensure the file exists
if not os.path.exists(file_path):
    messagebox.showerror("Error", "questions.txt file not found!")
    exit()

# Load questions from file
questions = []
answers = {}

with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for i in range(0, len(lines), 6):
        question = lines[i].strip()
        option1 = lines[i + 1].strip()
        option2 = lines[i + 2].strip()
        option3 = lines[i + 3].strip()
        option4 = lines[i + 4].strip()
        correct = lines[i + 5].strip()
        questions.append((question, [option1, option2, option3, option4], correct))

# Shuffle and pick 10 questions
random.shuffle(questions)
selected_questions = questions[:10]

# Initialize quiz variables
score = 0
question_index = 0
attempts = 0
user_answers = {}  # Stores selected answers
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        attempts = len(f.readlines())

# GUI setup
root = tk.Tk()
root.title("Quiz Page")
root.state("zoomed")  # Make full screen
root.configure(bg="#ffebcd")  # Light peach background

# Create button references
question_buttons = []

# Function to show main menu
def show_main_menu():
    global question_index, score
    question_index = 0
    score = 0
    clear_window()
    Label(root, text="Welcome to the Quiz", font=("Arial", 24, "bold"), bg="#ffebcd").pack(pady=30)
    Button(root, text="Start Quiz", width=20, font=("Arial", 14), bg="#32cd32", fg="white", command=start_quiz).pack(pady=10)
    Button(root, text=f"Previous Attempts: {attempts}", width=20, font=("Arial", 14), bg="#ffa500", fg="white").pack(pady=10)
    Button(root, text="History", width=20, font=("Arial", 14), bg="#1e90ff", fg="white", command=show_history).pack(pady=10)
    Button(root, text="Back", width=20, font=("Arial", 14), bg="#d32f2f", fg="white", command=root.quit).pack(pady=10)

# Function to start the quiz
def start_quiz():
    clear_window()
    create_nav_buttons()
    show_quiz()

# Function to clear the window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Create navigation buttons for questions 1-10
def create_nav_buttons():
    global question_buttons
    nav_frame = tk.Frame(root, bg="#ffebcd")
    nav_frame.pack(pady=10)

    question_buttons.clear()
    for i in range(10):
        btn = Button(nav_frame, text=str(i + 1), width=4, font=("Arial", 12), bg="#d3d3d3", command=lambda idx=i: go_to_question(idx))
        btn.grid(row=0, column=i, padx=5)
        question_buttons.append(btn)

# Quiz UI
def show_quiz():
    global frame, question_label, progress_label, option_buttons, button_frame, var

    var = tk.StringVar(root)
    frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=5, highlightbackground="#ff4500", highlightthickness=3)
    frame.place(relx=0.5, rely=0.45, anchor="center")

    question_label = Label(frame, font=("Arial", 16, "bold"), bg="#ffffff", wraplength=800, fg="#333")
    question_label.pack(pady=15)

    progress_label = Label(root, text="Progress: 0/10", font=("Arial", 14), bg="#ffebcd", fg="#000")
    progress_label.place(relx=0.5, rely=0.1, anchor="center")

    option_buttons = []
    for _ in range(4):  # Fix: Changed loop range to 4
        rb = Radiobutton(frame, variable=var, font=("Arial", 14), bg="#ffffff", fg="#00008b", selectcolor="#ffdab9",
                         command=update_button_color)
        rb.pack(anchor="w", padx=15, pady=8)
        option_buttons.append(rb)

    button_frame = tk.Frame(frame, bg="#ffffff")
    button_frame.pack(pady=25)

    Button(button_frame, text="Previous", width=12, font=("Arial", 14), bg="#ffa500", fg="white", command=prev_question).pack(side="left", padx=15)
    Button(button_frame, text="Next", width=12, font=("Arial", 14), bg="#32cd32", fg="white", command=next_question).pack(side="left", padx=15)
    Button(button_frame, text="End Test", width=12, font=("Arial", 14), bg="#dc143c", fg="white", command=end_test).pack(side="right", padx=15)
    Button(root, text="Back", width=15, font=("Arial", 14), bg="#d32f2f", fg="white", command=show_main_menu).place(relx=0.5, rely=0.85, anchor="center")

    load_question(question_index)

# Load question
def load_question(index):
    question, options, correct = selected_questions[index]
    question_label.config(text=f"Question {index + 1}: {question}")
    progress_label.config(text=f"Progress: {index + 1}/10")

    var.set(user_answers.get(index, None))  # Restore previous selection

    for i in range(4):  # Fix: Ensure all four options are shown
        option_buttons[i].config(text=options[i], value=options[i])

    answers[index] = correct
    update_button_color()

# Navigate previous question
def prev_question():
    global question_index
    if question_index > 0:
        question_index -= 1
        load_question(question_index)

# Navigate next question
def next_question():
    global question_index
    check_answer()
    if question_index < 9:
        question_index += 1
        load_question(question_index)
    else:
        end_test()

# Navigate to a specific question
def go_to_question(index):
    global question_index
    question_index = index
    load_question(question_index)

# Check answer
def check_answer():
    global score
    selected_option = var.get()
    if selected_option:
        user_answers[question_index] = selected_option
        if selected_option == answers[question_index]:
            score += 1

# Update button color based on selection
def update_button_color():
    for i in range(10):
        if i in user_answers:
            question_buttons[i].config(bg="#32cd32", fg="white")  # Green if answered
        else:
            question_buttons[i].config(bg="#d3d3d3", fg="black")  # Gray if unanswered

# End quiz
def end_test():
    global attempts
    check_answer()
    with open(history_file, "a") as f:
        f.write(f"Score: {score}/10\n")
    attempts += 1
    messagebox.showinfo("Quiz Completed", f"Your Final Score: {score}/10")
    show_main_menu()

# Show history
def show_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = f.read()
        messagebox.showinfo("Quiz History", history if history else "No history available.")
    else:
        messagebox.showinfo("Quiz History", "No history available.")

# Load the main menu
show_main_menu()

# Run the GUI
root.mainloop()
