# tallerdiseno1/views/pagos_view.py
import flet as ft
from modelos.base_model import BaseModel

def create_pagos_view(controller, page):
    """
    Crea y retorna la vista de gestión de pagos.

    Parámetros:
        controller: Controlador de la aplicación.
        page: Página de Flet para actualizar UI y mostrar SnackBars.

    Retorna:
        ft.Column: La vista de pagos como un objeto Column de Flet.
    """

    # Obtener el Dropdown de usuarios matriculados desde el controlador
    dropdown_usuarios = controller.dropdown_usuarios()

    # Crear dropdown de conceptos de pago
    dropdown_conceptos = ft.Dropdown(
        label="Concepto de Pago",
        options=[
            ft.dropdown.Option("Inscripción"),
            ft.dropdown.Option("Mensualidad"),
            ft.dropdown.Option("Otro"),
        ]
    )

    # Campo de fecha
    fecha_field = ft.TextField(label="Fecha", hint_text="YYYY-MM-DD")

    # Campo de cantidad
    cantidad_field = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)

    # Lista donde se mostrarán los pagos registrados
    pagos_list = ft.ListView(spacing=10, expand=True)

    # Función para mostrar mensajes con SnackBar
    def mostrar_snackbar(mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # Función para actualizar la lista de pagos en la UI
    def actualizar_vista_pagos():
        pagos = controller.cargar_pagos()
        pagos_list.controls.clear()
        for pago in pagos:
            pagos_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"ID Usuario: {pago['usuario_id']} - {pago['concepto']} - ${pago['cantidad']}"),
                    subtitle=ft.Text(f"Fecha: {pago['fecha']}"),
                    leading=ft.Icon(ft.icons.MONETIZATION_ON),
                )
            )
        page.update()

    # Función para registrar un pago
    def registrar_pago(e):
        usuario_nombre = dropdown_usuarios.value
        concepto = dropdown_conceptos.value
        fecha = fecha_field.value
        cantidad = cantidad_field.value

        if not (usuario_nombre and concepto and fecha and cantidad):
            mostrar_snackbar("Por favor, completa todos los campos.", "ERROR")
            return

        usuarios_matriculados_dict = controller.usuarios_matriculados_dict()

        if usuario_nombre in usuarios_matriculados_dict:
            usuario_id = usuarios_matriculados_dict[usuario_nombre]
            nuevo_pago = {
                "id": len(controller.cargar_pagos()) + 1,
                "usuario_id": usuario_id,
                "concepto": concepto,
                "fecha": fecha,
                "cantidad": float(cantidad),
            }

            # Guardar el nuevo pago en la base de datos
            pagos = controller.cargar_pagos()
            pagos.append(nuevo_pago)
            BaseModel.guardar_datos("pagos.json", pagos)

            # Actualizar estado del usuario si es un pago de inscripción
            if concepto == "Inscripción":
                controller.actualizar_estado_usuario(usuario_id, "matriculado")

            mostrar_snackbar("Pago registrado exitosamente.", "SUCCESS")
            actualizar_vista_pagos()
        else:
            mostrar_snackbar("Error: Usuario no encontrado.", "ERROR")

    # Botón para registrar pago
    registrar_button = ft.ElevatedButton(
        "Registrar Pago",
        icon=ft.icons.SAVE,
        on_click=registrar_pago
    )

    # Vista principal de pagos
    pagos_view = ft.Column(
        [
            ft.Text("Gestión de Pagos", size=24, weight=ft.FontWeight.BOLD),
            dropdown_usuarios,
            dropdown_conceptos,
            fecha_field,
            cantidad_field,
            registrar_button,
            ft.Divider(),
            ft.Text("Historial de Pagos", size=20, weight=ft.FontWeight.BOLD),
            pagos_list
        ],
        spacing=10
    )

    # Cargar los pagos al iniciar la vista
    actualizar_vista_pagos()

    # Retornar la vista principal
    return pagos_view
