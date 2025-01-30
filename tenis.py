import flet as ft
import re
import json
from modelos.base_model import BaseModel  # Importar BaseModel desde base_model.py
from modelos.usuario import Usuario  # Importar la nueva clase Usuario
from modelos.Inscripcion import Inscripcion
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento
from datetime import datetime
import os

from utils.validations import validar_identificacion, validar_email, validar_apellidos




# ------------------------- CONTROLADOR -------------------------
from controllers.club_controller import ClubController  


# ------------------------- VISTA -------------------------
def main(page: ft.Page):
    page.title = "Club de Tenis"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )

    titulo = ft.Text("Club de Tenis", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    app_bar = ft.AppBar(
        title=titulo,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_icon_button],
    )

    def cerrar_dialogo(e):
        aviso_dialog.open = False
        page.update()

    aviso_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Advertencia"),
        content=ft.Text("Por favor, complete todos los campos."),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo),
        ],
    )

    def inscribir_persona(e):
        if not nombre_field.value or not apellidos_field.value or not id_field.value or not correo_field.value:
            page.dialog = aviso_dialog
            aviso_dialog.open = True
            page.update()
            return

        nuevo_usuario = Usuario(
            id=Usuario.nuevo_id(),  # Generar un nuevo ID
            nombre=nombre_field.value,
            apellidos=apellidos_field.value,  # Obtener 'apellidos'
            edad=int(edad_field.value),  # Asegurarse de convertir a int
            num_identificacion=id_field.value,
            correo=correo_field.value,
            telefono=telefono_field.value,
            estado="inscrito"  # Estado por defecto
        )

        controller.agregar_usuario(nuevo_usuario)

        # Limpiar los campos después de la inscripción
        nombre_field.value = ""
        apellidos_field.value = ""  # Limpiar 'apellidos_field'
        edad_field.value = ""
        id_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        page.snack_bar = ft.SnackBar(
            ft.Text("Usuario inscrito exitosamente", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN
        )
        # age.snack_bar.open = True
        page.update()

    

    nombre_field = ft.TextField(label="Nombre", width=400, border_color=ft.colors.OUTLINE, expand=True)
    edad_field = ft.TextField(label="Edad", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion,keyboard_type=ft.KeyboardType.NUMBER)
    id_field = ft.TextField(label="Número de identificación", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion,keyboard_type=ft.KeyboardType.NUMBER)
    correo_field = ft.TextField(label="Correo", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_email)
    telefono_field = ft.TextField(label="Teléfono", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion,keyboard_type=ft.KeyboardType.NUMBER)
    apellidos_field = ft.TextField(label="Apellidos", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_apellidos)

    
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
            apellidos_field,  # Añadido 'apellidos_field'
            edad_field,
            id_field,
            correo_field,
            telefono_field,
            inscribir_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )


    def mostrar_info_usuario(usuario):
        usuario_info = ft.Column(
            [
                ft.Text("Información del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Text(f"Nombre: {usuario.nombre}"),
                ft.Text(f"Edad: {usuario.edad}"),
                ft.Text(f"Identificación: {usuario.num_identificacion}"),
                ft.Text(f"Correo: {usuario.correo}"),
                ft.Text(f"Teléfono: {usuario.telefono}"),
                ft.Text(f"Estado: {usuario.estado}"),
                ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_usuarios_view("inscrito")),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        content.controls.clear()
        content.controls.append(usuario_info)
        page.update()

    def mostrar_usuarios_view(estado):
        usuarios_filtrados = controller.filtrar_usuarios(estado)
        usuarios_list = [
            ft.ListTile(
                title=ft.Text(usuario.nombre, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Estado: {usuario.estado}"),
                leading=ft.Icon(ft.icons.PERSON),
                on_click=lambda e, u=usuario: mostrar_info_usuario(u),
            )
            for usuario in usuarios_filtrados
        ]
        usuarios_view = ft.ListView(
            [
                ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                *usuarios_list,
            ],
            spacing=10,
            expand=True,
        )
        content.controls.clear()
        content.controls.append(usuarios_view)
        page.update()


    matriculados_button = ft.ElevatedButton("Mostrar Matriculados", on_click=lambda e: mostrar_usuarios_view("matriculado"))
    inscritos_button = ft.ElevatedButton("Mostrar Inscritos", on_click=lambda e: mostrar_usuarios_view("inscrito"))

    Usuarios_view = ft.Column([
        ft.Text("Usuarios", size=20, weight=ft.FontWeight.BOLD),
        matriculados_button,
        inscritos_button
    ], spacing=10)
    

    # Torneos
    def inscribir_a_torneo(e):
        if not dropdown_usuarios.value or not dropdown_torneos.value:
            page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar un usuario y un torneo"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open = True
            return

        # Buscar el ID del torneo seleccionado
        try:
            with open("base_de_datos/torneos.json", "r") as archivo:
                torneos = json.load(archivo)
                torneo = next((t for t in torneos if t["nombre"] == dropdown_torneos.value), None)
        except (FileNotFoundError, json.JSONDecodeError):
            torneo = None

        if not torneo:
            page.snack_bar = ft.SnackBar(
                ft.Text("El torneo seleccionado no existe."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            return

        try:
            # Crear y guardar la inscripción
            nueva_inscripcion = Inscripcion(usuario=dropdown_usuarios.value, torneo_id=torneo["id"])
            nueva_inscripcion.guardar()

            # Crear el diálogo
            dialog = ft.AlertDialog(
                title=ft.Text("Inscripción Exitosa"),
                content=ft.Text(f"El usuario '{dropdown_usuarios.value}' ha sido inscrito exitosamente en el torneo '{dropdown_torneos.value}'!"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.overlay.remove(dialog)),
                ],
            )
            # Agregar el diálogo al overlay y actualizar la página
            page.overlay.append(dialog)
            page.update()

            # Opcional: Actualizar la vista de inscripciones
            actualizar_inscripciones()

        except ValueError as ex:
            # Si ya está inscrito, mostrar un mensaje de advertencia
            page.snack_bar = ft.SnackBar(ft.Text(str(ex)), bgcolor=ft.colors.WARNING)
            page.snack_bar.open = True

        page.update()


    def actualizar_inscripciones():
        try:
            # Cargar inscripciones
            inscripciones = Inscripcion.cargar_inscripciones()
        except Exception:
            inscripciones = []

        try:
            # Cargar torneos
            with open("base_de_datos/torneos.json", "r") as archivo:
                torneos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            torneos = []

        # Crear un diccionario de torneos para buscar por ID
        torneos_dict = {torneo["id"]: torneo["nombre"] for torneo in torneos}

        # Limpiar la lista de inscripciones
        inscripciones_list.controls.clear()

        # Agregar los elementos scrolleables al ListView
        inscripciones_list.controls.append(
            ft.Container(
                content=ft.ListView(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(f"Usuario: {inscripcion['usuario']}"),
                            subtitle=ft.Text(f"Torneo: {torneos_dict.get(inscripcion['torneo_id'], 'Torneo no encontrado')}"),
                        )
                        for inscripcion in inscripciones
                    ],
                    spacing=10,  # Espaciado entre elementos
                ),
                expand=True,  # Permitir que el contenedor ocupe el espacio disponible
                height=500,   # Fijar altura para permitir scroll si el contenido excede
            )
        )

        # Actualizar la página
        page.update()

    def agregar_torneo(e):
        nuevo_torneo = Torneo(id=Torneo.nuevo_id(), nombre="Nuevo Torneo", fecha="2025-01-01")
        nuevo_torneo.guardar()
        actualizar_torneos()
        page.snack_bar = ft.SnackBar(ft.Text("Torneo añadido"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True

    def actualizar_torneos():
        torneos = controller.cargar_torneos()

        # Actualizamos las opciones del dropdown
        dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in torneos]

        # Limpiamos y reconstruimos la lista de torneos
        torneos_list.controls.clear()
        torneos_list.controls.append(
            ft.Container(  # Agregamos un contenedor para definir el tamaño y permitir scroll
                content=ft.ListView(
                    [
                        ft.ListTile(
                            title=ft.Text(torneo.nombre),
                            subtitle=ft.Text(torneo.fecha),
                        ) for torneo in torneos
                    ],
                    spacing=10,  # Espaciado entre los elementos
                ),
                expand=True,  # El contenedor ocupará el espacio disponible
                height=500,   # Altura fija para habilitar el scroll si es necesario
                bgcolor=ft.colors.SURFACE_VARIANT,  # Color de fondo opcional
                padding=10,  # Opcional: Espaciado interno
            )
        )
        page.update()

    dropdown_usuarios = ft.Dropdown(
        label="Seleccionar Usuario",
        options=[ft.dropdown.Option(usuario.nombre) for usuario in controller.filtrar_usuarios("matriculado")],
    )

    dropdown_torneos = ft.Dropdown(label="Seleccionar Torneo", options=[])

    inscribir_button = ft.ElevatedButton(
        "Inscribir en Torneo", icon=ft.icons.CHECK, on_click=inscribir_a_torneo
    )

    torneos_list = ft.Column([])

    agregar_torneo_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=agregar_torneo, tooltip="Añadir Torneo"
    )

    inscripciones_list = ft.Column([])

    inscripciones_view = ft.Container(
        ft.Column(
            [
                ft.Text("Inscripciones", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                inscripciones_list,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        expand=True,
        padding=20,
    )

    torneos_view = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        dropdown_usuarios,
                        dropdown_torneos,
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
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Torneos", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        torneos_list,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
            ft.VerticalDivider(width=1),
            inscripciones_view,  # Nueva vista
        ],
        expand=True,
    )

    actualizar_torneos()

    #Entrenamientos
    def inscribir_a_entrenamiento(e):
        if not dropdown_usuarios.value or not dropdown_entrenamientos.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Debe seleccionar un usuario y un entrenamiento."),
                bgcolor=ft.colors.ERROR,
            )
            page.snack_bar.open = True
            return

        # Buscar el entrenamiento seleccionado
        try:
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos = json.load(archivo)
                entrenamiento = next(
                    (t for t in entrenamientos if t["fecha"] == dropdown_entrenamientos.value), None
                )
        except (FileNotFoundError, json.JSONDecodeError):
            entrenamiento = None

        if not entrenamiento:
            page.snack_bar = ft.SnackBar(
                ft.Text("El entrenamiento seleccionado no existe."),
                bgcolor=ft.colors.ERROR,
            )
            page.snack_bar.open = True
            return

        # Buscar el usuario seleccionado
        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
                usuario = next(
                    (u for u in usuarios if u["nombre"] == dropdown_usuarios.value), None
                )
        except (FileNotFoundError, json.JSONDecodeError):
            usuario = None

        if not usuario:
            page.snack_bar = ft.SnackBar(
                ft.Text("El usuario seleccionado no existe."),
                bgcolor=ft.colors.ERROR,
            )
            page.snack_bar.open = True
            return

        # Crear la asistencia y guardar
        try:
            nueva_asistencia = Asistencia_Entrenamiento(
                id=Asistencia_Entrenamiento.nuevo_id(),
                usuario_id=usuario["id"],
                entrenamiento_id=entrenamiento["id"],
                estado="pendiente",
            )
            nueva_asistencia.guardar()

            # Mostrar mensaje de éxito
            dialog = ft.AlertDialog(
                title=ft.Text("Inscripción Exitosa"),
                content=ft.Text(
                    f"El usuario '{dropdown_usuarios.value}' ha sido inscrito exitosamente en el entrenamiento del '{dropdown_entrenamientos.value}'!"
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.overlay.remove(dialog)),
                ],
            )
            page.overlay.append(dialog)
            page.update()

            # Actualizar la vista de asistencias
            actualizar_asistencias()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open = True

        page.update()


    def actualizar_entrenamientos():
        try:
            # Cargar entrenamientos desde el archivo JSON
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            entrenamientos = []
    
        if not entrenamientos:
            print("No se encontraron entrenamientos.")
            dropdown_entrenamientos.options = []
            entrenamientos_list.controls.clear()
            page.update()
            return
    
        # Actualizamos las opciones del dropdown
        dropdown_entrenamientos.options = [
            ft.dropdown.Option(entrenamiento["fecha"]) for entrenamiento in entrenamientos
        ]
    
        # Mostrar entrenamientos en la lista
        entrenamientos_list.controls.clear()
        for entrenamiento in entrenamientos:
            entrenamientos_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Fecha: {entrenamiento['fecha']}"),
                    subtitle=ft.Text(f"ID: {entrenamiento['id']}"),
                )
            )
        page.update()



    def actualizar_asistencias():
        try:
            # Cargar asistencias desde el archivo JSON
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []
    
        try:
            # Cargar usuarios y entrenamientos para mostrar nombres en lugar de IDs
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
            usuarios_dict = {usuario["id"]: usuario["nombre"] for usuario in usuarios}
    
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos = json.load(archivo)
            entrenamientos_dict = {entrenamiento["id"]: entrenamiento["fecha"] for entrenamiento in entrenamientos}
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios_dict = {}
            entrenamientos_dict = {}
    
        # Limpiar la lista de asistencias en la interfaz
        asistencias_list.controls.clear()
    
        # Mostrar asistencias en la interfaz
        for asistencia in asistencias:
            usuario_nombre = usuarios_dict.get(asistencia["usuario_id"], "Usuario no encontrado")
            entrenamiento_fecha = entrenamientos_dict.get(asistencia["entrenamiento_id"], "Entrenamiento no encontrado")
            asistencias_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Usuario: {usuario_nombre}"),
                    subtitle=ft.Text(f"Entrenamiento: {entrenamiento_fecha} | Estado: {asistencia['estado']}"),
                )
            )
    
        # Actualizar la página
        page.update()



    dropdown_entrenamientos = ft.Dropdown(label="Seleccionar Entrenamiento", options=[])

    inscribir_entrenamiento_button = ft.ElevatedButton(
        "Inscribir en Entrenamiento",
        icon=ft.icons.CHECK,
        on_click=inscribir_a_entrenamiento,
    )

    entrenamientos_list = ft.Column([])
    asistencias_list = ft.Column([])

    entrenamientos_view = ft.Row(
        [
            # Primera columna: Dropdowns y botón para inscripción
            ft.Container(
                ft.Column(
                    [
                        dropdown_usuarios,
                        dropdown_entrenamientos,
                        inscribir_entrenamiento_button,
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
            # Segunda columna: Entrenamientos disponibles
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Entrenamientos Disponibles", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        entrenamientos_list,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
            ft.VerticalDivider(width=1),
            # Tercera columna: Asistencias registradas
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Asistencias Registradas", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        asistencias_list,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
        ],
        expand=True,
    )


    actualizar_entrenamientos()


    def informes_view():
        # Campo de texto para ingresar el año
        input_anio = ft.TextField(
            label="Ingresar Año",
            width=100,
            hint_text="2025",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        # Campo de texto para ingresar el mes
        input_mes = ft.TextField(
            label="Ingresar Mes",
            width=50,
            hint_text="01",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        # Contenedor para mostrar los informes
        informe_container = ft.Column([], expand=True, spacing=10)

        # Función para crear informes
        def crear_informes(anio, mes):
            print("Generando informes...")
            # Validar entradas
            if not anio.isdigit() or not mes.isdigit():
                page.snack_bar = ft.SnackBar(
                    ft.Text("Año y mes deben ser números."),
                    bgcolor=ft.colors.ERROR
                )
                page.snack_bar.open = True
                page.update()
                return

            anio_int = int(anio)
            mes_int = int(mes)

            if not (1 <= mes_int <= 12):
                page.snack_bar = ft.SnackBar(
                    ft.Text("Mes debe estar entre 1 y 12."),
                    bgcolor=ft.colors.ERROR
                )
                page.snack_bar.open = True
                page.update()
                return

            # Formatear mes con dos dígitos
            mes_formateado = str(mes_int).zfill(2)

            # Cargar los datos de los usuarios
            try:
                with open("base_de_datos/usuarios.json", "r") as archivo_usuarios:
                    usuarios = json.load(archivo_usuarios)
            except FileNotFoundError:
                print("El archivo de usuarios no se encuentra.")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Archivo de usuarios no encontrado."),
                    bgcolor=ft.colors.ERROR
                )
                page.snack_bar.open = True
                page.update()
                return
            except json.JSONDecodeError:
                print("El archivo de usuarios no está en el formato correcto.")
                page.snack_bar = ft.SnackBar(
                    ft.Text("Error en el formato del archivo de usuarios."),
                    bgcolor=ft.colors.ERROR
                )
                page.snack_bar.open = True
                page.update()
                return

                # Filtrar usuarios con estado 'matriculado'
            usuarios_matriculados = [usuario for usuario in usuarios if usuario['estado'] == 'matriculado']

                    # Generar un informe para cada miembro matriculado
            for usuario in usuarios_matriculados:
                Informe.crear_informe(usuario['id'], mes_formateado, anio)

                print(f"Informes generados para el mes {mes_int} del año {anio_int}")
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Informes generados para el mes {mes_int} del año {anio_int}."),
                    bgcolor=ft.colors.GREEN
                )
                page.snack_bar.open = True
                page.update()

        # Función para cargar y mostrar informes
        def generar_informes(e):
            anio_val = input_anio.value
            mes_val = input_mes.value

            # Primero, crear los informes en disco
            crear_informes(anio_val, mes_val)

            # Luego, limpiar el contenedor e intentar mostrar los informes creados
            informe_container.controls.clear()
            try:
                with open("base_de_datos/informes.json", "r") as file:
                    content = file.read().strip()
                    if not content:
                        informes = []
                    else:
                        informes = json.loads(content)

                # Filtrar informes por año y mes
                informes_filtrados = [
                    inf for inf in informes
                    if str(inf["anio"]) == str(anio_val)
                    and str(inf["mes"]).zfill(2) == str(mes_val).zfill(2)
                ]

                print(f"Cantidad de informes filtrados: {len(informes_filtrados)}")

                # Mostrar cada informe con sus datos en un Card
                for inf in informes_filtrados:
                    informe_card = ft.Card(
                        content=ft.Container(
                            ft.Column([
                                ft.Text(f"Informe ID: {inf['id']}"),
                                ft.Text(f"Usuario ID: {inf['usuario_id']}"),
                                ft.Text(f"Año: {inf['anio']}  |  Mes: {inf['mes']}"),
                                ft.Text(f"Clases del Mes: {inf['clases_mes']}"),
                                ft.Text(f"Clases Asistidas: {inf['clases_asistidas']}"),
                                ft.Text(f"Torneos Asistidos: {inf['torneos_asistidos']}"),
                                ft.Text(f"Top Torneos: {inf['top_torneos']}")
                            ]),
                            padding=10
                        ),
                        width=300,
                    )
                    informe_container.controls.append(informe_card)

                page.update()

            except Exception as ex:
                print("Error al cargar informes:", ex)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Error al cargar informes."),
                    bgcolor=ft.colors.ERROR
                )
                page.snack_bar.open = True
                page.update()

        # Botón para generar informes
        generar_informe_button = ft.ElevatedButton(
            "Generar Informes",
            on_click=generar_informes
        )

        # Retornar la vista de informes
        return ft.Column(
            [
                ft.Row([input_anio, input_mes]),
                generar_informe_button,
                informe_container
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )



    def crear_entrenamiento(anio, mes, dia):
        # Formatear día y mes para asegurar el formato de dos dígitos
        dia_formateado = str(dia).zfill(2)
        mes_formateado = str(mes).zfill(2)
        
        # Componer la fecha en formato aaaa-mm-dd
        fecha = f"{anio}-{mes_formateado}-{dia_formateado}"
        
        # Intentar crear un nuevo objeto de Entrenamiento
        try:
            nuevo_entrenamiento = Entrenamiento(id=Entrenamiento.nuevo_id(), fecha=fecha)
            nuevo_entrenamiento.guardar()  # Guarda el entrenamiento en la base de datos
            nuevo_entrenamiento.crear_asistencia_entrenamientos()  # Crea asistencias para todos los usuarios
            print(f"Entrenamiento creado para la fecha {fecha}")
        except Exception as e:
            print(f"No se pudo crear el entrenamiento: {e}")
    
    # crear_entrenamiento_button = ft.ElevatedButton("Crear Entrenamiento", on_click=lambda e: crear_entrenamiento(anio, mes, dia)) #Modificar para que sea dinamico en el front
    
    def crear_torneo(anio, mes, dia):
        # Formatear día y mes para asegurar el formato de dos dígitos
        dia_formateado = str(dia).zfill(2)
        mes_formateado = str(mes).zfill(2)
        
        # Componer la fecha en formato aaaa-mm-dd
        fecha = f"{anio}-{mes_formateado}-{dia_formateado}"
        
        # Intentar crear un nuevo objeto de Torneo
        nuevo_torneo = Torneo(
            id=Torneo.nuevo_id(),
            nombre="Nombre del Torneo",  # Asumiendo que el nombre se proveerá o se manejará de otra manera
            fecha=fecha
        )
        nuevo_torneo.guardar()
        print(f"Torneo creado para la fecha {fecha}")

    #crear_torneo_button = ft.ElevatedButton("Crear Torneo", on_click=lambda e: crear_torneo(anio, mes, dia)) #Modificar para que sea dinamico en el front

    def crear_asistencia_torneo(torneo_id, miembro_id, puesto):
        Asistencia_Torneo.crear_asistencia(
            torneo_id=torneo_id,
            miembro_id=miembro_id,
            puesto=puesto
        )
        print(f"Asistencia para el torneo {torneo_id} creada para el miembro {miembro_id} con puesto {puesto}")

    #crear_asistencia_torneo_button = ft.ElevatedButton("Aceptar", on_click=lambda e: crear_asistencia_torneo(usuario_id, torneo_id, puesto)) #Modificar para que sea dinamico en el front



    def tomar_asistencia_entrenamiento(usuario_id, entrenamiento_id, estado):
        # Verificar que el estado sea válido
        if estado not in ["ausente", "presente"]:
            print("Error: Estado no válido. Debe ser 'ausente' o 'presente'.")
            return
        
        # Encontrar el ID de la asistencia correspondiente
        asistencia_id = Asistencia_Entrenamiento.find_by_user_and_entrenamiento_id(usuario_id, entrenamiento_id)
        
        if asistencia_id is None:
            print("No se encontró una asistencia correspondiente con los datos proporcionados.")
            return
        
        # Cargar el objeto Asistencia_Entrenamiento usando el ID encontrado
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
            
            # Encontrar el objeto asistencia específico y cambiar su estado
            asistencia = next((item for item in asistencias if item["id"] == asistencia_id), None)
            if asistencia:
                asistencia_obj = Asistencia_Entrenamiento(id=asistencia['id'], usuario_id=asistencia['usuario_id'], entrenamiento_id=asistencia['entrenamiento_id'], estado=asistencia['estado'])
                asistencia_obj.cambiar_estado(estado)
                print(f"Estado de asistencia actualizado correctamente a {estado}.")
            else:
                print("No se pudo cargar la asistencia correctamente.")
        except FileNotFoundError:
            print("Archivo de asistencias no encontrado.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo de asistencias.")
        
    #tomar_asistencia_entrenamiento_button = ft.ElevatedButton("Aceptar", on_click=lambda e: tomar_asistencia_entrenamiento(usuario_id, entrenamiento_id, estado)) #Modificar para que sea dinamico en el front

    def main(page: ft.Page):
        page.title = "Gestión de Pagos del Club"
        page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()
    
    usuarios_inscritos = [u for u in controller.usuarios if u.estado == "inscrito"]
# Dropdown de usuarios
    # Crear un diccionario para mapear nombres de usuarios a sus IDs
    nombre_id_map = {u.nombre: u.id for u in usuarios_inscritos}

# Dropdown de usuarios usando solo el argumento 'text'
    dropdown_usuarios = ft.Dropdown(
        label="Seleccionar Usuario",
        options=[ft.dropdown.Option(text=u.nombre) for u in usuarios_inscritos]
    )

    # Dropdown de conceptos
    dropdown_conceptos = ft.Dropdown(
        label="Concepto de Pago",
        options=[
            ft.dropdown.Option(text="Matrícula"),
            ft.dropdown.Option(text="Mensualidad")
        ]
    )

    # Campos adicionales
    fecha_field = ft.TextField(label="Fecha (YYYY-MM-DD)")
    cantidad_field = ft.TextField(label="Cantidad")
    pagos_list = ft.ListView(expand=True)

    # Función para registrar un pago
    def registrar_pago():
        usuario_nombre = dropdown_usuarios.value
        if not (usuario_nombre and dropdown_conceptos.value and fecha_field.value and cantidad_field.value):
            mostrar_snackbar("Por favor, completa todos los campos.", "ERROR")
            return

        if usuario_nombre in nombre_id_map:
            usuario_id = nombre_id_map[usuario_nombre]
            nuevo_pago = {
                "id": len(controller.cargar_pagos()) + 1,
                "usuario_id": usuario_id,
                "concepto": dropdown_conceptos.value,
                "fecha": fecha_field.value,
                "cantidad": float(cantidad_field.value),
            }

        # Guardar el nuevo pago
            pagos = controller.cargar_pagos()
            pagos.append(nuevo_pago)
            BaseModel.guardar_datos("pagos.json", pagos)

        # Actualizar estado del usuario
            controller.actualizar_estado_usuario(usuario_id, "matriculado")
            mostrar_snackbar("Pago registrado exitosamente.", "SUCCESS")
            actualizar_vista_pagos()
        else:
            mostrar_snackbar("Error: Usuario no encontrado.", "ERROR")


    # Mostrar mensajes con SnackBar
    def mostrar_snackbar(mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        page.overlay.append(snack_bar)
        
    registrar_button = ft.ElevatedButton(
    "Registrar Pago",
    icon=ft.icons.SAVE,
    on_click=lambda e: registrar_pago()
)

    # Actualizar la vista de pagos
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
    # Layout principal
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

    actualizar_vista_pagos()

    # Cambiar vistas
    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index == 0:
            content.controls.append(inscripcion_view)
        elif index == 1:
            content.controls.append(Usuarios_view)
        elif index == 2:
            content.controls.append(torneos_view)
        elif index == 3:
            content.controls.append(entrenamientos_view)
        elif index == 4:
            content.controls.append(informes_view())
        elif index == 5:
            content.controls.append(pagos_view)
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.PERSON_ADD, label="Inscripción"),
            ft.NavigationRailDestination(icon=ft.icons.GROUP, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.SPORTS_TENNIS, label="Torneos"),
            ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamiento"),
            ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
        ],
        on_change=destination_change,
    )

    content = ft.Column([inscripcion_view], expand=True)

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)
