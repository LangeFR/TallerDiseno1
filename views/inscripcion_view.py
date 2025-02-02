# tallerdiseno1/views/inscripcion_view.py

import flet as ft
from modelos.usuario import Usuario

def create_inscripcion_view(page, controller, validar_identificacion, validar_email, validar_apellidos, validar_nombre, validar_telefono, validar_edad):
    """
    Crea y retorna la vista de inscripción de miembros con la lógica interna de inscripción.
    
    Parámetros:
        page (ft.Page): La página principal.
        controller: El controlador del club.
        validar_identificacion, validar_email, validar_apellidos, validar_nombre, validar_telefono, validar_edad: Funciones de validación.
    
    Retorna:
        tuple: (inscripcion_view, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field)
    """
    
    nombre_field = ft.TextField(
        label="Nombre", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True
    )
    
    apellidos_field = ft.TextField(
        label="Apellidos", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_apellidos
    )
    
    edad_field = ft.TextField(
        label="Edad", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    id_field = ft.TextField(
        label="Número de identificación", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    correo_field = ft.TextField(
        label="Correo", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_email
    )
    
    telefono_field = ft.TextField(
        label="Teléfono", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # Función interna que se encargará de procesar la inscripción
    def inscribir_persona(e):
        # Validar campos vacíos
        if not nombre_field.value or not apellidos_field.value or not id_field.value or not correo_field.value:
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Advertencia"),
                content=ft.Text("Por favor, complete todos los campos."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: (setattr(dialog, "open", False), page.update()))
                ],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return

        # Validar edad (no puede ser mayor a 116 años)
        try:
            edad = int(edad_field.value)
            if not validar_edad(edad):
                page.snack_bar = ft.SnackBar(
                    ft.Text("La edad no puede ser mayor a 116 años", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED
                )
                page.snack_bar.open = True
                page.update()
                return
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Edad inválida", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Llamar a las funciones de validación para cada campo
        if not (validar_nombre(nombre_field) and validar_apellidos(apellidos_field) and 
                validar_email(correo_field) and validar_telefono(telefono_field) and 
                validar_identificacion(id_field)):
            page.snack_bar = ft.SnackBar(
                ft.Text("Corrija los errores en los campos", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validar número de identificación (entre 8 y 10 dígitos y numérico)
        if len(id_field.value) > 10 or len(id_field.value) < 8 or not id_field.value.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("La identificación debe ser numérica y tener entre 8 y 10 dígitos.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validar número de celular (de 8 a 12 dígitos y solo números)
        if len(telefono_field.value) < 8 or len(telefono_field.value) > 12 or not telefono_field.value.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("El número de celular debe tener entre 8 y 12 dígitos y solo contener números", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Verificar si ya existe una persona registrada con el mismo número de identificación
        if controller.existe_usuario(id_field.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("Ya existe una persona registrada con este número de identificación", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            id=Usuario.nuevo_id(),  # Genera un nuevo ID
            nombre=nombre_field.value,
            apellidos=apellidos_field.value,
            edad=edad,
            num_identificacion=id_field.value,
            correo=correo_field.value,
            telefono=telefono_field.value,
            estado="inscrito"  # Estado por defecto
        )

        controller.agregar_usuario(nuevo_usuario)

        # Limpiar los campos después de la inscripción
        nombre_field.value = ""
        apellidos_field.value = ""
        edad_field.value = ""
        id_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        
        page.snack_bar = ft.SnackBar(
            ft.Text("Usuario inscrito exitosamente", color=ft.colors.WHITE),
            bgcolor=ft.colors.GREEN
        )
        page.snack_bar.open = True
        page.update()

    inscribir_button = ft.ElevatedButton(
        "Inscribir",
        on_click=inscribir_persona,
        icon=ft.icons.PERSON_ADD,
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.WHITE,
    )
    
    inscripcion_view = ft.Column(
        [
            ft.Text("Inscripción de Miembros", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            nombre_field,
            apellidos_field,
            edad_field,
            id_field,
            correo_field,
            telefono_field,
            inscribir_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
    
    return inscripcion_view, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field
