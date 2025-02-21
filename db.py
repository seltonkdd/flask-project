import sqlite3, hashlib, os

db_directory = 'database/'
if not os.path.exists(db_directory):
    os.mkdir(db_directory)


def create_database():
    conn = sqlite3.connect(os.path.join(db_directory + 'db_users.db'), check_same_thread=False)
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                bio TEXT,
                CONSTRAINT unique_email UNIQUE (email)
                  )''')
    conn.commit()
    conn.close()


def salvar_database(username, email, password, bio=''):
    hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('database/db_users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, password, bio) VALUES (?, ?, ?, ?)', (username, email, hash, bio))
    conn.commit()
    conn.close()


def update_database(id, username, email, password, bio=''):
    hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('database/db_users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE users SET username=?, email=?, password=?, bio=? WHERE id=?', (username, email, hash, bio, id))
    conn.commit()
    conn.close()

def get_database():
    conn = sqlite3.connect('database/db_users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_id(id):
    conn = sqlite3.connect('database/db_users.db', check_same_thread=False)
    c = conn.cursor()
    user = c.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    conn.close()
    return user

def delete_and_save(id):
    conn = sqlite3.connect('database/db_users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()
