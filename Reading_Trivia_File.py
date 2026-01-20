"""
Molly O'Connor
January 17, 2025

Module to load movie trivia questions from a text file.

- Reads questions from the "movies" file.
- Each question starts with '#Q', correct answer with '^', and choices with 'A ', 'B ', etc.
- Returns a list of dictionaries, each representing a question with its prompt, choices, and correct answer.
"""


def load_trivia():
    """
    Reads trivia questions from the 'movies' file and returns them as a list of dictionaries.

    Each dictionary contains:
    - 'prompt': The text of the question
    - 'correct_answer': The correct answer string
    - 'choices': A dictionary of all answer options (A, B, C, D)
    """
    trivia_questions = []

    # Open the file containing all trivia questions
    with open("movies", "r") as file:
        current_question = None

        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip blank lines

            # Start of a new question
            if line.startswith("#Q"):
                # Save previous question
                if current_question is not None:
                    trivia_questions.append(current_question)

                current_question = {
                    "prompt": line[3:].strip(),  # remove "#Q" and get the prompt
                    "correct_answer": "",
                    "choices": {}
                }

            # Correct answer
            elif line.startswith("^"):
                current_question["correct_answer"] = line[1:].strip()

            # Checks to make sure first character is (A/B/C/D)
            # Ensures the line is long enough to have a letter, a space, and some text
            # Checks second character is a " "
            elif line[0].isalpha() and len(line) > 2 and line[1] == " ":  # remove '^' and store
                letter = line[0]
                answer_text = line[2:].strip()
                current_question["choices"][letter] = answer_text

            # Any other line that is not ^ or a choice is part of the prompt
            else:
                if current_question is not None:
                    current_question["prompt"] += " " + line  # append with space

        # Add the last question
        if current_question is not None:
            trivia_questions.append(current_question)

    return trivia_questions
