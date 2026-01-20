# Ultimate Movie Trivia Game

# Overview

The **Ultimate Movie Trivia Game** is a Python GUI application built using **Tkinter**.  
Players answer multiple-choice movie trivia questions, aiming to score as many points as possible in **60 seconds**.  

**Features:**

- Fullscreen window with a movie-themed background.
- Player enters a name (5–15 characters, must be unique).
- Randomized multiple-choice movie trivia questions.
- Scoring: **+5 points** for correct answers, **-1 point** for incorrect answers.
- 60-second timer to complete as many questions as possible.
- Tracks score in real time and displays a **Top 5 leaderboard**.
- Highlights correct/incorrect answers and provides immediate feedback.
- After the game, displays the final scoreboard with options to **replay** or **exit**.

# Dataset

The trivia questions are loaded from a local file named `movies`, which is based on the Open Trivia QA dataset.  
The dataset can be found at the following link:  
[OpenTriviaQA Categories](https://github.com/uberspot/OpenTriviaQA/tree/master/categories)

You can use this dataset to add or update trivia questions.
This link also has more trivia categories avialble in the same format! 

# Requirements

To run this program, you need:

- **Python 3.11** (recommended for full Tkinter compatibility)
- **Tkinter** (usually comes with Python)
- **Pillow (PIL)** for image handling  

Install the Pillow library if you don't already have it:

```bash
pip install pillow
```

# How to Run

1. Ensure you have Python 3.11 installed.
2. Clone or download the repository.
3. Make sure the following files are present in the project folder:
   - `TriviaGame.py`
   - `Reading_Trivia_File.py`
   - `Scoreboard_Logic.py`
   - `movies` (the trivia dataset)
4. Open a terminal or command prompt, navigate to the project folder, and run:

```bash
python TriviaGame.py
```

5. The game opens in fullscreen mode. Enter your name, click **Start Game**, and begin answering trivia questions.
6. After 60 seconds, the final scoreboard is displayed showing your score and the Top 5 players.

# Future Ideas

Currently, this trivia game focuses on movies. However, the OpenTriviaQA repository provides many other categories in the same format, so adapting the game to a different topic would be straightforward. This allows for easy expansion and reproducibility with minimal changes to the code.


