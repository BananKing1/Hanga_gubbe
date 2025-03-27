import random
import tkinter as tk
from tkinter import messagebox

def load_words(filename):
    """Läser in ord från en fil och returnerar en lista."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file.readlines()]
        return words
    except FileNotFoundError:
        messagebox.showerror("Fel", "Filen med ord hittades inte.")
        return []

def save_score(score, filename="score.txt"):
    """Sparar spelarens poäng i en fil."""
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{score}\n")

def new_game():
    global word, guessed_letters, correct_letters, attempts
    words = load_words("words.txt")
    if not words:
        return
    
    word = random.choice(words).upper()
    guessed_letters = set()
    correct_letters = set(word)
    attempts = 16
    update_display()

def guess_letter():
    global attempts
    letter = entry.get().upper()
    entry.delete(0, tk.END)
    
    if len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("Fel", "Ange en enda bokstav.")
        return
    
    if letter in guessed_letters:
        messagebox.showinfo("Info", "Du har redan gissat den bokstaven.")
        return
    
    guessed_letters.add(letter)
    
    if letter in correct_letters:
        correct_letters.remove(letter)
    else:
        attempts -= 1
    
    update_display()
    check_game_over()

def update_display():
    word_display.config(text=" ".join(letter if letter in guessed_letters else "_" for letter in word))
    attempts_label.config(text=f"Försök kvar: {attempts}")
    update_hangman_image()

def update_hangman_image():
    hangman_image.config(image=hangman_images[6 - attempts])

def check_game_over():
    if not correct_letters:
        messagebox.showinfo("Grattis!", f"Du vann! Ordet var: {word}")
        save_score(1)
        new_game()
    elif attempts == 0:
        messagebox.showinfo("Game Over", f"Du förlorade! Ordet var: {word}")
        save_score(0)
        new_game()

root = tk.Tk()
root.title("Hänga Gubbe")

hangman_images = [tk.PhotoImage(file=f"hangman{i}.png") for i in range(7)]
hangman_image = tk.Label(root)
hangman_image.pack()

word_display = tk.Label(root, text="", font=("Arial", 20))
word_display.pack(pady=20)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack()

guess_button = tk.Button(root, text="Gissa", command=guess_letter)
guess_button.pack(pady=10)

attempts_label = tk.Label(root, text="", font=("Arial", 14))
attempts_label.pack()

new_game_button = tk.Button(root, text="Nytt spel", command=new_game)
new_game_button.pack(pady=10)

new_game()
root.mainloop()
