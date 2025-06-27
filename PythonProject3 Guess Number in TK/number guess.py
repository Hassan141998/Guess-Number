import random
import sys
from tkinter import Tk, Label, Entry, Button, messagebox, simpledialog, StringVar


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.score = 0
        self.difficulty = StringVar(value="medium")

        # Create UI
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        # Game info
        Label(self.root, text="Guess the number!", font=('Arial', 16)).pack(pady=10)

        # Difficulty selection
        Label(self.root, text="Select Difficulty:").pack()
        for level in ["easy", "medium", "hard"]:
            Button(self.root, text=level.capitalize(),
                   command=lambda l=level: self.set_difficulty(l),
                   bg="lightgreen" if level == "medium" else "white").pack(side="left", padx=5)

        # Guess entry
        Label(self.root, text="Your guess:").pack(pady=(20, 5))
        self.guess_entry = Entry(self.root, font=('Arial', 14))
        self.guess_entry.pack()
        self.guess_entry.bind('<Return>', lambda e: self.check_guess())

        # Submit button
        Button(self.root, text="Submit Guess", command=self.check_guess, bg="lightblue").pack(pady=10)

        # Game info display
        self.info_label = Label(self.root, text="", font=('Arial', 12))
        self.info_label.pack(pady=10)

        # Score display
        self.score_label = Label(self.root, text="Score: 0", font=('Arial', 12))
        self.score_label.pack()

    def set_difficulty(self, level):
        self.difficulty.set(level)
        self.start_new_game()

    def start_new_game(self):
        difficulty_settings = {
            "easy": (1, 50, 10),
            "medium": (1, 100, 7),
            "hard": (1, 200, 5)
        }

        min_num, max_num, self.max_attempts = difficulty_settings[self.difficulty.get()]
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0

        self.update_display(f"Guess a number between {min_num} and {max_num}. You have {self.max_attempts} attempts.")

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess == self.secret_number:
                self.handle_win()
            elif self.attempts >= self.max_attempts:
                self.handle_loss()
            elif guess < self.secret_number:
                self.update_display(f"Too low! Try a higher number. Attempts left: {self.max_attempts - self.attempts}")
            else:
                self.update_display(f"Too high! Try a lower number. Attempts left: {self.max_attempts - self.attempts}")

            self.guess_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def handle_win(self):
        points = (self.max_attempts - self.attempts + 1) * 10
        self.score += points
        self.update_display(f"Congratulations! You guessed it in {self.attempts} attempts. You earned {points} points.")
        self.score_label.config(text=f"Score: {self.score}")

        if messagebox.askyesno("Game Over", "You won! Play again?"):
            self.start_new_game()
        else:
            self.root.quit()

    def handle_loss(self):
        self.update_display(f"Game over! The number was {self.secret_number}.")

        if messagebox.askyesno("Game Over", "You lost. Try again?"):
            self.start_new_game()
        else:
            self.root.quit()

    def update_display(self, message):
        self.info_label.config(text=message)


if __name__ == "__main__":
    root = Tk()
    game = NumberGuessingGame(root)
    root.mainloop()