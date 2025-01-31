# tallerdiseno1/views/torneos_view.py

import flet as ft
import json
from dataclasses import asdict  # Importar asdict para convertir dataclasses a dicts
from modelos.base_model import BaseModel
from modelos.asistencia_torneos import Asistencia_Torneo  # Asegúrate de que exista el import correcto
from modelos.torneo import Torneo  # Asegúrate de importar la clase Torneo
from utils.validations import validar_fecha

def crear_asistencia_torneo(torneo_id, usuario_id, puesto):
    """
    Crea un registro de asistencia en asistencia_torneos.json.
    """
    Asistencia_Torneo.crear_asistencia(
        torneo_id=torneo_id,
        usuario_id=usuario_id,
        puesto=puesto
    )
    print(f"Asistencia para el torneo {torneo_id} creada para el miembro {usuario_id} con puesto {puesto}")


def create_torneos_view(controller, torneos, page):
    """
    Crea y retorna la vista de gestión de torneos, pero ahora usando asistencia_torneos.json
    en lugar de inscripciones.json.
    
    Parámetros:
        controller: El controlador de la aplicación (ClubController) que gestiona la lógica de negocio.
        torneos: Lista de torneos disponibles (instancias de Torneo).
        page: Página de Flet para actualizar UI y mostrar SnackBars.
    
    Retorna:
        tuple: Contiene la vista de torneos y los componentes necesarios como objetos de Flet.
    """
    
    # Función para mostrar SnackBar
    def mostrar_snackbar(mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    # Función para cerrar el diálogo
    def cerrar_dialogo():
        page.dialog.open = False
        page.update()

    # Función para inscribir (crear asistencia) a un torneo
    def inscribir_a_torneo(e):
        usuario_nombre = dropdown_usuarios.value
        torneo_nombre = dropdown_torneos.value
        puesto_valor = puesto_field.value
        
        if not usuario_nombre or not torneo_nombre or not puesto_valor:
            mostrar_snackbar("Debe seleccionar un usuario, un torneo y definir el puesto.", "ERROR")
            return
        
        # Obtener torneo_id desde el nombre usando el mapeo
        torneo_id = torneo_id_map.get(torneo_nombre)
        if torneo_id is None:
            mostrar_snackbar("El torneo seleccionado no existe.", "ERROR")
            return
        
        # Obtener el usuario_id desde el nombre (utilizamos el diccionario del controlador)
        usuario_id_dict = controller.usuarios_matriculados_dict()
        usuario_id = usuario_id_dict.get(usuario_nombre)
        if not usuario_id:
            mostrar_snackbar("El usuario seleccionado no existe o no está matriculado.", "ERROR")
            return
        
        # Intentamos convertir el puesto a entero
        try:
            puesto_int = int(puesto_valor)
        except ValueError:
            mostrar_snackbar("El puesto debe ser un número entero.", "ERROR")
            return

        # Crear la asistencia al torneo
        try:
            crear_asistencia_torneo(torneo_id, usuario_id, puesto_int)
            mostrar_snackbar(
                f"Usuario ID={usuario_id} inscrito (asistencia) al torneo ID={torneo_id} con puesto {puesto_int}",
                "SUCCESS"
            )
        except Exception as ex:
            mostrar_snackbar(f"Error al crear la asistencia: {ex}", "ERROR")

        # Limpieza de campo puesto (opcional)
        puesto_field.value = ""
        page.update()

    # Función para agregar torneo
    def agregar_torneo(e):
        # Abrir un diálogo para ingresar nombre y fecha del torneo
        nombre_input = ft.TextField(label="Nombre del Torneo", autofocus=True)
        fecha_input = ft.TextField(label="Fecha del Torneo", hint_text="YYYY-MM-DD")
        agregar_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Torneo"),
            content=ft.Column([nombre_input, fecha_input], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
                ft.TextButton("Agregar", on_click=lambda e: agregar_torneo_confirm(nombre_input.value, fecha_input.value, fecha_input)),
            ]
        )
        page.dialog = agregar_dialog
        agregar_dialog.open = True
        page.update()


    # Confirmar agregar torneo
    def agregar_torneo_confirm(nombre, fecha, fecha_input):
        # Formatear la fecha para asegurarse de que el día y el mes son de dos dígitos
        try:
            partes = fecha.split('-')
            if len(partes) == 3:
                año, mes, dia = partes
                mes = f"{int(mes):02}"  # Asegura que el mes tenga dos dígitos
                dia = f"{int(dia):02}"  # Asegura que el día tenga dos dígitos
                fecha_formateada = f"{año}-{mes}-{dia}"
            else:
                mostrar_snackbar("Formato de fecha incorrecto. Use YYYY-MM-DD", "ERROR")
                return
        except ValueError:
            mostrar_snackbar("Fecha inválida. Asegúrese de que el año, mes y día sean números.", "ERROR")
            return
        
        # Actualizamos el valor del input de fecha con el formato correcto
        fecha_input.value = fecha_formateada

        # Validación de fecha
        validar_fecha(fecha_input)  # Utilizamos la función de validación de fecha aquí
        if fecha_input.error_text:
            mostrar_snackbar(fecha_input.error_text, "ERROR")
            return
        if not nombre:
            mostrar_snackbar("Por favor, complete todos los campos.", "ERROR")
            return
        
        # Crear el torneo como una instancia de Torneo
        nuevo_id = max([t.id for t in torneos], default=0) + 1
        nuevo_torneo = Torneo(id=nuevo_id, nombre=nombre, fecha=fecha)
        torneos.append(nuevo_torneo)
        # Convertir todos los torneos a dicts antes de guardar
        torneos_dicts = [asdict(torneo) for torneo in torneos]
        BaseModel.guardar_datos("torneos.json", torneos_dicts)
        # Actualizar el mapeo de nombres a IDs
        torneo_id_map[nombre] = nuevo_id
        # Agregar la entrada visual del nuevo torneo en la lista
        torneos_list.controls.append(
            ft.ListTile(
                title=ft.Text(nuevo_torneo.nombre),
                on_click=lambda e, t=nuevo_torneo.id: on_torneo_click(t),
                data=nuevo_torneo.id  # Almacenar torneo.id como data
            )
        )
        # Actualizar las opciones en el dropdown de torneos
        dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in torneos]
        # Actualizar las opciones en el dropdown de usuarios
        dropdown_usuarios.options = [ft.dropdown.Option(usuario.nombre) for usuario in controller.usuarios_matriculados_list()]
        mostrar_snackbar(f"Torneo '{nombre}' agregado exitosamente.", "SUCCESS")
        # Cerrar el diálogo correctamente
        page.dialog.open = False
        page.update()


    # Función para mostrar asistencias al hacer clic en un torneo
    def on_torneo_click(torneo_id):
        asistencias_list.controls.clear()
        
        # Obtener las asistencias para este torneo
        asistencias = controller.get_asistencias_by_torneo(torneo_id)  # Se asume está en el controller

        if not asistencias:
            asistencias_list.controls.append(ft.Text("No hay asistencias para este torneo."))
        else:
            for asis in asistencias:
                # Buscar el nombre del usuario a partir de su ID
                user_obj = controller.get_user_by_id(asis["usuario_id"])
                if user_obj:
                    nombre_usuario = user_obj.nombre
                else:
                    nombre_usuario = f"Usuario ID={asis['usuario_id']}"
                
                # Mostramos nombre y puesto
                asistencias_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON),
                        title=ft.Text(f"{nombre_usuario} (Puesto: {asis['puesto']})")
                    )
                )
        page.update()
    
    def actualizar_data_torneos():
        """
        Refresca la lista de torneos y actualiza los dropdowns de usuarios y torneos.
        """
        # Recargar la lista de torneos desde el controlador
        torneos_actualizados = controller.cargar_torneos()
        
        # Actualizar el dropdown de torneos
        dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in torneos_actualizados]

        # Actualizar el mapeo de nombres a IDs para torneos
        torneo_id_map = {torneo.nombre: torneo.id for torneo in torneos_actualizados}

        # Limpiar y reconstruir la lista de torneos
        torneos_list.controls.clear()
        torneos_list.controls.extend([
            ft.ListTile(
                title=ft.Text(torneo.nombre),
                on_click=lambda e, t=torneo.id: on_torneo_click(t),
                data=torneo.id
            )
            for torneo in torneos_actualizados
        ])

        # Actualizar las opciones en el dropdown de usuarios
        dropdown_usuarios.options = [ft.dropdown.Option(usuario.nombre) for usuario in controller.usuarios_matriculados_list()]
        
        # Recargar la lista de usuarios matriculados y actualizar el dropdown
        # dropdown_usuarios = controller.dropdown_usuarios_matriculados()  # Removido para evitar redefinición

        # Asegurarse de actualizar la UI
        page.update()



    # Dropdown de usuarios (matriculados)
    dropdown_usuarios = ft.Dropdown(
        label="Seleccione un usuario",
        options=[ft.dropdown.Option(usuario.nombre) for usuario in controller.usuarios_matriculados_list()],
        value=None  # Inicialmente sin selección
    )

    # Mapeo de nombres de torneos a IDs para uso interno
    torneo_id_map = {torneo.nombre: torneo.id for torneo in torneos}

    # Dropdown de torneos
    dropdown_torneos = ft.Dropdown(
        label="Seleccione un torneo",
        options=[ft.dropdown.Option(torneo.nombre) for torneo in torneos],
        value=None  # Inicialmente sin selección
    )

    # Campo para el puesto
    puesto_field = ft.TextField(label="Puesto en el Torneo", value="")

    # Lista de torneos
    torneos_list = ft.ListView(
        controls=[
            ft.ListTile(
                title=ft.Text(torneo.nombre),
                on_click=lambda e, t=torneo.id: on_torneo_click(t),  # Corregido el acceso
                data=torneo.id
            )
            for torneo in torneos
        ],
        expand=True,
        auto_scroll=False
    )

    # Botón para crear asistencia (antes "Inscribir")
    inscribir_button = ft.ElevatedButton(
        "Crear Asistencia",
        icon=ft.icons.CHECK,
        on_click=inscribir_a_torneo
    )

    # Botón flotante para agregar torneo
    agregar_torneo_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=agregar_torneo,
        tooltip="Añadir Torneo"
    )

    # Lista para mostrar asistencias
    asistencias_list = ft.ListView(expand=True, spacing=10)  # Cambiado a ListView

    # Contenedor (columna) de asistencias
    asistencias_view = ft.Container(
        ft.Column(
            [
                ft.Text("Asistencias", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                asistencias_list,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        expand=True,
        padding=20,
    )

    # Vista principal de torneos
    torneos_view = ft.Row(
        [
            # Columna de selección de usuario, torneo y puesto
            ft.Container(
                ft.Column(
                    [
                        dropdown_usuarios,
                        dropdown_torneos,
                        puesto_field,
                        inscribir_button,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=300,
                padding=20,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            ),
            ft.VerticalDivider(width=1),
            # Columna de lista de torneos y botón para agregar
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Torneos", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        torneos_list,
                        agregar_torneo_button,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
            ft.VerticalDivider(width=1),
            # Columna de asistencias registradas
            asistencias_view,
        ],
        expand=True,
    )

    return torneos_view, torneos_list, dropdown_torneos, actualizar_data_torneos
