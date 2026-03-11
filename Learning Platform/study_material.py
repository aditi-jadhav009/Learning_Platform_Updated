import os
import tkinter as tk
from tkinter import Button, Frame, Label
from tkinter import filedialog

class StudyMaterialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Material")
        self.root.state("zoomed")
        self.root.geometry("600x400")
        self.root.config(bg="#f0f8ff")

        self.script_dir = r"C:\D\PYTHON\Learning_Platform_Updated\Learning Platform\download"
        self.study_materials = {
            "Notes": "notes.pdf",
            "PPT": "study_material.pptx",
            "Examination Paper Solution ": "PWP 22616 EPA.pdf",
            "Python Tricks(BOOK)": "Python Tricks.pdf"
        }

        self.create_ui()

    def create_ui(self):
        frame = Frame(self.root, bg="#ffffff", bd=4, relief="solid", padx=20, pady=20)
        frame.pack(pady=50)

        Label(frame, text="Download Study Material", font=("Arial", 18, "bold"),
              bg="#0077b6", fg="white", pady=10).pack(fill="x")

        for text, file_name in self.study_materials.items():
            self.create_styled_button(frame, text, "#0288d1", lambda f=file_name: self.open_file(f))

        self.create_styled_button(frame, "Exit", "#d32f2f", self.root.quit)

    def create_styled_button(self, parent, text, color, command):
        btn = Button(parent, text=text, width=25, font=("Arial", 14), bg=color, fg="white", bd=2, 
                     relief="raised", command=command, activebackground="#ffffff", activeforeground=color)
        btn.pack(pady=8)

    def open_file(self, file_name):
        file_path = os.path.join(self.script_dir, file_name)
        if os.path.exists(file_path):
            os.startfile(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyMaterialApp(root)
    root.mainloop()
