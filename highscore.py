def save_high_score(score):
    """
    Saves the provided score as a high score.

    Parameters:

    - score (int) : The score to be saved as a high score.

    Returns : None

    """
    with open("Scores/high_score.txt", "w") as file:
        file.write(str(score))


def load_high_score():
    """
    Load the high score from the saved file.

    Returns:
        int : The loaded high score, or 0 if the file is not found

    """
    try:
        with open("Scores/high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0