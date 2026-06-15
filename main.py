import flet as ft
from db_helper import init_database, get_all_notes, search_notes

# Initialize database when app starts
init_database()

def main(page: ft.Page):
    """
    Main app function
    Sets up the home page with notes list, search and add button
    """

    page.title = "Notify"
    page.theme = ft.Theme(font_family="Times New Roman")
    page.window_width = 400
    page.window_height = 800
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    # STATE VARIABLES
    current_notes = [] # Stores the displayed notes

    # UI CONTROLS
    search_box = ft.TextField(
        label="Search Notes...",
        hint_text="Type to search",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: on_search_change(), # Trigger search on every keystroke
        width=300,
        height=50
    )

    # NOTES CONTAINER
    notes_container = ft.Column(
        controls=[],
        spacing=10,
        scroll="auto"
    )

    # EMPTY STATE - shown when no notes exist
    empty_state = ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    icon=ft.Icons.DESCRIPTION_OUTLINED,
                    size=80,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                ),
                ft.Text(
                    "No notes yet!",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_700,
                ),
                ft.Text(
                    "Tap the + button to create your first note",
                    size=14,
                    color=ft.Colors.GREY_400,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    # MAIN CONTENT - switches between empty state and notes list
    content_area = ft.Container(
        content=empty_state,
        expand=True
    )

    # EVENT HANDLERS
    def on_search_change():
        """
        Called when user types in search box
        Searches notes by title and content
        """

        query = search_box.value.strip()

        if query == "":
            # Empty search - show all notes
            current_notes.clear()
            current_notes.extend(get_all_notes())

        else:
            # Search query - find matching notes
            current_notes.clear()
            current_notes.extend(search_notes(query))

        # Rebuild the notes display
        rebuild_notes_list()

    
    def rebuild_notes_list():
        """
        Rebuild the notes list on screen
        Show notes as clickable buttons
        """

        notes_container.controls.clear()

        if not current_notes:
            # No notes - show empty state
            content_area.content = empty_state
            page.update()
            return
        
        # CREATE A BUTTON FOR each note
        for note_id, title, content, created_date, modified_date in current_notes:
            # NOTE PREVIEW - show first 50 chars of content
            preview = content[:100] + "..." if len(content) > 100 else content
            preview = preview.replace("\n", " ") # Remove line breaks for preview

            # CREATE NOTE CARD (as a clickable button)
            note_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            # Title
                            ft.Text(
                                title,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            # Preview
                            ft.Text(
                                preview,
                                size=12,
                                color=ft.Colors.GREY_700,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            # Date
                            ft.Text(
                                f"Modified: {modified_date}",
                                size=10,
                                color=ft.Colors.GREY_600,
                                italic=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=15,
                    on_click=lambda _, nid=note_id: on_note_click(nid), # Make card clickable
                ),
            )

            notes_container.controls.append(note_card)

        # Show notes list instead of empty state
        content_area.content = notes_container
        page.update()

    
    def on_note_click(note_id):
        """
        Called when user clicks on a note
        Navigate to the view/edit page
        """

        print(f"Clicked note {note_id}")
        # TODO: Navigate to create note view page


    async def on_add_button_click(e):
        """
        Called when user clicks the + (FloatingActionButton)
        Navigate to create note page
        """

        print("Create new note")
        # TODO: Navigate to create note page


    # Page Layout
    page.add(
        ft.Column(
            [
                # HEADER
                ft.Container(
                    content=ft.Text(
                        "Notes",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    padding=ft.Padding.only(left=10, right=10, bottom=15),
                ),

                # SEARCH BOX
                ft.Container(
                    content=search_box,
                    padding=ft.Padding.only(left=10, right=10, bottom=15),
                ),

                # NOTES LIST / EMPTY STATE
                content_area,
            ],
            expand=True,
            spacing=0,
        ),
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=on_add_button_click,
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_600),
        foreground_color=ft.Colors.WHITE,
    )

    # INITIALIZATION
    # Load all notes on app start
    current_notes.extend(get_all_notes())
    rebuild_notes_list()

ft.run(main)
