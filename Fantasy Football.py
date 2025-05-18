import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root123'
)

cursor = conn.cursor()

# Set up database and tables

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS fantasy_football")
conn.database = 'fantasy_football'

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    name VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_teams (
    user_id INT,
    player_id INT,
    PRIMARY KEY (user_id, player_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_stats (
    match_id INT,
    player_id INT,
    goals INT,
    assists INT,
    points INT,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_points (
    user_id INT PRIMARY KEY,
    total_points INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Add players
cursor.executemany("""
INSERT IGNORE INTO players (player_id, name) VALUES (%s, %s)
""", [
    (101, 'Lamine Yamal'),
    (102, 'Erling Haaland'),
    (103, 'Kylian Mbappe'),
    (104, 'De Bruyne'),
    (105, 'Pedri'),
    (106, 'Raphinha'),
    (107, 'Dani Olmo'),
    (108, 'Jamal Musiala'),
    (109, 'Harry Kane'),
    (110, 'Lionel Messi')
])
conn.commit()

# Insert player stats
cursor.executemany("""
INSERT INTO player_stats (match_id, player_id, goals, assists, points)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
goals = VALUES(goals),
assists = VALUES(assists),
points = VALUES(points)
""", [
    (1, 101, 1, 1, 10),
    (1, 102, 2, 0, 8),
    (1, 103, 0, 2, 4),
    (1, 104, 0, 1, 2),
    (1, 105, 1, 2, 12),
    (1, 106, 3, 1, 20),
    (1, 107, 1, 1, 10),
    (1, 108, 0, 1, 2),
    (1, 109, 1, 1, 8),
    (1, 110, 3, 3, 30),
])
conn.commit()


def calculate_user_points(user_id, match_id):
    total_points = 0
    cursor.execute("SELECT player_id FROM user_teams WHERE user_id = %s", (user_id,))
    player_ids = cursor.fetchall()

    for (player_id,) in player_ids:
        cursor.execute("SELECT points FROM player_stats WHERE match_id = %s AND player_id = %s", (match_id, player_id))
        result = cursor.fetchone()
        if result:
            total_points += result[0]

    cursor.execute("""
    INSERT INTO user_points (user_id, total_points)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE total_points = %s
    """, (user_id, total_points, total_points))
    conn.commit()

# Tkinter 
root = tk.Tk()
root.title("Fantasy Football")


user_id = None


def handle_user():
    global user_id
    username = username_entry.get()
    
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        user_id = existing_user[0]
        messagebox.showinfo("Welcome", f"Welcome back, {username}!")
        # Clear previous selections
        player_listbox.selection_clear(0, tk.END)
    else:
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        user_id = cursor.lastrowid
        messagebox.showinfo("New User", f"New user created: {username}")

def select_players():
    if user_id is None:
        messagebox.showwarning("User Not Found", "Please create or log in to a user first.")
        return

    selected_players = player_listbox.curselection()
    if len(selected_players) != 5:
        messagebox.showwarning("Invalid Selection", "You must select exactly 5 players.")
        return

    selected_player_ids = [player_listbox.get(i).split(':')[0] for i in selected_players]

    for player_id in selected_player_ids:
        cursor.execute("INSERT INTO user_teams (user_id, player_id) VALUES (%s, %s)", (user_id, int(player_id)))
    conn.commit()
    
    calculate_user_points(user_id, match_id=1)
    messagebox.showinfo("Team Updated", "Your team has been updated!")


def show_leaderboard():
    cursor.execute("""
    SELECT u.username, up.total_points
    FROM users u
    JOIN user_points up ON u.user_id = up.user_id
    ORDER BY up.total_points DESC
    """)
    
    leaderboard = cursor.fetchall()
    
    leaderboard_text = "⚽ Weekly Leaderboard (Match 1):\n\nRank  Username       Points\n"
    leaderboard_text += "-" * 40 + "\n"
    for rank, (name, points) in enumerate(leaderboard, 1):
        leaderboard_text += f"{rank:<6}{name:<15}{points:<7}\n"
    
    messagebox.showinfo("Leaderboard", leaderboard_text)


username_label = tk.Label(root, text="Enter your username:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

login_button = tk.Button(root, text="Log in or Create User", command=handle_user)
login_button.pack()

player_listbox_label = tk.Label(root, text="Available Players (select 5):")
player_listbox_label.pack()

player_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
cursor.execute("SELECT player_id, name FROM players")
players = cursor.fetchall()

for player in players:
    player_listbox.insert(tk.END, f"{player[0]}: {player[1]}")

player_listbox.pack()

select_players_button = tk.Button(root, text="Select Players", command=select_players)
select_players_button.pack()

leaderboard_button = tk.Button(root, text="Show Leaderboard", command=show_leaderboard)
leaderboard_button.pack()


root.mainloop()


cursor.close()
conn.close()
