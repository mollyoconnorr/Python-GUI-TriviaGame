"""
Molly O'Connor
January 17, 2026

Scoreboard Logic for Ultimate Movie Trivia Game

- Manages reading and writing player scores to a text file.
- Keeps a list of scores as dictionaries with 'name' and 'score'.
- Supports loading scores, saving scores, and updating the top 5 scores.
"""


def load_scores():
    """
    Reads scores from 'scoreboard.txt' and returns them as a list of dictionaries.
    Each dictionary has keys 'name' and 'score'. Skips invalid lines or if the file
    does not exist.
    """
    scores_list = []  # use a separate list
    try:
        with open("scoreboard.txt", "r") as score_file:
            for line in score_file:
                line = line.strip()
                if not line:
                    continue
                try:
                    name, score = line.split(",", 1)
                    scores_list.append({"name": name, "score": int(score)})
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return scores_list


def save_scores(scores):
    """
    Writes the given list of score dictionaries to 'scoreboard.txt'.
    Each line in the file is formatted as: name,score
    """
    with open("scoreboard.txt", "w") as score_file:  # Write permission
        for entry in scores:
            score_file.write(f"{entry['name']},{entry['score']}\n")


def update_scores(name, score):
    """
    Adds a new score for the given player name and keeps only the top 5 scores.
    Updates the scoreboard file and returns the updated top scores list.
    """
    scores = load_scores()
    scores.append({"name": name, "score": score})

    # Sort descending by score
    scores.sort(key=lambda x: x["score"], reverse=True)
    # Keep only top 5
    scores = scores[:5]
    save_scores(scores)
    return scores
