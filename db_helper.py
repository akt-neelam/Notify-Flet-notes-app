import sqlite3
import os
from datetime import datetime

# DATABASE FILE SETUP
# This gets the directory where db_helper.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create full path to database file
DB_PATH = os.path.join(BASE_DIR, 'notes.db')


def init_database():
    """
    Initialize the database and create tables if they don't exist
    Called once when the first starts
    
    WHAT IT DOES:
    - Creates notes.db file (if doesn't exist)
    - Creates 'notes' table with columns
    - Sets up soft-delete system (is_deleted flag instead of permanent delete)
    """

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # CREATE TABLE - This table holds all notes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_deleted INTEGER DEFAULT 0
        )
    ''')

    # SAVE changes to database
    conn.commit()
    # CLOSE connection
    conn.close()

    print("Database initialized successfully!")


def add_note(title, content):
    """
    Add a NEW note to the database
    
    RETURNS:
    - int: ID of created notes (to reference note later)
    - None: If there's an error
    
    WORKING FLOW:
    - Takes title & content from user
    - Inserts into database with current timestamp
    - Returns the ID so we know which note was created
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # INSERT new note to database
        cursor.execute('''
            INSERT INTO notes (title, content, created_date, modified_date)
            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (title, content))

        # Get the ID of the note just created
        # lastrowid = the ID flet assigned to this row
        note_id = cursor.lastrowid

        conn.commit()
        conn.close()

        print(f"Note {note_id} created!")
        return note_id
    
    except Exception as e:
        print(f"Error adding note: {e}")
        return None
    

def get_all_notes():
    """
    Get ALL active notes (not deleted)
    
    RETURNS:
    - List of tuples: [(id, title, content....)]
    - Empty list: [] if no notes or error
    
    WORKING FLOW:
    - Queries database for all notes where notes is_deleted = 0
    - ORDER BY modified_date DESC = newest notes first
    - USed for Home Page to display list of all notes
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SELECT all notes where is_deleted = 0 (not in trash)
        # ORDER BY modified_date DESC = newest first
        cursor.execute('''
            SELECT id, title, content, created_date, modified_date
            FROM notes
            WHERE is_deleted = 0
            ORDER BY modified_date DESC
        ''')

        # fetchall() gets ALL matching rows as a list of tuples
        notes = cursor.fetchall()
        conn.close()

        return notes
    
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return []
    

def get_note_by_id(note_id):
    """
    Get ONE specific note by its ID
    Used when user clicks on a note to view it
    
    RETURNS:
    - Tuple: (id, title, content....)
    - None: If note doesn't exist or error
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SELECT single note by ID
        # fetchone() returns just one row (or None if not found)
        cursor.execute('''
            SELECT id, title, content, created_date, modified_date
            FROM notes
            WHERE id = ? AND is_deleted = 0
        ''', (note_id))

        note = cursor.fetchone()
        conn.close()

        return note
    
    except Exception as e:
        print(f"Error fetching note: {e}")
        return None
    

def search_notes(query):
    """
    SEARCH notes by both TITLE and CONTENT
    Case-insensitive
    
    RETURNS:
    - List of matching notes
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SEARCH - Case insensitive in BOTH title & content
        cursor.execute('''
            SELECT id, title, content, created_date, modified_date
            FROM notes
            WHERE is_deleted = 0 AND (
                LOWER(title) LIKE LOWER(?)
            )
            ORDER BY modified_date DESC
        ''', (f'%{query}%', f'%{query}%'))

        results = cursor.fetchall()
        conn.close()

        return results
    
    except Exception as e:
        print(f"Error searching notes: {e}")
        return []
    

def update_note(note_id, title, content):
    """
    UPDATE an existing note's title and content
    Used when user edits a note
    
    RETURNS:
    - True: If successful
    - False: If error
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # UPDATE note and automatically set modified_date to NOW
        cursor.execute('''
            UPDATE notes
            SET title = ?, content = ?, modified_date = CURRENT_TIMESTAMP
            WHERE id = ? AND is_deleted = 0
        ''', (title, content, note_id))

        conn.commit()
        conn.close()

        print(f"Note {note_id} updated!")
        return True
    
    except Exception as e:
        print(f"Error updating note: {e}")
        return False
    

def soft_delete_note(note_id):
    """
    SOFT DELETE a note (marks as deleted, don't actually remove)
    This allows recovery from trash later.
    
    RETURNS:
    - True: If successful
    - False: If error
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SET is_deleted = 1 (marks as deleted, but doesn't remove)
        cursor.execute('''
            UPDATE notes
            SET is_deleted = 1
            WHERE id = ?
        ''', (note_id))

        conn.commit()
        conn.close()

        print(f"Note {note_id} moved to trash!")
        return True
    
    except Exception as e:
        print(f"Error deleting note: {e}")
        return False
    

def get_trash_notes():
    """
    Get all DELETED notes (notes in trash)
    
    RETURNS:
    - List of deleted notes
    - Empty list if trash is empty
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SELECT WHERE is_deleted = 1 (get deleted notes)
        cursor.execute('''
            SELECT id, title, content, created_date, modified_date
            FROM notes
            WHERE is_deleted = 1
            ORDER BY modified_date DESC
        ''')

        trash = cursor.fetchall()
        conn.close()

        return trash
    
    except Exception as e:
        print(f"Error fetching trash: {e}")
        return []
    

def restore_note(note_id):
    """
    Restore a note from trash
    
    RETURNS:
    - True: If successful
    - False: If error
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Set is_deleted = 0 (marks as active again)
        cursor.execute('''
            UPDATE notes
            SET is_deleted = 0
            WHERE id = ?
        ''', (note_id,))

        conn.commit()
        conn.close()

        print(f"Note {note_id} restored!")
        return True
    
    except Exception as e:
        print(f"Error restoring note: {e}")
        return False
    

def permenantly_delete_note(note_id):
    """
    Permenanty delete a note from database
    CANNOT be recovered after this!
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # DELETE - permenantly removes row from database
        cursor.execute('''
            DELETE FROM notes
            WHERE id = ?
        ''', (note_id,))

        conn.commit()
        conn.close()

        print(f"Note {note_id} permenantly deleted!")
        return True
    
    except Exception as e:
        print(f"Error permenantly deleting: {e}")
        return False