import flet as ft
import matplotlib.pyplot as plt
import networkx as nx


def main(page: ft.Page):
    page.title = "Club de tenis"
    page.theme_mode = ft.ThemeMode.DARK

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )

    titulo = ft.Text("Tenis")

    app_bar = ft.AppBar(
        title=titulo,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_icon_button],
    )


    search_field = ft.TextField(label="Buscar por título, autor, género o año", width=300, on_change=lambda e: search_books())
    clear_search_button = ft.ElevatedButton("Limpiar Filtro", on_click=lambda _: clear_search())
    

    sort_button = ft.PopupMenuButton(
        icon=ft.icons.SORT,
        items=[
            ft.PopupMenuItem(text="Título", on_click=lambda _: sort_books("title")),
            ft.PopupMenuItem(text="Autor", on_click=lambda _: sort_books("author")),
            ft.PopupMenuItem(text="Género", on_click=lambda _: sort_books("genre")),
            ft.PopupMenuItem(text="Año", on_click=lambda _: sort_books("year")),
        ],
        
    )


    all_books = []

    def search_books():
        search_text = search_field.value.lower()
        books_view.controls.clear()
        for book in all_books:
            if (search_text in book["title"].lower() or
                search_text in book["author"].lower() or
                search_text in book["genre"].lower() or
                search_text in book["year"].lower()):
                books_view.controls.append(book["display"])
        page.update()

    def clear_search():
        search_field.value = ""
        books_view.controls.clear()
        books_view.controls.extend([book["display"] for book in all_books])
        page.update()


    def add_book(e):
        if not title_field.value:
            title_field.error_text = "Por favor ingrese un título"
            page.update()
            return
        
         # Validar el campo de año solo si se ha ingresado un valor
        if year_field.value and not year_field.value.isdigit():
            year_field.error_text = "Por favor ingrese un año válido (número entero)"
            page.update()
            return  
        else:
            year_field.error_text = None
        page.update()
        
        new_book_data = {
            "title": title_field.value,
            "author": author_field.value if author_field.value else 'Desconocido',
            "genre": genero_field.value if genero_field.value else 'Sin género',
            "year": year_field.value if year_field.value else 'Sin reporte',
            "image": image_state["path"]
        }

        image_container = ft.Container(
            ft.Image(src=image_state["path"], fit=ft.ImageFit.COVER),
            width=100,
            height=150,
        ) if image_state["path"] else None

        



    title_field = ft.TextField(label="Título del libro", width=300)
    author_field = ft.TextField(label="Autor", width=300)
    genero_field = ft.TextField(label="Género", width=300)
    year_field = ft.TextField(label="Año de Publicación", width=300)
    add_button = ft.ElevatedButton("Añadir libro", on_click=add_book)
    upload_image_button = ft.ElevatedButton("Subir imagen", on_click=lambda _: image_picker.pick_files(allow_multiple=False))


    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index == 0:
            content.controls.append(ft.Column([search_field, clear_search_button, sort_button, books_view], spacing=10))
        elif index == 1:
            content.controls.append(add_book_view)
        elif index == 2:
            content.controls.append(loans_view)
        elif index == 3:
            content.controls.append(add_visual_view)
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.BOOK, label="Inscripción"),
            ft.NavigationRailDestination(icon=ft.icons.ADD, label="Matrícula"),
            ft.NavigationRailDestination(icon=ft.icons.LIBRARY_BOOKS, label="Seguimiento"),
            ft.NavigationRailDestination(icon=ft.icons.REMOVE_RED_EYE_ROUNDED, label="Informes"),
        ],
        on_change=destination_change,
    )

    content = ft.Column(
        [search_field, clear_search_button, sort_button, books_view],
        spacing=10,
        expand=True
    )

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)