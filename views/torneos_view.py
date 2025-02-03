# tallerdiseno1/views/torneos_view.py
import flet as ft
import json
from dataclasses import asdict
from modelos.base_model import BaseModel
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.torneo import Torneo
from utils.validations import validar_fecha
from utils.fecha import formatear_fecha

class ContenedorTorneosSuper:
    def __init__(self, controller, torneos, page):
        self.controller = controller
        self.torneos = torneos
        self.page = page

        # Dropdown de usuarios (matriculados)
        self.dropdown_usuarios = ft.Dropdown(
            label="Seleccione un usuario",
            options=[ft.dropdown.Option(usuario.nombre) for usuario in controller.usuarios_matriculados_list()],
            value=None
        )

        # Mapeo de nombres de torneos a IDs para uso interno
        self.torneo_id_map = {torneo.nombre: torneo.id for torneo in torneos}

        # Dropdown de torneos
        self.dropdown_torneos = ft.Dropdown(
            label="Seleccione un torneo",
            options=[ft.dropdown.Option(torneo.nombre) for torneo in torneos],
            value=None
        )

        # Campo para el puesto
        self.puesto_field = ft.TextField(label="Puesto en el Torneo", value="")

        # Lista de torneos
        self.torneos_list = ft.ListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(torneo.nombre),
                    on_click=lambda e, t=torneo.id: self.on_torneo_click(t),
                    data=torneo.id
                )
                for torneo in torneos
            ],
            expand=True,
            auto_scroll=False
        )

        # Botón para crear asistencia
        self.inscribir_button = ft.ElevatedButton(
            "Crear Asistencia",
            icon=ft.icons.CHECK,
            on_click=self.inscribir_a_torneo
        )

        # Botón flotante para agregar torneo
        self.agregar_torneo_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=self.agregar_torneo,
            tooltip="Añadir Torneo"
        )

        # Lista para mostrar asistencias
        self.asistencias_list = ft.ListView(expand=True, spacing=10)

        # Contenedor de asistencias
        self.asistencias_view = ft.Container(
            ft.Column(
                [
                    ft.Text("Asistencias", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=10, thickness=2),
                    self.asistencias_list,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
        )

        # Vista principal de torneos
        self.torneos_view = ft.Row(
            [
                # Columna de selección de usuario, torneo y puesto
                ft.Container(
                    ft.Column(
                        [
                            self.dropdown_usuarios,
                            self.dropdown_torneos,
                            self.puesto_field,
                            self.inscribir_button,
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
                            self.torneos_list,
                            self.agregar_torneo_button,
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    expand=True,
                    padding=20,
                ),
                ft.VerticalDivider(width=1),
                # Columna de asistencias registradas
                self.asistencias_view,
            ],
            expand=True,
        )

    def mostrar_snackbar(self, mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def cerrar_dialogo(self, e=None):
        self.page.dialog.open = False
        self.page.update()

    def inscribir_a_torneo(self, e):
        usuario_nombre = self.dropdown_usuarios.value
        torneo_nombre = self.dropdown_torneos.value
        puesto_valor = self.puesto_field.value

        if not usuario_nombre or not torneo_nombre or not puesto_valor:
            self.mostrar_snackbar("Debe seleccionar un usuario, un torneo y definir el puesto.", "ERROR")
            return

        torneo_id = self.torneo_id_map.get(torneo_nombre)
        if torneo_id is None:
            self.mostrar_snackbar("El torneo seleccionado no existe.", "ERROR")
            return

        usuario_id_dict = self.controller.usuarios_matriculados_dict()
        usuario_id = usuario_id_dict.get(usuario_nombre)
        if not usuario_id:
            self.mostrar_snackbar("El usuario seleccionado no existe o no está matriculado.", "ERROR")
            return

        try:
            puesto_int = int(puesto_valor)
            if puesto_int < 1 or puesto_int >= 1000:
                self.mostrar_snackbar("El puesto debe ser un número entero entre 1 y 999.", "ERROR")
                return
        except ValueError:
            self.mostrar_snackbar("El puesto debe ser un número entero.", "ERROR")
            return

        try:
            asistencias = self.controller.get_asistencias_by_torneo(torneo_id)
            asistencia_existente = next((a for a in asistencias if a.usuario_id == usuario_id), None)

            if asistencia_existente:
                Asistencia_Torneo.actualizar_puesto(torneo_id, usuario_id, puesto_int)
                self.mostrar_snackbar(
                    f"Usuario ID={usuario_id} ya inscrito. Puesto actualizado a {puesto_int}.",
                    "SUCCESS"
                )
            else:
                self.crear_asistencia_torneo(torneo_id, usuario_id, puesto_int)
                self.mostrar_snackbar(
                    f"Usuario ID={usuario_id} inscrito al torneo ID={torneo_id} con puesto {puesto_int}.",
                    "SUCCESS"
                )
        except Exception as ex:
            self.mostrar_snackbar(f"Error al crear o actualizar la asistencia: {ex}", "ERROR")

        self.puesto_field.value = ""
        self.page.update()

    def crear_asistencia_torneo(self, torneo_id, usuario_id, puesto):
        Asistencia_Torneo.crear_asistencia(
            torneo_id=torneo_id,
            usuario_id=usuario_id,
            puesto=puesto
        )
        print(f"Asistencia para el torneo {torneo_id} creada para el miembro {usuario_id} con puesto {puesto}")

    def agregar_torneo(self, e):
        nombre_input = ft.TextField(label="Nombre del Torneo", autofocus=True)
        fecha_input = ft.TextField(label="Fecha del Torneo", hint_text="YYYY-MM-DD")

        agregar_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Torneo"),
            content=ft.Column([nombre_input, fecha_input], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                ft.TextButton("Agregar", on_click=lambda e: self.agregar_torneo_confirm(nombre_input.value, fecha_input)),
            ]
        )
        self.page.dialog = agregar_dialog
        agregar_dialog.open = True
        self.page.update()

    def agregar_torneo_confirm(self, nombre, fecha_input):
        fecha_formateada, error_message = formatear_fecha(fecha_input.value)
        if error_message:
            self.mostrar_snackbar(error_message, "ERROR")
            return

        fecha_input.value = fecha_formateada
        fecha_input.update()

        validar_fecha(fecha_input)
        if fecha_input.error_text:
            self.mostrar_snackbar(fecha_input.error_text, "ERROR")
            return

        if not nombre:
            self.mostrar_snackbar("Por favor, complete todos los campos.", "ERROR")
            return

        nuevo_id = max([t.id for t in self.torneos], default=0) + 1
        nuevo_torneo = Torneo(id=nuevo_id, nombre=nombre, fecha=fecha_formateada)
        self.torneos.append(nuevo_torneo)
        torneos_dicts = [asdict(torneo) for torneo in self.torneos]
        BaseModel.guardar_datos("torneos.json", torneos_dicts)
        self.torneo_id_map[nombre] = nuevo_id

        self.torneos_list.controls.append(
            ft.ListTile(
                title=ft.Text(nuevo_torneo.nombre),
                on_click=lambda e, t=nuevo_torneo.id: self.on_torneo_click(t),
                data=nuevo_torneo.id
            )
        )

        self.dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in self.torneos]
        self.dropdown_usuarios.options = [ft.dropdown.Option(usuario.nombre) for usuario in self.controller.usuarios_matriculados_list()]
        self.mostrar_snackbar(f"Torneo '{nombre}' agregado exitosamente.", "SUCCESS")
        self.page.dialog.open = False
        self.page.update()

    def on_torneo_click(self, torneo_id):
        self.asistencias_list.controls.clear()
        asistencias = self.controller.get_asistencias_by_torneo(torneo_id)
        if not asistencias:
            self.asistencias_list.controls.append(ft.Text("No hay asistencias para este torneo."))
        else:
            for asis in asistencias:
                user_obj = self.controller.get_user_by_id(asis.usuario_id)
                nombre_usuario = user_obj.nombre if user_obj else f"Usuario ID={asis.usuario_id}"
                self.asistencias_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON),
                        title=ft.Text(f"{nombre_usuario} (Puesto: {asis.puesto})")
                    )
                )
        self.page.update()

    def actualizar_data_torneos(self):
        torneos_actualizados = self.controller.cargar_torneos()
        self.dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in torneos_actualizados]
        self.torneo_id_map = {torneo.nombre: torneo.id for torneo in torneos_actualizados}

        self.torneos_list.controls.clear()
        self.torneos_list.controls.extend([
            ft.ListTile(
                title=ft.Text(torneo.nombre),
                on_click=lambda e, t=torneo.id: self.on_torneo_click(t),
                data=torneo.id
            )
            for torneo in torneos_actualizados
        ])

        self.dropdown_usuarios.options = [ft.dropdown.Option(usuario.nombre) for usuario in self.controller.usuarios_matriculados_list()]
        self.page.update()

    def get_contenedor(self):
        """Retorna el contenedor principal para integrarlo en la vista."""
        return self.torneos_view
    
class ContenedorTorneos:
    def __init__(self, controller, torneos, page, usuario_id):
        self.controller = controller
        self.torneos = torneos
        self.page = page
        self.usuario_id = usuario_id

        # Dropdown de torneos disponibles (ya que el usuario es el mismo, no se requiere seleccionar usuario)
        self.dropdown_torneos = ft.Dropdown(
            label="Seleccione un torneo",
            options=[ft.dropdown.Option(torneo.nombre) for torneo in torneos],
            value=None
        )

        # Campos para filtrar por año y mes
        self.anio_field = ft.TextField(label="Año", hint_text="YYYY")
        self.mes_field = ft.TextField(label="Mes", hint_text="MM")

        # Botón para filtrar torneos
        self.filtrar_button = ft.ElevatedButton(
            "Filtrar",
            on_click=self.filtrar_torneos
        )

        # Botón para inscribirse en el torneo seleccionado
        self.inscribir_button = ft.ElevatedButton(
            "Inscribirme",
            icon=ft.icons.CHECK,
            on_click=self.inscribir_a_torneo
        )

        # Lista para mostrar torneos (disponibles o inscritos)
        self.torneos_list = ft.ListView(expand=True, spacing=10)

        # Contenedor para filtros
        self.filtros_container = ft.Container(
            content=ft.Row(
                controls=[self.anio_field, self.mes_field, self.filtrar_button],
                spacing=10,
            ),
            padding=10
        )

        # Contenedor principal con las secciones:
        # - Dropdown e inscribir
        # - Filtros para búsqueda
        # - Lista de torneos
        self.contenedor = ft.Column(
            controls=[
                ft.Text("Torneos Disponibles", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.dropdown_torneos,
                            self.inscribir_button
                        ],
                        spacing=10
                    ),
                    padding=10,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=10,
                    width=300
                ),
                self.filtros_container,
                ft.Divider(height=10, thickness=2),
                ft.Text("Listado de Torneos", size=20, weight=ft.FontWeight.BOLD),
                self.torneos_list,
            ],
            spacing=20,
            expand=True
        )

        # Inicialmente se muestran todos los torneos disponibles
        self.mostrar_torneos_disponibles()

    def mostrar_snackbar(self, mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

    def mostrar_torneos_disponibles(self, torneos_filtrados=None):
        """Muestra la lista de torneos disponibles (filtrados o completos)."""
        self.torneos_list.controls.clear()
        torneos_a_mostrar = torneos_filtrados if torneos_filtrados is not None else self.torneos
        if not torneos_a_mostrar:
            self.torneos_list.controls.append(ft.Text("No hay torneos disponibles."))
        else:
            for torneo in torneos_a_mostrar:
                self.torneos_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(torneo.nombre),
                        subtitle=ft.Text(f"Fecha: {torneo.fecha}"),
                        on_click=lambda e, t=torneo.id: self.ver_detalle_torneo(t)
                    )
                )
        self.page.update()

    def ver_detalle_torneo(self, torneo_id):
        """Muestra detalles del torneo seleccionado, junto con la opción de inscribirse si aún no lo está."""
        # Buscar torneo por id
        torneo = next((t for t in self.torneos if t.id == torneo_id), None)
        if not torneo:
            self.mostrar_snackbar("Torneo no encontrado.", "ERROR")
            return

        # Verificar si el usuario ya está inscrito en este torneo
        asistencias = self.controller.get_asistencias_by_torneo(torneo_id)
        inscrito = any(asis.usuario_id == self.usuario_id for asis in asistencias)

        detalle = ft.Column(
            controls=[
                ft.Text(f"Torneo: {torneo.nombre}", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Fecha: {torneo.fecha}"),
                ft.Text("Ya inscrito" if inscrito else "No inscrito"),
                ft.ElevatedButton(
                    "Inscribirme" if not inscrito else "Ya inscrito",
                    on_click=lambda e: self.inscribir_a_torneo(e, torneo_id),
                    disabled=inscrito
                ),
                ft.ElevatedButton(
                    "Regresar",
                    on_click=lambda e: self.mostrar_torneos_disponibles()
                )
            ],
            spacing=10
        )
        self.torneos_list.controls.clear()
        self.torneos_list.controls.append(detalle)
        self.page.update()

    def inscribir_a_torneo(self, e, torneo_id=None):
        """Permite inscribirse al torneo seleccionado. Si torneo_id no se pasa, se toma del dropdown."""
        # Si no se pasó torneo_id, se toma del dropdown
        if torneo_id is None:
            torneo_nombre = self.dropdown_torneos.value
            if not torneo_nombre:
                self.mostrar_snackbar("Seleccione un torneo para inscribirse.", "ERROR")
                return
            # Buscar torneo por nombre
            torneo = next((t for t in self.torneos if t.nombre == torneo_nombre), None)
            if not torneo:
                self.mostrar_snackbar("El torneo seleccionado no existe.", "ERROR")
                return
            torneo_id = torneo.id

        try:
            asistencias = self.controller.get_asistencias_by_torneo(torneo_id)
            # Verificar si ya existe inscripción para este usuario
            if any(asis.usuario_id == self.usuario_id for asis in asistencias):
                self.mostrar_snackbar("Ya estás inscrito en este torneo.", "ERROR")
                return

            # Crear la asistencia para el usuario
            Asistencia_Torneo.crear_asistencia(
                torneo_id=torneo_id,
                usuario_id=self.usuario_id,
                puesto=0  # Se puede definir un valor predeterminado para el puesto
            )
            self.mostrar_snackbar("Inscripción exitosa.", "SUCCESS")
        except Exception as ex:
            self.mostrar_snackbar(f"Error al inscribirse: {ex}", "ERROR")
        self.page.update()

    def filtrar_torneos(self, e):
        """Filtra los torneos disponibles según el año y mes ingresados."""
        anio = self.anio_field.value.strip()
        mes = self.mes_field.value.strip()
        torneos_filtrados = self.torneos

        if anio:
            torneos_filtrados = [t for t in torneos_filtrados if t.fecha.startswith(anio)]
        if mes:
            torneos_filtrados = [t for t in torneos_filtrados if "-"+mes.zfill(2)+"-" in t.fecha]

        self.mostrar_torneos_disponibles(torneos_filtrados)

    def get_contenedor(self):
        """Retorna el contenedor principal para integrarlo en la vista."""
        return self.contenedor





