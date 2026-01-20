def load_scores():
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
    with open("scoreboard.txt", "w") as score_file:
        for entry in scores:
            score_file.write(f"{entry['name']},{entry['score']}\n")

def update_scores(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})

    # Sort descending by score
    scores.sort(key=lambda x: x["score"], reverse=True)
    # Keep only top N
    scores = scores[:5]
    save_scores(scores)
    return scores
