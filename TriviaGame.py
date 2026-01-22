"""
Molly O'Connor
January 17, 2025

Ultimate Movie Trivia Game using Tkinter.

This game features:
- Fullscreen window with a movie-themed background
- Player enters a name (5–15 characters, must be unique)
- Random multiple-choice movie trivia questions
- Scoring: +5 points for correct, -1 point for incorrect
- 60-second timer to complete as many questions as possible
- Tracks score in real time and shows the Top 5 leaderboard
- Highlights correct/incorrect answers and provides feedback
- After the game, shows final scoreboard with options to replay or exit
"""

import tkinter as tk
from tkmacosx import Button
import random
from Reading_Trivia_File import load_trivia
from Scoreboard_Logic import update_scores, save_scores
from Scoreboard_Logic import load_scores
from PIL import Image, ImageTk


class TriviaGame:
    """
    TriviaGame manages the main game interface, including:
    - displaying instructions
    - showing questions and answer buttons
    - tracking the player's score and time
    - displaying the final scoreboard
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Game")
        self.master.attributes("-fullscreen", True)
        self.player_name = ""
        self.quiz = load_trivia()
        self.current_score = 0

        # Set background inside the class
        self.set_background("movie.jpg")

        # This frame holds all UI elements and sits on top of the background
        self.ui_frame = tk.Frame(self.master, bg="white", bd=5, relief="ridge")
        self.ui_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Show instructions and initializes game
        self.show_instructions()

    def set_background(self, image_path):
        """
        Sets a background image for the game window.
        The image is resized to fill the entire screen and attached to a Label
        that sits behind all other widgets.
        """
        self.master.update_idletasks()  # Ensures window and widget sizes are updated before using them
        self.bg_image = Image.open(image_path)

        # Resize to window size
        self.bg_image = self.bg_image.resize(
            (self.master.winfo_screenwidth(), self.master.winfo_screenheight())
        )

        # Convert the image to a Tkinter-compatible image
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Keep a reference of the image
        self.bg_label.image = self.bg_photo

    def show_instructions(self):
        """
        Clear the UI frame and show the game instructions.
        Explains how to play, scoring rules (5 points for correct, -1 for wrong),
        and the 60-second time limit. Provides an entry for the player’s name
        and a button to start the game that isn't enabled until there is a valid entry for name.
        """
        # Use this to clear any existing widgets in the ui_frame
        for widget in self.ui_frame.winfo_children():
            widget.destroy()

        # TITLE LABEL
        title_label = tk.Label(
            self.ui_frame,
            text="Welcome to the Ultimate Movie Trivia Game!",
            font=("Helvetica", 24, "bold"),
            fg="red",
            bg=self.ui_frame["bg"],
            pady=20
        )
        title_label.pack(padx=20)

        # INSTRUCTIONS LABEL
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
            font=("Helvetica", 18),
            fg="black",
            justify="center",
            wraplength=700,  # wrap text
            pady=20,
            bg=self.ui_frame["bg"]
        )
        instructions_label.pack(padx=50)

        # ENTRY BOX FOR PLAYER NAME
        self.name_entry = tk.Entry(self.ui_frame, font=("Helvetica", 16), bg=self.ui_frame["bg"])
        self.name_entry.pack(padx=5, pady=(0, 20))

        # WARNING LABEL FOR VALIDATION PURPOSES
        self.name_warning = tk.Label(
            self.ui_frame,
            text="",  # Initially Empty
            font=("Helvetica", 12, "italic"),
            fg="red",
            bg=self.ui_frame["bg"]
        )
        self.name_warning.pack(pady=(0, 20))

        # START BUTTON (INITIALLY DISABLED)
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
            command=self.start_game
        )
        self.start_button.pack(pady=40)

        # Run check_name_entry every time the user types or releases a key in the name entry box
        self.name_entry.bind("<KeyRelease>", self.check_name_entry)

    def check_name_entry(self, event=None):
        """
        Checks the player's name entry for validity.

        - Ensures the name is at least 5 characters and no more than 15.
        - Checks that the name isn't already in the scoreboard.
        - Displays a warning if invalid and disables the Start button.
        - Enables the Start button if the name is valid.
        """
        name = self.name_entry.get().strip()  # removes a space from the beginning or end of the entry
        scores_list = load_scores()  # loads the existing entries from the scoreboard

        # Check to see if the name is unique
        name_taken = any(entry['name'].lower() == name.lower() for entry in scores_list)

        # Validate name length and uniqueness (enables start button once all conditions are met)
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
            self.name_warning.config(text="")  # clear the warning label
            self.start_button.config(state="normal")

    def start_game(self):
        """
        Sets up the game screen: displays the player's score and a 60-second countdown timer,
        starts the countdown, and loads the first trivia question. Updates the timer every second
        and ends the game when time runs out, disabling unanswered buttons.
        """

        # If for some reason validation doesn't work, username will be "Unknown Player"
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            self.player_name = "Unknown Player"

        # SCORE LABEL
        self.score_label = tk.Label(self.ui_frame,
                                    text=f"Score: {self.current_score}",
                                    font=("Helvetica", 16, "bold"),
                                    fg="green", bg=self.ui_frame["bg"])
        self.score_label.pack(pady=10)

        # TIMER LABEL
        self.time_left = 60  # seconds
        self.timer_label = tk.Label(
            self.ui_frame,
            text=f"Time Left: {self.time_left} s",
            font=("Helvetica", 16, "bold"),
            fg="red", bg=self.ui_frame["bg"]
        )
        self.timer_label.pack(pady=10)

        def update_timer():
            """
            Decreases the game timer by one second every second, updates the timer label,
            and checks if time has run out. If time reaches zero, disables any unanswered
            answer buttons and calls the times_up() function to end the round.
            """
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=f"Time Left: {self.time_left} s")
                self.master.after(1000, update_timer)  # Recursively calls itself
            else:
                # Time's up: disable buttons if they haven't clicked
                for b in self.answer_buttons:
                    if b['state'] == "normal":
                        b.config(state="disabled")
                self.times_up()

        # Start the timer countdown
        update_timer()
        self.get_question()

    def get_question(self):
        """
        Loads and displays a new trivia question on the game screen.
        Clears previous question widgets while keeping the timer and score visible.

        - Picks a random question from the quiz list.
        - Displays the question prompt in a label.
        - Creates buttons for each possible answer.
        - Handles clicks on answer buttons:
            * Correct answers add 5 points and turn the button green.
            * Incorrect answers subtract 1 point, turn the clicked button red,
              and highlight the correct answer in green.
        - Displays a "Result" label to show whether the player's choice was correct.
        - Provides a "Next Question" button to load the next question.
        """

        # Clear previous widgets except the score and time label
        for widget in self.ui_frame.winfo_children():
            if widget != self.timer_label and widget != self.score_label and widget != self.bg_label:  # keep the timer
                widget.destroy()

        # Pick a random question
        self.current_question = random.choice(self.quiz)

        # QUESTION LABEL
        self.question_label = tk.Label(
            self.ui_frame,
            text=self.current_question["prompt"],
            font=("Helvetica", 18, "bold"),
            wraplength=750,
            justify="center",
            fg="black",
            bg=self.ui_frame["bg"]
        )
        self.question_label.pack(pady=30)

        # Gets potential answers and the correct answer
        num_choices = self.current_question["choices"]
        correct_answer = self.current_question["correct_answer"]

        # List for each potential answer button
        self.answer_buttons = []

        # Create buttons and pass the button object and answer correctly
        for letter, answer_text in num_choices.items():
            btn = Button(
                self.ui_frame,
                text=f"{letter}: {answer_text}",
                width=1000,
                height=70,
                fg="black",
                font=("Helvetica", 16),
                padx=20, pady=20,
                bg=self.ui_frame["bg"]
            )
            btn.pack(pady=5, padx=20)

            # Capture both button and answer_text in lambda
            btn.config(command=lambda b=btn, a=answer_text: handle_click(a, b))

            self.answer_buttons.append(btn)

        # RESULT LABEL
        self.result_label = tk.Label(
            self.ui_frame,
            text="Result:",
            font=("Helvetica", 16, "bold"),
            fg="blue",
            bg=self.ui_frame["bg"]
        )
        self.result_label.pack(pady=30)

        def handle_click(selected_answer, button):
            """
            Handles the user's answer selection.

            Disables all answer buttons once one is clicked, checks if the selected answer
            is correct, updates the score accordingly (+5 for correct, -1 for incorrect),
            changes button colors to indicate correct (green) or incorrect (red) answers,
            updates the result label to show feedback, and creates a "Next Question" button
            to proceed to the next trivia question.
            """

            # Disable all buttons once they select one
            for b in self.answer_buttons:
                b.config(state="disabled")

            # Correct/Incorrect coloring and label updating
            if selected_answer == correct_answer:
                self.current_score += 5
                self.score_label.config(text=f"Score: {self.current_score}")
                self.result_label.config(text="Correct!", bg=self.ui_frame["bg"])
                button.config(bg="#4CAF50")  # Green for correct
            else:
                # Red for wrong
                button.config(bg="#F44336")
                if self.current_score > 0:
                    self.current_score -= 1
                    self.score_label.config(text=f"Score: {self.current_score}")
                    self.result_label.config(text=f"Incorrect! The answer was {correct_answer}", fg="#F44336",
                                             bg=self.ui_frame["bg"])
                # Pairs each button with it's corresponding answer
                for b, text in zip(self.answer_buttons, num_choices.values()):
                    # Highlights the correct answer in green
                    if text == correct_answer:
                        b.config(bg="#4CAF50")

            # NEXT BUTTON
            next_btn = Button(
                self.ui_frame,
                text="Next Question",
                width=600,
                height=60,
                font=("Helvetica", 14),
                padx=10, bg=self.ui_frame["bg"]
            )
            next_btn.pack(pady=20)
            next_btn.config(command=self.get_question)  # Generate new question when they click next

    def times_up(self):
        """
        Called when the game timer reaches zero. Clears the question and answer widgets,
        displays a countdown message for 3 seconds, and then automatically shows the
        scoreboard. Updates the countdown label every second to indicate time until the scoreboard.
        """

        # Clear question and answers
        for widget in self.ui_frame.winfo_children():
            widget.destroy()

        # COUNTDOWN LABEL
        countdown_label = tk.Label(
            self.ui_frame,
            text="",
            font=("Helvetica", 36, "bold"),
            fg="#E53935",  # bright red
            bg=self.ui_frame["bg"],  # match frame color
            pady=20
        )
        countdown_label.pack(pady=(20, 10))

        # Countdown function
        def countdown(n):
            """
            Recursively updates the countdown label each second, decreasing `n` by 1.
            When `n` reaches 0, it calls `display_score_board()` to show the final scores.
            Uses `self.master.after(1000, ...)` to schedule the next update after 1 second.
            """
            if n > 0:
                countdown_label.config(text=f"Time's Up! Showing scoreboard in {n}...")
                self.master.after(1000, countdown, n - 1)
            else:
                self.display_score_board()

        # Start countdown from 3
        countdown(3)

    def display_score_board(self):
        """
        Displays the scoreboard after the game ends. Clears the previous widgets, shows the
        player's score, checks if they made the top 5, displays the top scores, and adds a
        'Back to Start' button to return to the instructions. Applies consistent styling
        with colors, fonts, and spacing for clarity.
        """
        # Clear previous widgets in frame
        for widget in self.ui_frame.winfo_children():
            widget.destroy()

        # TITLE LABEL
        title = tk.Label(
            self.ui_frame,
            text="🏆 Score Board 🏆",
            font=("Helvetica", 28, "bold"),
            fg="#212121",  # dark gray
            bg=self.ui_frame["bg"],
            pady=20
        )
        title.pack(pady=(10, 20))

        # Update scores and load the top scores
        update_scores(self.player_name, self.current_score)
        scores_list = load_scores()  # already sorted top 5

        # PLAYER SCORE LABEL
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

        # MADE IT? MESSAGE LABEL
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
            # MAKE A LABEL FOR EAH TOP SCORE
            score_label = tk.Label(
                self.ui_frame,
                text=f"{entry['name']} - {entry['score']}",
                font=("Helvetica", 18),
                fg="#424242",
                bg=self.ui_frame["bg"],
                pady=5
            )
            score_label.pack()

        # BACK BUTTON
        back_btn = tk.Button(
            self.ui_frame,
            text="PLAY AGAIN",
            font=("Helvetica", 18, "bold"),
            bg="black",
            fg="black",
            width=20,
            height=2,
            bd=3,
            command=self.show_instructions
        )
        back_btn.pack(pady=(30, 20), padx=80)

        # EXIT BUTTON
        exit_btn = tk.Button(
            self.ui_frame,
            text="EXIT",
            font=("Helvetica", 18, "bold"),
            bg="black",
            fg="black",
            width=20,
            height=2,
            bd=3,
            command=self.master.destroy  # Destroys game
        )
        exit_btn.pack(pady=(30, 20), padx=80)


"""
Starts the Trivia Game application by creating the main Tkinter window,
initializing the TriviaGame class with that window, and starting the
Tkinter event loop so the GUI runs and responds to user interactions.
"""
if __name__ == "__main__":
    window = tk.Tk()
    game = TriviaGame(window)
    window.mainloop()
