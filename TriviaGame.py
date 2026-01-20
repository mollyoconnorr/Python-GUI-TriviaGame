import tkinter as tk
from tkmacosx import Button
import random
from Reading_Trivia_File import load_trivia
from Scoreboard_Logic import update_scores, save_scores
from Scoreboard_Logic import load_scores
from PIL import Image, ImageTk


class TriviaGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Game")
        self.master.attributes("-fullscreen", True)
        self.player_name = ""
        self.quiz = load_trivia()
        self.current_score = 0

        # Set background inside the class
        self.set_background("movie.jpg")
        self.ui_frame = tk.Frame(self.master, bg="white", bd=5, relief="ridge")  # solid white background
        self.ui_frame.place(relx=0.5, rely=0.5, anchor="center")
        # Show instructions
        self.show_instructions()

    def set_background(self, image_path):
        self.master.update_idletasks()  # ensure window dimensions are correct
        self.bg_image = Image.open(image_path)

        # Resize to window size
        self.bg_image = self.bg_image.resize(
            (self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        )

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep reference to avoid garbage collection
        self.bg_label.image = self.bg_photo

    def show_instructions(self):
        # USE THIS TO CLEAR WIDGETS
        for widget in self.ui_frame.winfo_children():
                widget.destroy()

        # Title
        title_label = tk.Label(
            self.ui_frame,
            text="Welcome to the Ultimate Movie Trivia Game!",
            font=("Helvetica", 24, "bold"),
            fg="red",
            bg=self.ui_frame["bg"],
            pady=20
        )
        title_label.pack(padx=20)

        # Instructions
        instructions_label = tk.Label(
            self.ui_frame,
            text=(
                "Answer the questions as best you can.\n"
                "Each question has multiple choices.\n"
                "Choose an answer to proceed.\n\n"
                "You earn 5 points for each correct answer\n"
                "and lose 1 point for each incorrect answer.\n"
                "You have 60 seconds to get a score high enough\n"
                "to make the Top 5 leaderboard.\n\n"
                "Enter your name below and click Start Game!"
            ),
            font=("Helvetica", 16),
            justify="center",
            wraplength=700,  # wrap text nicely in the window
            pady=20,
            bg = self.ui_frame["bg"]
        )
        instructions_label.pack(padx=50)

        self.name_entry = tk.Entry(self.ui_frame, font=("Helvetica", 16), bg = self.ui_frame["bg"])
        self.name_entry.pack(padx=5, pady=(0, 20))

        # Warning label (initially empty)
        self.name_warning = tk.Label(
            self.ui_frame,
            text="",
            font=("Helvetica", 12, "italic"),
            fg="red",
            bg=self.ui_frame["bg"]
        )
        self.name_warning.pack(pady=(0, 20))

        # Start button initially disabled
        self.start_button = Button(
            self.ui_frame,
            text="Start Game",
            width=400,
            height=70,
            font=("Helvetica", 18, "bold"),
            bg="red",
            fg="white",
            padx=20,
            pady=20,
            state="disabled",
            command=self.start_game_with_name  # store string here
        )
        self.start_button.pack(pady=40)

        # Bind key release to enable button when typing
        self.name_entry.bind("<KeyRelease>", self.check_name_entry)

    def check_name_entry(self, event=None):
        name = self.name_entry.get().strip()
        scores_list = load_scores()  # get existing scores

        # Check if name is already in the scoreboard
        name_taken = any(entry['name'].lower() == name.lower() for entry in scores_list)

        # Validate name length and uniqueness
        if len(name) < 5:
            self.name_warning.config(text="Name must be at least 5 characters.")
            self.start_button.config(state="disabled")
        elif len(name) > 15:
            self.name_warning.config(text="Name cannot exceed 15 characters.")
            self.start_button.config(state="disabled")
        elif name_taken:
            self.name_warning.config(text="This name already exists. Choose another.")
            self.start_button.config(state="disabled")
        else:
            self.name_warning.config(text="")  # clear warning
            self.start_button.config(state="normal")

    def start_game_with_name(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            self.player_name = "Unknow Player"  # fallback name
        self.start_game()

    def start_game(self):
        self.score_label = tk.Label(self.ui_frame,
            text=f"Score: {self.current_score}",
            font=("Helvetica", 16, "bold"),
            fg="green", bg = self.ui_frame["bg"])
        self.score_label.pack(pady=10)

        self.time_left = 60 # 60 seconds
        self.timer_label = tk.Label(
            self.ui_frame,
            text=f"Time Left: {self.time_left} s",
            font=("Helvetica", 16, "bold"),
            fg="red", bg = self.ui_frame["bg"]
        )
        self.timer_label.pack(pady=10)

        def update_timer():
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=f"Time Left: {self.time_left} s")
                self.master.after(1000, update_timer)
            else:
                # Time's up: disable buttons if they haven't clicked
                for b in self.answer_buttons:
                    if b['state'] == "normal":
                        b.config(state="disabled")
                self.times_up()

        # Start the countdown
        update_timer()
        self.get_question()

    def get_question(self):
        # Clear previous widgets
        for widget in self.ui_frame.winfo_children():
            if widget != self.timer_label and widget != self.score_label and widget != self.bg_label:  # keep the timer
                widget.destroy()

        # Pick a random question
        self.current_question = random.choice(self.quiz)

        # Show the question
        self.question_label = tk.Label(
            self.ui_frame,
            text=self.current_question["prompt"],
            font=("Helvetica", 18, "bold"),
            wraplength=750,  # fits window width
            justify="center",
            bg=self.ui_frame["bg"]
        )
        self.question_label.pack(pady=30)

        # Get choices and correct answer
        num_choices = self.current_question["choices"]
        correct_answer = self.current_question["correct_answer"]

        self.answer_buttons = []

        def handle_click(selected_answer, button):
            # Disable all buttons
            for b in self.answer_buttons:
                b.config(state="disabled")

            # Correct/Incorrect coloring
            if selected_answer == correct_answer:
                self.current_score += 5
                self.score_label.config(text=f"Score: {self.current_score}")
                self.result_label.config(text="Correct!", bg=self.ui_frame["bg"])
                button.config(bg="#4CAF50")  # Green for correct
            else:
                # Red for wrong
                button.config(bg="#F44336")
                if self.current_score >0:
                    self.current_score -= 1
                    self.score_label.config(text=f"Score: {self.current_score}")
                # Highlight the correct answer in green
                # Zip pairs each button with it's corresponding answer
                for b, text in zip(self.answer_buttons, num_choices.values()):
                    if text == correct_answer:
                        b.config(bg="#4CAF50")
                    if selected_answer == correct_answer:
                        self.result_label.config(text="Correct!", fg="#4CAF50", bg=self.ui_frame["bg"])  # green
                    else:
                        self.result_label.config(text=f"Incorrect! The answer was {correct_answer}", fg="#F44336", bg=self.ui_frame["bg"])
            next_btn = Button(
                self.ui_frame,
                text="Next Question",
                width=600,
                height=60,
                font=("Helvetica", 14),
                padx=10, bg = self.ui_frame["bg"]
            )
            next_btn.pack(pady=20)
            next_btn.config(command=self.get_question)


        # Create buttons and pass the button object and answer correctly
        for letter, answer_text in num_choices.items():
            btn = Button(
                self.ui_frame,
                text=f"{letter}: {answer_text}",
                width=800,
                height=70,
                font=("Helvetica", 16),
                padx=20, pady=20,
                bg=self.ui_frame["bg"]
            )
            btn.pack(pady=5, padx=20)

            # Capture both button and answer_text in lambda
            btn.config(command=lambda b=btn, a=answer_text: handle_click(a, b))

            self.answer_buttons.append(btn)

        self.result_label = tk.Label(
            self.ui_frame,
            text="Result:",
            font=("Helvetica", 16, "bold"),
            fg="blue",
            bg=self.ui_frame["bg"]
        )
        self.result_label.pack(pady=30)

    def times_up(self):
        # Clear question and answers first
        for widget in self.ui_frame.winfo_children():
                widget.destroy()

        # Create a label to update countdown
        countdown_label = tk.Label(
            self.ui_frame,
            text="Time's Up!",
            font=("Helvetica", 36, "bold"),
            fg="#E53935",  # bright red
            bg=self.ui_frame["bg"],  # match frame color
            pady=20
        )
        countdown_label.pack(pady=(20, 10))

        # Countdown function
        def countdown(n):
            if n > 0:
                countdown_label.config(text=f"Time's Up! Showing scoreboard in {n}...")
                self.master.after(1000, countdown, n - 1)
            else:
                self.display_score_board()

        # Start countdown from 3
        countdown(3)

    def display_score_board(self):
        # Clear previous widgets in frame
        for widget in self.ui_frame.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(
            self.ui_frame,
            text="🏆 Score Board 🏆",
            font=("Helvetica", 28, "bold"),
            fg="#212121",  # dark gray
            bg=self.ui_frame["bg"],
            pady=20
        )
        title.pack(pady=(10, 20))  # top/bottom spacing

        # Update scores and load the top scores
        update_scores(self.player_name, self.current_score)
        scores_list = load_scores()  # already sorted top 5

        # Show player's score
        player_score = tk.Label(
            self.ui_frame,
            text=f'Your Score: {self.player_name} - {self.current_score}',
            font=("Helvetica", 24, "bold"),
            fg="#1976D2",  # nice blue
            bg=self.ui_frame["bg"],
            pady=10
        )
        player_score.pack(pady=(0, 15))

        # Check if player made the top scores
        made_top = any(
            entry['name'] == self.player_name and entry['score'] == self.current_score for entry in scores_list
        )
        message_text = "You made the Top 5!" if made_top else "You did not make the Top 5."
        top_msg = tk.Label(
            self.ui_frame,
            text=message_text,
            font=("Helvetica", 20, "italic"),
            fg="#E65100",  # deep orange
            bg=self.ui_frame["bg"],
            pady=10
        )
        top_msg.pack(pady=(0, 50))

        # Show top scores
        for entry in scores_list:
            score_label = tk.Label(
                self.ui_frame,
                text=f"{entry['name']} - {entry['score']}",
                font=("Helvetica", 18),
                fg="#424242",  # medium gray
                bg=self.ui_frame["bg"],
                pady=5
            )
            score_label.pack()

        # Back button with nicer styling
        back_btn = tk.Button(
            self.ui_frame,
            text="Back to Start",
            font=("Helvetica", 18, "bold"),
            bg="black",
            fg="black",
            width=20,
            height=2,
            bd=3,
            command=self.show_instructions
        )
        back_btn.pack(pady=(30, 20), padx=80)

if __name__ == "__main__":
    window = tk.Tk()
    game = TriviaGame(window)
    window.mainloop()