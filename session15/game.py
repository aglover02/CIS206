"""
Simple Rock, Paper, Scissors Game (GUI)

- The player chooses Rock, Paper, or Scissors by clicking a button.
- The computer randomly chooses Rock, Paper, or Scissors.
- The program compares the choices and displays whether the player wins,
  loses, or ties.
- A simple graphic (a face) on a Canvas shows the result:
    * Green happy face for WIN
    * Red sad face for LOSS
    * Blue neutral face for TIE
- The user can play repeatedly by clicking the buttons again.
"""

import tkinter as tk
import random


class RPSGame:
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the main window, widgets, and layout."""
        self.root = root
        self.root.title("Rock, Paper, Scissors Game")

        # Instructions label (guides the user)
        self.instructions_label = tk.Label(
            self.root,
            text="Choose Rock, Paper, or Scissors to play against the computer."
        )
        self.instructions_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # Buttons for user choices (repeated interaction)
        self.rock_button = tk.Button(
            self.root,
            text="Rock",
            width=10,
            command=lambda: self.play_round("Rock")
        )
        self.paper_button = tk.Button(
            self.root,
            text="Paper",
            width=10,
            command=lambda: self.play_round("Paper")
        )
        self.scissors_button = tk.Button(
            self.root,
            text="Scissors",
            width=10,
            command=lambda: self.play_round("Scissors")
        )

        self.rock_button.grid(row=1, column=0, padx=5, pady=5)
        self.paper_button.grid(row=1, column=1, padx=5, pady=5)
        self.scissors_button.grid(row=1, column=2, padx=5, pady=5)

        # Labels to show choices and result text 
        self.player_choice_label = tk.Label(self.root, text="Your choice: ")
        self.computer_choice_label = tk.Label(self.root, text="Computer's choice: ")
        self.result_label = tk.Label(self.root, text="Result: ", font=("Arial", 12, "bold"))

        self.player_choice_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        self.computer_choice_label.grid(row=3, column=0, columnspan=3)
        self.result_label.grid(row=4, column=0, columnspan=3, pady=(5, 10))

        # Canvas for simple graphics (face changes with result)
        self.canvas = tk.Canvas(self.root, width=120, height=120, bg="white")
        self.canvas.grid(row=5, column=0, columnspan=3, pady=(5, 10))

        # Draw an initial neutral face
        self.draw_face("tie")

    def play_round(self, player_choice: str) -> None:
        """Handle one round of the game when the user clicks a button."""
        options = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(options)

        # Display choices
        self.player_choice_label.config(text=f"Your choice: {player_choice}")
        self.computer_choice_label.config(text=f"Computer's choice: {computer_choice}")

        # Determine outcome
        result = self.determine_winner(player_choice, computer_choice)

        # Update result label and graphic
        if result == "win":
            self.result_label.config(text="Result: You WIN!", fg="green")
        elif result == "lose":
            self.result_label.config(text="Result: You LOSE!", fg="red")
        else:
            self.result_label.config(text="Result: It's a TIE!", fg="blue")

        self.draw_face(result)

    def determine_winner(self, player: str, computer: str) -> str:
        """Return 'win', 'lose', or 'tie' based on standard RPS rules."""
        if player == computer:
            return "tie"

        # Winning combinations for the player
        wins = {
            ("Rock", "Scissors"),
            ("Paper", "Rock"),
            ("Scissors", "Paper")
        }

        if (player, computer) in wins:
            return "win"
        else:
            return "lose"

    def draw_face(self, result: str) -> None:
        """
        Draw a simple face on the canvas:
        - Green happy face for win
        - Red sad face for lose
        - Blue neutral face for tie
        """
        self.canvas.delete("all")  # Clear previous drawing

        # Choose color and mouth shape based on result
        if result == "win":
            outline_color = "green"
            mouth_start = 40
            mouth_end = 80
            mouth_top = 70
            mouth_bottom = 90  # smile (arc)
            style = tk.ARC
        elif result == "lose":
            outline_color = "red"
            mouth_start = 40
            mouth_end = 80
            # frown higher on the face
            mouth_top = 60
            mouth_bottom = 80  # frown (arc)
            style = tk.ARC
        else:  # tie
            outline_color = "blue"
            mouth_start = 40
            mouth_end = 80
            mouth_top = 80
            mouth_bottom = 80  # straight line for neutral
            style = tk.PIESLICE  # straight line (drawn as thin slice)

        # Face (circle)
        self.canvas.create_oval(20, 20, 100, 100, outline=outline_color, width=3)

        # Eyes
        self.canvas.create_oval(40, 45, 50, 55, fill=outline_color)
        self.canvas.create_oval(70, 45, 80, 55, fill=outline_color)

        # Mouth
        if result == "tie":
            # Draw straight line mouth
            self.canvas.create_line(40, 80, 80, 80, fill=outline_color, width=3)
        else:
            # Draw arc for smile or frown
            if result == "win":
                start_angle = 0
                extent_angle = -180   # bottom half → smile
            else:  # lose
                start_angle = 0
                extent_angle = 180    # top half → frown

            self.canvas.create_arc(
                mouth_start,
                mouth_top,
                mouth_end,
                mouth_bottom,
                start=start_angle,
                extent=extent_angle,
                style=style,
                outline=outline_color,
                width=3
            )

if __name__ == "__main__":
    root_window = tk.Tk()
    app = RPSGame(root_window)
    root_window.mainloop()
