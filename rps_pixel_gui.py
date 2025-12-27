import tkinter as tk
import random

# ---------------- CONSTANTS ----------------
MAX_ROUNDS = 100

# ---------------- GAME STATE ----------------
choices = ["rock", "paper", "scissors"]
user_score = 0
cpu_score = 0
rounds_played = 0
game_mode = "unlimited"  # or "100"
leaderboard = []

# ---------------- GAME LOGIC ----------------
def play(user_choice):
    global user_score, cpu_score, rounds_played

    cpu_choice = random.choice(choices)
    rounds_played += 1

    you_choice.config(text=f"YOU: {icon(user_choice)}")
    cpu_choice_lbl.config(text=f"CPU: {icon(cpu_choice)}")

    if user_choice == cpu_choice:
        result.config(text="TIE!")
    elif (
        (user_choice == "rock" and cpu_choice == "scissors") or
        (user_choice == "paper" and cpu_choice == "rock") or
        (user_choice == "scissors" and cpu_choice == "paper")
    ):
        user_score += 1
        result.config(text="YOU WIN!")
    else:
        cpu_score += 1
        result.config(text="CPU WINS!")

    score.config(text=f"SCORE  YOU {user_score}  |  CPU {cpu_score}")
    rounds_label.config(text=f"ROUNDS: {rounds_played}")

    if game_mode == "100" and rounds_played >= MAX_ROUNDS:
        end_game(auto=True)

# ---------------- END GAME ----------------
def end_game(auto=False):
    global user_score, cpu_score, rounds_played

    name = name_entry.get().strip()
    if not name:
        name = "Player"

    leaderboard.append((name, user_score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    del leaderboard[7:]

    update_leaderboard()

    result.config(
        text="GAME OVER!" if auto else "SCORE SAVED!"
    )

    reset_game()

# ---------------- RESET / REPLAY ----------------
def reset_game():
    global user_score, cpu_score, rounds_played
    user_score = 0
    cpu_score = 0
    rounds_played = 0

    score.config(text="SCORE  YOU 0  |  CPU 0")
    rounds_label.config(text="ROUNDS: 0")
    you_choice.config(text="YOU:")
    cpu_choice_lbl.config(text="CPU:")

# ---------------- MODE SELECTION ----------------
def set_mode(mode):
    global game_mode
    game_mode = mode
    reset_game()
    result.config(
        text="UNLIMITED MODE!" if mode == "unlimited" else "100 ROUND CHALLENGE!"
    )

# ---------------- LEADERBOARD ----------------
def update_leaderboard():
    text = "🏆 HIGH SCORES 🏆\n"
    for i, (name, score_val) in enumerate(leaderboard, start=1):
        text += f"{i}. {name} — {score_val}\n"
    leaderboard_label.config(text=text)

# ---------------- ICONS ----------------
def icon(choice):
    return {"rock": "🪨", "paper": "📄", "scissors": "✂️"}[choice]

# ---------------- WINDOW ----------------
win = tk.Tk()
win.title("Rock Paper Scissors Arcade")
win.geometry("560x700")
win.configure(bg="#8fd3ff")

# ---------------- CANVAS ----------------
canvas = tk.Canvas(win, width=560, height=180, bg="#8fd3ff", highlightthickness=0)
canvas.pack()

def pixel_cloud(x, y):
    for bx, by in [(0,20),(20,20),(40,20),(60,20),(20,0),(40,0),(80,20),(100,20)]:
        canvas.create_rectangle(x+bx, y+by, x+bx+20, y+by+20, fill="white", outline="")

pixel_cloud(60, 80)
pixel_cloud(360, 60)

canvas.create_text(280, 50, text="ROCK PAPER SCISSORS",
                   font=("Courier New", 24, "bold"), fill="#1d3557")

# ---------------- MODE BUTTONS ----------------
mode_frame = tk.Frame(win, bg="#8fd3ff")
mode_frame.pack(pady=4)

tk.Button(mode_frame, text="UNLIMITED MODE",
          font=("Courier New", 11, "bold"),
          bg="#caffbf",
          command=lambda: set_mode("unlimited")).grid(row=0, column=0, padx=4)

tk.Button(mode_frame, text="100 ROUND CHALLENGE",
          font=("Courier New", 11, "bold"),
          bg="#ffd6a5",
          command=lambda: set_mode("100")).grid(row=0, column=1, padx=4)

# ---------------- GAME BUTTONS ----------------
panel = tk.Frame(win, bg="#8fd3ff")
panel.pack(pady=8)

def game_button(text, choice, color):
    return tk.Button(panel, text=text,
                     font=("Courier New", 12, "bold"),
                     width=10, height=2,
                     bg=color, bd=4,
                     command=lambda: play(choice))

game_button("🪨 ROCK", "rock", "#ffd6a5").grid(row=0, column=0, padx=6)
game_button("📄 PAPER", "paper", "#fdffb6").grid(row=0, column=1, padx=6)
game_button("✂️ SCISSORS", "scissors", "#caffbf").grid(row=0, column=2, padx=6)

# ---------------- STATUS ----------------
you_choice = tk.Label(win, text="YOU:", font=("Courier New", 14, "bold"), bg="#8fd3ff")
you_choice.pack()

cpu_choice_lbl = tk.Label(win, text="CPU:", font=("Courier New", 14, "bold"), bg="#8fd3ff")
cpu_choice_lbl.pack()

result = tk.Label(win, text="CHOOSE A MODE!",
                  font=("Courier New", 18, "bold"),
                  bg="#8fd3ff", fg="#e63946")
result.pack(pady=6)

score = tk.Label(win, text="SCORE  YOU 0  |  CPU 0",
                 font=("Courier New", 14, "bold"), bg="#8fd3ff")
score.pack()

rounds_label = tk.Label(win, text="ROUNDS: 0",
                        font=("Courier New", 12, "bold"), bg="#8fd3ff")
rounds_label.pack(pady=2)

# ---------------- NAME + CONTROLS ----------------
name_frame = tk.Frame(win, bg="#8fd3ff")
name_frame.pack(pady=6)

tk.Label(name_frame, text="Player Name:",
         font=("Courier New", 12), bg="#8fd3ff").grid(row=0, column=0, padx=4)

name_entry = tk.Entry(name_frame, font=("Courier New", 12), width=12)
name_entry.grid(row=0, column=1)

tk.Button(win, text="END GAME & SAVE SCORE",
          font=("Courier New", 12, "bold"),
          bg="#ffd166",
          command=end_game).pack(pady=4)

tk.Button(win, text="REPLAY",
          font=("Courier New", 12, "bold"),
          bg="#bdb2ff",
          command=reset_game).pack(pady=2)

# ---------------- LEADERBOARD ----------------
leaderboard_label = tk.Label(win, text="🏆 HIGH SCORES 🏆",
                             font=("Courier New", 14, "bold"),
                             bg="#8fd3ff", justify="left")
leaderboard_label.pack(pady=8)

win.mainloop()
