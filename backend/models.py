import sqlite3

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    # Create a table to track each user's current challenge
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            current_challenge INTEGER DEFAULT 1
        )
    ''')

    # Create a table to store challenges and their answers
    c.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Insert your actual challenges if none exist yet
    c.execute('SELECT COUNT(*) FROM challenges')
    if c.fetchone()[0] == 0:
        challenges = [
            (1, "Operations, All Calls, hellos and goodbyes, often happen here, in the heart of the squadron", "Insert number hidden at crew desk"),
            (2, "Congrats! navigage to [website], and find the flag", "Answer"),
            (3, "Cloud team?", "6")
        ]
        c.executemany('INSERT INTO challenges VALUES (?, ?, ?)', challenges)
        conn.commit()

    conn.close()

# Fetch the current progress of a user
def get_user_progress(username):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    # Check if user exists
    c.execute('SELECT current_challenge FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    if row:
        current = row[0]
    else:
        # If not, add them with default progress (challenge 1)
        current = 1
        c.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()

    conn.close()
    return {"username": username, "current": current}

# Get the next challenge for the user based on their progress
def get_next_challenge(username):
    progress = get_user_progress(username)
    current = progress['current']

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute('SELECT id, question FROM challenges WHERE id = ?', (current,))
    row = c.fetchone()
    conn.close()

    # If a challenge exists, return it
    if row:
        return {"id": row[0], "question": row[1]}
    else:
        return {"message": "No more challenges!"}

# Validate the submitted answer and update progress if correct
def submit_answer(username, flag):
    progress = get_user_progress(username)
    current = progress['current']

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    # Get correct answer for current challenge
    c.execute('SELECT answer FROM challenges WHERE id = ?', (current,))
    correct = c.fetchone()[0]

    # Compare answers (case insensitive)
    if flag.strip().lower() == correct.lower():
        # Move to the next challenge
        c.execute('UPDATE users SET current_challenge = current_challenge + 1 WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        return {"correct": True}
    else:
        conn.close()
        return {"correct": False}
