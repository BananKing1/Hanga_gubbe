import random

def load_words(filename):
    """Läser in ord från en fil och returnerar en lista."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file.readlines()]
        return words
    except FileNotFoundError:
        print("Filen med ord hittades inte.")
        return []

def save_score(score, filename="score.txt"):
    """Sparar spelarens poäng i en fil."""
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{score}\n")

def hangman():
    words = load_words("words.txt")
    if not words:
        return
    
    word = random.choice(words).upper()
    guessed_letters = set()
    correct_letters = set(word)
    attempts = 6
    
    print("Välkommen till Hänga Gubbe!")
    
    while attempts > 0 and correct_letters:
        print("\n" + " ".join(letter if letter in guessed_letters else "_" for letter in word))
        print(f"Felaktiga gissningar: {attempts} kvar")
        guess = input("Gissa en bokstav: ").upper()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Felaktig inmatning, gissa en enda bokstav.")
            continue
        
        if guess in guessed_letters:
            print("Du har redan gissat den bokstaven.")
            continue
        
        guessed_letters.add(guess)
        
        if guess in correct_letters:
            correct_letters.remove(guess)
            print("Rätt gissning!")
        else:
            attempts -= 1
            print("Fel gissning!")
    
    if not correct_letters:
        print(f"Grattis! Du gissade ordet: {word}")
        save_score(1)
    else:
        print(f"Game Over! Ordet var: {word}")
        save_score(0)

if __name__ == "__main__":
    hangman()
