# tallerdiseno1/views/pagos_view.py
import flet as ft
from modelos.base_model import BaseModel
from utils.validations import validar_fecha
from utils.fecha import formatear_fecha

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
            ft.dropdown.Option("Inscripcion"),
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

    # Para garantizar el scroll, es posible que necesitemos ajustar el contenedor que alberga el ListView.
    # Asegurémonos de que el ListView tiene espacio suficiente para expandirse y activar el scroll.
    pagos_list_container = ft.Container(
        content=pagos_list,
        expand=True,
        padding=10  # Padding opcional para mejorar la visualización
    )

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

        # Utilizar la función formatear_fecha desde fecha.py
        fecha, error_message = formatear_fecha(fecha)
        if error_message:
            mostrar_snackbar(error_message, "ERROR")
            return
        
        # Actualizamos el valor del input de fecha con el formato correcto
        fecha_field.value = fecha
        
        # Validación de fecha
        validar_fecha(fecha_field)  # Utilizamos la función de validación de fecha aquí
        if fecha_field.error_text:
            mostrar_snackbar(fecha_field.error_text, "ERROR")
            return

        if not (usuario_nombre and concepto and fecha and cantidad):
            mostrar_snackbar("Por favor, completa todos los campos.", "ERROR")
            return

        usuarios_inscritos_dict = controller.usuarios_inscritos_dict()

        if usuario_nombre in usuarios_inscritos_dict:
            usuario_id = usuarios_inscritos_dict[usuario_nombre]
            
            # Verificar si el usuario ya está matriculado y el pago es de inscripción
            if controller.usuario_esta_matriculado(usuario_id) and concepto == "Inscripcion":
                mostrar_snackbar("Error: El usuario ya está matriculado y no puede pagar la inscripción nuevamente.", "ERROR")
                return
            if not controller.usuario_esta_matriculado(usuario_id) and concepto == "Mensualidad":
                mostrar_snackbar("Error: El usuario debe estar matriculado para pagar mensualidad.", "ERROR")
                return
            
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
            if concepto == "Inscripcion":
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
            pagos_list_container  # Utilizando el contenedor ajustado
        ],
        spacing=10,
        expand=True  # Asegurar que la columna principal pueda expandirse
    )

    # Cargar los pagos al iniciar la vista
    actualizar_vista_pagos()

    # Retornar la vista principal
    return pagos_view
