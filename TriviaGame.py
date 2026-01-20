import tkinter as tk
from tkinter import messagebox
import random
from Reading_Trivia_File import load_trivia

class TriviaGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Game")
        self.master.geometry("600x400")

        # Load quiz
        self.quiz = load_trivia()
        self.score = 0
        self.question_number = 0
        self.asked_questions = []

        # GUI Elements
        self.question_label = tk.Label(master, text="", wraplength=550, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=20)

        self.choice_buttons = {}

        for letter in ["A", "B", "C", "D"]:
            btn = tk.Button(self.buttons_frame, text="", width=20, command=lambda l=letter: self.check_answer(l))
            btn.pack(pady=5)
            self.choice_buttons[letter] = btn

        # Score label
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Start first question
        self.next_question()

    if __name__ == "__main__":
        root = tk.Tk()
        game = TriviaGame(root)
        root.mainloop()