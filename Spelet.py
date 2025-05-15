import random
import tkinter as tk
from tkinter import messagebox

# Klass för spellojiken
class HangmanGame:
    def __init__(self, word_file="words.txt", score_file="score.txt"):
        # Initierar spelet med standardfiler för ord och poäng
        self.word_file = word_file
        self.score_file = score_file
        self.reset_game()

    def load_words(self):
        # Läser in ord från fil
        try:
            with open(self.word_file, 'r', encoding='utf-8') as file:
                return [line.strip().upper() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("Fel", "Filen med ord hittades inte.")
            return []

    def save_score(self, score):
        # Sparar spelarens poäng till fil
        with open(self.score_file, 'a', encoding='utf-8') as file:
            file.write(f"{score}\n")

    def reset_game(self):
        # Startar ett nytt spel
        words = self.load_words()
        if not words:
            self.word = ""
            return False
        self.word = random.choice(words)
        self.guessed_letters = set()
        self.correct_letters = set(self.word)
        self.attempts = 16
        return True

    def guess(self, letter):
        # Hanterar en gissning
        letter = letter.upper()
        if len(letter) != 1 or not letter.isalpha():
            return "Fel format"
        if letter in self.guessed_letters:
            return "Redan gissat"

        self.guessed_letters.add(letter)
        if letter in self.correct_letters:
            self.correct_letters.remove(letter)
            return "Rätt"
        else:
            self.attempts -= 1
            return "Fel"

    def is_won(self):
        # Kollar om spelaren har vunnit
        return not self.correct_letters

    def is_lost(self):
        # Kollar om spelaren har förlorat
        return self.attempts <= 0

    def get_display_word(self):
        # Returnerar ordet med _ för ogissade bokstäver
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)


# Klass för grafiska gränssnittet
class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hänga Gubbe")

        self.game = HangmanGame()
        # Laddar in bilder för gubben
        self.hangman_images = [
            tk.PhotoImage(file=f"hangman{i}.png").subsample(2, 2) for i in range(17)
        ]

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        # Skapar alla GUI-komponenter
        self.hangman_image = tk.Label(self.root)
        self.hangman_image.pack()

        self.word_display = tk.Label(self.root, text="", font=("Arial", 20))
        self.word_display.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack()

        self.guess_button = tk.Button(self.root, text="Gissa", command=self.guess_letter)
        self.guess_button.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.attempts_label.pack()

        self.new_game_button = tk.Button(self.root, text="Nytt spel", command=self.new_game)
        self.new_game_button.pack(pady=10)

    def new_game(self):
        # Startar nytt spel och uppdaterar GUI
        if not self.game.reset_game():
            return
        self.update_display()

    def guess_letter(self):
        # Hanterar när spelaren klickar på "Gissa"
        letter = self.entry.get().upper()
        self.entry.delete(0, tk.END)

        result = self.game.guess(letter)
        if result == "Fel format":
            messagebox.showwarning("Fel", "Ange en enda bokstav.")
        elif result == "Redan gissat":
            messagebox.showinfo("Info", "Du har redan gissat den bokstaven.")
        self.update_display()
        self.check_game_over()

    def update_display(self):
        # Uppdaterar ordet och antal försök i GUI
        self.word_display.config(text=self.game.get_display_word())
        self.attempts_label.config(text=f"Försök kvar: {self.game.attempts}")
        self.update_hangman_image()

    def update_hangman_image(self):
        # Uppdaterar bilden för hängda gubben
        index = min(16 - self.game.attempts, len(self.hangman_images) - 1)
        scaled_image = self.hangman_images[index]
        self.hangman_image.config(image=scaled_image)
        self.hangman_image.image = scaled_image  # Behåller referens så att bilden inte försvinner

    def check_game_over(self):
        # Kollar om spelet är slut (vinst eller förlust)
        if self.game.is_won():
            messagebox.showinfo("Grattis!", f"Du vann! Ordet var: {self.game.word}")
            self.game.save_score(1)
            self.new_game()
        elif self.game.is_lost():
            messagebox.showinfo("Game Over", f"Du förlorade! Ordet var: {self.game.word}")
            self.game.save_score(0)
            self.new_game()


# Startar spelet
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
