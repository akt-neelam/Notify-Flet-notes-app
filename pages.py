import flet as ft
from db_helper import add_note, get_note_by_id, update_note, soft_delete_note
import sqlite3

# MARKDOWN SYNTAX HELPERS
# These functions wrap text with markdown syntax

def make_bold(text):
    return f"**{text}**"

def make_italic(text):
    return f"*{text}*"

def make_underline(text):
    return f"__{text}__"

def make_heading(level, text):
    return f"{'#' * level} {text}\n"

def make_bullet(text):
    return f"-{text}\n"

def make_numbered(text):
    return f"1. {text}\n"

def make_divider():
    return "---\n"


class CreateNotePage:
    """
    Page for creating a NEW note
    User enters title + content with markdown formatting
    """

    def __init__(self, page, on_note_saved):
        """
        Initialize the create note page
        
        PARAMETER:
        - on_note_saved; Callback function when note is saved
        """

        self.page = page
        self.on_note_saved = on_note_saved
        self.note_id = None # For edit mode (will be set if editing existing note)

    def get_selected_text(self, text_field):
        """
        Get selected text from a TextField
        """

        return ""
    
    def insert_markdown(self, content_field, markdown_text):
        """
        Insert markdown syntax into content field
        """

        # Get current content
        current = content_field.value

        # Append markdown
        content_field.value += markdown_text
        content_field.update()

    def build(self, note_data=None):
        """
        Build the create/edit note page UI
        
        - note_data; If provided, we're in edit mode (id, title, content,...)
        """

        is_edit_mode = note_data is not None
        if is_edit_mode:
            self.note_id = note_data[0] # note_id
            initial_title = note_data[1] # title
            initial_content = note_data[2]
        else:
            initial_title = ""
            initial_content = ""
            
        