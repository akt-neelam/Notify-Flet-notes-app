import flet as ft
from db_helper import init_database, get_all_notes, search_notes, get_note_by_id, add_note, update_note, soft_delete_note, get_trash_notes, restore_note, permenantly_delete_note

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
    current_search = ""
    current_note_id = None


    # HELPER FUNCTIONS

    def get_notes_display():
        """Get notes to display (all or filtered by search)"""
        if current_search.strip() == "":
            return get_all_notes()
        else:
            return search_notes(current_search)
        
    
    # ===== PAGE: HOME PAGE =====

    def build_home_page():
        """Build the home page with notes list"""
        notes_list = get_notes_display()

        # Search box
        search_box = ft.TextField(
            label="Search notes...",
            hint_text="Type to search",
            prefix_icon=ft.Icons.SEARCH,
            on_change=lambda e: on_search_change(e),
            width=300,
            height=50,
            text_style=ft.TextStyle(font_family="Times New Roman", size=14),
        )

        # Notes Container
        notes_column = ft.Column(
            spacing=10,
            scroll="auto",
        )

        # Build note cards
        for note_id, title, content, created_date, modified_date in notes_list:
            preview = content[:100] + "..." if len(content) > 100 else content
            preview = preview.replace("\n", " ")

            note_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                title, 
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Text(
                                preview,
                                size=12,
                                color=ft.Colors.GREY_700,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
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
                    on_click=lambda _, nid=note_id: go_to_view(nid),
                ),
            )
            notes_column.controls.append(note_card)

        # Empty State
        if not notes_list:
            empty_state = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            icon=ft.Icons.DESCRIPTION_OUTLINED,
                            size=80,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                        ),
                        ft.Text(
                            "No notes yet",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Text(
                            "Tap the + button to create your first note",
                            size=14,
                            color=ft.Colors.GREY_600,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )

            return ft.View(
                route="/",
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Notes",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                        ),
                        padding=ft.Padding.only(left=20, top=20, bottom=10),
                    ),
                    ft.Container(
                        content=search_box,
                        padding=ft.Padding.only(left=10, right=10, bottom=15),
                    ),
                    empty_state,
                ],
            )
        
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Notes",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    padding=ft.Padding.only(left=20, top=20, bottom=10),
                ),
                ft.Container(
                    content=search_box,
                    padding=ft.Padding.only(left=10, right=10, bottom=15),
                ),
                ft.Container(
                    content=notes_column,
                    expand=True,
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                ),
            ],
        )
    

    # ===== PAGE: CREATE NOTE PAGE =====

    def build_create_page():
        """Build the create note page with markdown toolbar"""

        title_field = ft.TextField(
            label="Note Title",
            hint_text="Enter note title",
            width=300,
            height=50,
            text_style=ft.TextStyle(font_family="Times NEw Roman", size=14),
        )

        content_field = ft.TextField(
            label="Note Content",
            hint_text="Start typing your note...",
            multiline=True,
            width=300,
            height=300,
            min_lines=10,
            text_style=ft.TextStyle(font_family="Times New Roman", size=14),
        )

        # Toolbar Buttons

            
