import os 
import subprocess
import tkinter as tk
from tkinter import Button, Frame, Label, Scrollbar, Text

class PythonLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning Platform")
        self.root.state("zoomed")
        self.root.config(bg="#f0f8ff")

        # Get script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.chapter_dir = os.path.join(self.script_dir, "chapter")  # Path to chapter files C:\D\PYTHON\Learning_Platform_\Learning Platform\chapter

        self.create_home_page()

    def create_home_page(self):
        self.clear_window()
        home_frame = Frame(self.root, bg="#ffffff", bd=4, relief="solid", padx=20, pady=20)
        home_frame.pack(pady=50)

        Label(home_frame, text="Welcome to Python Learning Platform", font=("Arial", 24, "bold"), 
              bg="#0077b6", fg="white", pady=15).pack(fill="x")
        Label(home_frame, text="Learn Python step by step with interactive content", 
              font=("Arial", 16), bg="#ffffff", fg="#333", pady=10).pack()

        btn_frame = Frame(home_frame, bg="#ffffff", pady=20)
        btn_frame.pack()

        self.create_styled_button(btn_frame, "Start Learning", "#0288d1", self.show_chapters)
        self.create_styled_button(btn_frame, "Take a Quiz", "#00bcd4", self.start_quiz)
        self.create_styled_button(btn_frame, "Study Material", "#ff9800", self.study_material)
        self.create_styled_button(btn_frame, "Get Certificate", "#1e90ff", self.certificate)
        self.create_styled_button(btn_frame, "Exit", "#d32f2f", self.root.quit)

    def study_material(self):
        study_material_path = os.path.join(self.script_dir, "study_material.py")
        subprocess.Popen(["python", study_material_path], shell=True)

    def certificate(self):
        certificate_path = os.path.join(self.script_dir, "certificate.py")
        subprocess.Popen(["python", certificate_path], shell=True)

    def show_chapters(self):
        self.clear_window()
        Label(self.root, text="Select a Chapter", font=("Arial", 20, "bold"), 
              bg="#0077b6", fg="white", pady=10).pack(fill="x")

        frame = Frame(self.root, bg="#f0f8ff", padx=20, pady=20, bd=2, relief="ridge")
        frame.pack(pady=20)

        for i in range(1, 7):
            self.create_styled_button(frame, f"Chapter {i}", "#1976d2", lambda i=i: self.show_chapter(i))

        self.create_styled_button(self.root, "Back to Home", "#d32f2f", self.create_home_page)

    def show_chapter(self, chapter_number):
        self.clear_window()
        Label(self.root, text=f"Chapter {chapter_number}", font=("Arial", 20, "bold"),
              bg="#0077b6", fg="white", pady=10).pack(fill="x")

        chapter_path = os.path.join(self.chapter_dir, f"chapter{chapter_number}.txt")

        text_frame = Frame(self.root, bg="#f0f8ff")
        text_frame.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_box = Text(text_frame, wrap="word", font=("Arial", 14), bg="#ffffff", fg="#333",
                        yscrollcommand=scrollbar.set, padx=10, pady=10)
        text_box.pack(fill="both", expand=True)

        scrollbar.config(command=text_box.yview)

        if os.path.exists(chapter_path):
            with open(chapter_path, "r", encoding="utf-8") as file:
                text_box.insert("1.0", file.read())
        else:
            text_box.insert("1.0", "Chapter content not found.")

        text_box.config(state="disabled")

        self.create_styled_button(self.root, "Back to Chapters", "#d32f2f", self.show_chapters)

    def create_styled_button(self, parent, text, color, command):
        btn = Button(parent, text=text, width=25, font=("Arial", 14), bg=color, fg="white", bd=2, 
                     relief="raised", command=command, activebackground="#ffffff", activeforeground=color)
        btn.pack(pady=8)

    def start_quiz(self):
        quiz_path = os.path.join(self.script_dir, "quize.py")
        subprocess.Popen(["python", quiz_path], shell=True)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create main application window
root = tk.Tk()
app = PythonLearningApp(root)
root.mainloop()
