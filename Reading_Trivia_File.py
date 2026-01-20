def load_trivia():
    quiz = []

    with open("movies", "r", encoding="utf-8") as file:
        current_question = None

        for line in file:
            line = line.strip()
            if not line:
                continue  # skip blank lines

            # Start of a new question
            if line.startswith("#Q"):
                if current_question is not None:
                    quiz.append(current_question)

                current_question = {
                    "prompt": line[3:].strip(),
                    "correct_answer": "",
                    "choices": {}
                }

            # Correct answer
            elif line.startswith("^"):
                current_question["correct_answer"] = line[1:].strip()

            # Answer choices (A, B, C, D)
            elif line[0].isalpha() and len(line) > 2 and line[1] == " ":
                letter = line[0]
                answer_text = line[2:].strip()
                current_question["choices"][letter] = answer_text

            # Any other line that is not ^ or a choice is part of the prompt
            else:
                if current_question is not None:
                    current_question["prompt"] += " " + line  # append with space

        # Add the last question
        if current_question is not None:
            quiz.append(current_question)

    return quiz