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
    page.window_bgcolor = ft.Colors.WHITE

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

        # TOOLBAR BUTTON HANDLERS

        def on_bold_click(e):
            """Add bold markdown"""
            content_field.value += "**bold text**"
            content_field.update()
    
        def on_italic_click(e):
            """Add italic markdown"""
            content_field.value += "*italic text*"
            content_field.update()
        
        def on_underline_click(e):
            """Add underline markdown"""
            content_field.value += "__underlined text__"
            content_field.update()
        
        def on_h1_click(e):
            """Add H1 heading"""
            content_field.value += "\n# Heading 1\n"
            content_field.update()
        
        def on_h2_click(e):
            """Add H2 heading"""
            content_field.value += "\n## Heading 2\n"
            content_field.update()
        
        def on_h3_click(e):
            """Add H3 heading"""
            content_field.value += "\n### Heading 3\n"
            content_field.update()
        
        def on_bullet_click(e):
            """Add bullet point"""
            content_field.value += "\n- Bullet point\n"
            content_field.update()
        
        def on_number_click(e):
            """Add numbered item"""
            content_field.value += "\n1. Numbered item\n"
            content_field.update()
        
        def on_divider_click(e):
            """Add divider"""
            content_field.value += "\n---\n"
            content_field.update()

        # Toolbar Buttons
        toolbar_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.FORMAT_BOLD,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_600),
                    tooltip="Bold",
                    on_click=on_bold_click,
                ),
                ft.IconButton(
                    icon=ft.Icons.FORMAT_ITALIC,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_600),
                    tooltip="Italic",
                    on_click=on_italic_click
                ),
                ft.IconButton(
                    icon=ft.Icons.FORMAT_UNDERLINED,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_600),
                    tooltip="Underline",
                    on_click=on_underline_click
                ),
                ft.VerticalDivider(width=10),
                ft.IconButton(
                    icon=ft.Icons.TITLE,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.PURPLE_600),
                    tooltip="H1",
                    on_click=on_h1_click
                ),
                ft.IconButton(
                    icon=ft.Icons.TEXT_FIELDS,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.PURPLE_600),
                    tooltip="H2",
                    on_click=on_h2_click,
                ),
                ft.VerticalDivider(width=10),
                ft.IconButton(
                    icon=ft.Icons.FORMAT_LIST_BULLETED,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_600),
                    tooltip="Bullet",
                    on_click=on_bullet_click,
                ),
                ft.IconButton(
                    icon=ft.Icons.FORMAT_LIST_NUMBERED,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_600),
                    tooltip="Number",
                    on_click=on_number_click,
                ),
                ft.VerticalDivider(width=10),
                ft.IconButton(
                    icon=ft.Icons.HORIZONTAL_RULE,
                    icon_color=ft.Colors.with_opacity(0.7, ft.Colors.GREY_600),
                    tooltip="Divider",
                    on_click=on_divider_click
                ),
            ],
            scroll="auto",
            spacing=5,
        )

        async def on_save_click(e):
            """Save note"""
            title = title_field.value.strip()
            content = content_field.value.strip()

            if not title or not content:
                print("Title and content required!")
                return
            
            add_note(title, content)
            print("Note Saved!")
            await page.push_route("/")

        async def on_back_click(e):
            """go back to home"""
            await page.push_route("/")

        save_btn = ft.Button(
            "Save",
            on_click=on_save_click,
            width=180,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_600),
        )
        
        back_btn = ft.Button(
            "Back",
            on_click=on_back_click,
            width=180
        )

        return ft.View(
            route="/create",
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Create Note",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    padding=ft.Padding.only(left=20, top=20, bottom=10),
                ),
                ft.Container(
                    content=title_field,
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                    bgcolor=ft.Colors.WHITE
                ),
                ft.Container(
                    content=toolbar_buttons,
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                    border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
                    bgcolor=ft.Colors.WHITE
                ),
                ft.Container(
                    content=content_field,
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                    expand=True,
                    bgcolor=ft.Colors.WHITE
                ),
                ft.Container(
                    content=ft.Row([back_btn, save_btn], spacing=10),
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                ),
            ],
        )
    

    # ===== PAGE: VIEW NOTE PAGE =====

    def build_view_page(note_id):
        """build the view note page"""

        note_data = get_note_by_id(note_id)
        if not note_data:
            return ft.View(
                route=f"/view/{note_id}",
                controls=[ft.Text("Note note found!")],
            )
        
        note_id_db, title, content, created_data, modified_date = note_data

        async def on_edit_click(e):
            """Go to edit page"""
            await page.push_route(f"/edit.{note_id_db}")

        async def on_delete_click(e):
            """Delete note"""
            soft_delete_note(note_id_db)
            print(f"Note {note_id_db} deleted!")
            await page.push_route("/")

        async def on_back_click(e):
            """Go back to home"""
            await page.push_route("/")

        edit_btn = ft.Button(
            "Edit",
            on_click=on_edit_click,
            width=120,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_600),
        )

        delete_btn = ft.Button(
            "Delete",
            on_click=on_delete_click,
            width=120,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.RED_600),
        )

        back_btn = ft.Button(
            "Back",
            on_click=on_back_click,
            width=120,
        )

        return ft.View(
            route=f"/view/{note_id_db}",
            controls=[
                ft.Container(
                    content=ft.Text(
                        title,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    padding=ft.Padding.only(left=20, top=20, bottom=10),
                ),
                ft.Container(
                    content=ft.Text(
                        f"Modified: {modified_date}",
                        size=10,
                        color=ft.Colors.GREY_600,
                        italic=True,
                    ),
                    padding=ft.Padding.only(left=20, right=20, bottom=15),
                ),
                ft.Container(
                    content=ft.Markdown(
                        value=content,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    ),
                    padding=ft.Padding.only(left=20, right=20, bottom=20),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row([back_btn, delete_btn, edit_btn], spacing=10),
                    padding=ft.Padding.only(left=10, right=10, bottom=10),
                ),
            ],
        )
    

    # ====== ROUTE CHANGE HANDLER ======

    def route_change(route):
        """Handle route changes"""
        page.views.clear()

        # Home page
        page.views.append(build_home_page())

        # Create page
        if page.route == "/create":
            page.views.append(build_create_page())

        # View page
        elif page.route.startswith("/view/"):
            note_id = int(page.route.split("/")[-1])
            page.views.append(build_view_page(note_id))

        # Edit page (TODO - similar to create)
        elif page.route.startswith("/edit/"):
            note_id = int(page.route.split("/")[-1])
            # TODO: Build edit page
            page.views.append(build_create_page())

        async def on_add_button_click(e):
            """Handle add button click"""
            await page.push_route("/create")

        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=on_add_button_click,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_600),
            foreground_color=ft.Colors.WHITE,
        )

        page.update()

    async def go_to_view(note_id):
        """Navigate to view page"""
        await page.push_route(f"/view/{note_id}")

    async def on_search_change(e):
        """Handle search"""
        nonlocal current_search
        current_search = search_box.value
        page.on_route_change(page.route)

    
    # ==== SETUP =====

    page.on_route_change = route_change
    page.on_route_change(page.route)


ft.run(main)

