# tallerdiseno1/views/informes_view.py
import flet as ft
import json
from datetime import datetime
from modelos.informe import Informe
from modelos.base_model import BaseModel

class ContenedorInformeSuper:
    def __init__(self, controller, page):
        self.controller = controller
        self.page = page

        # -----------------------------------------------------------
        # Elementos de UI y variables
        # -----------------------------------------------------------
        # Columna 1: Opciones para generar informes
        self.input_anio_col1 = ft.TextField(
            label="Año",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.input_mes_col1 = ft.TextField(
            label="Mes",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        col1 = ft.Column(
            controls=[
                ft.Text("Opciones", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.input_anio_col1,
                self.input_mes_col1,
                ft.ElevatedButton("Generar Informes", on_click=self.on_generar_informes_click),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=False
        )

        # Columna 2: Selección de año y mes y filtro por usuario
        self.input_anio = ft.TextField(
            label="Año",
            width=100,
            hint_text="2025",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.input_mes = ft.TextField(
            label="Mes",
            width=100,
            hint_text="01",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        col2_1 = ft.Column(
            controls=[
                ft.Text("Seleccionar Año y Mes", weight=ft.FontWeight.BOLD),
                ft.Row([self.input_anio, self.input_mes]),
            ],
            spacing=10,
        )

        self.usuarios_listview = ft.ListView(expand=True, spacing=5)
        # Construir la lista de usuarios matriculados
        matriculados = self.controller.filtrar_usuarios("matriculado")
        for u in matriculados:
            self.usuarios_listview.controls.append(
                ft.ListTile(
                    title=ft.Text(u.nombre),
                    subtitle=ft.Text(f"ID: {u.id}"),
                    on_click=lambda e, uid=u.id: self.on_user_click(e, uid)
                )
            )
        btn_limpiar_filtro = ft.ElevatedButton("Deseleccionar usuario", on_click=self.limpiar_filtro_usuario)
        col2_2 = ft.ListView(
            controls=[
                ft.ListTile(title=ft.Text("Usuarios Matriculados")),
                ft.Container(self.usuarios_listview, expand=True, height=300),
                btn_limpiar_filtro,
            ],
            expand=True
        )
        col2 = ft.Column(
            controls=[col2_1, col2_2],
            spacing=20,
            expand=False
        )

        # Columna 3: Contenedor para mostrar informes
        self.informe_container = ft.ListView([], expand=True)
        col3 = ft.Container(
            content=self.informe_container,
            expand=True
        )

        # Calcular anchos para cada columna (Columna 1 ancho fijo)
        col1_width = 180
        available_width = page.width - col1_width - 2  # 2 para los divisores
        col2_and_3_width = available_width / 3

        self.informes_view = ft.Row(
            controls=[
                ft.Container(col1, width=180, padding=10),
                ft.VerticalDivider(width=1),
                ft.Container(col2, width=col2_and_3_width, padding=10),
                ft.VerticalDivider(width=1),
                ft.Container(col3, width=col2_and_3_width * 2, padding=10),
            ],
            expand=True
        )

        # Variable para manejar el filtro por usuario
        self.selected_user_id = None

    # -----------------------------------------------------------
    # Funciones de apoyo (convertidas a métodos)
    # -----------------------------------------------------------
    def cargar_asistencia_entrenamientos(self):
        try:
            return BaseModel.cargar_datos("asistencia_entrenamientos.json")
        except:
            return []

    def cargar_asistencia_torneos(self):
        try:
            return BaseModel.cargar_datos("asistencia_torneos.json")
        except:
            return []

    def cargar_torneos(self):
        torneos = self.controller.cargar_torneos()  # Retorna lista de objetos Torneo
        return {t.id: (t.nombre, t.fecha) for t in torneos}

    def cargar_entrenamientos(self):
        entrenamientos = self.controller.cargar_entrenamientos()
        return {e.id: e.fecha for e in entrenamientos}

    def extraer_mes_anio_de_fecha(self, fecha_str):
        if not fecha_str:
            return (None, None)
        try:
            dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            return (dt.year, dt.month)
        except:
            return (None, None)

    def generar_id_informe(self, informes_existentes):
        if not informes_existentes:
            return 1
        else:
            max_id = max(inf["id"] for inf in informes_existentes)
            return max_id + 1

    def crear_informes(self, anio, mes):
        # Validaciones básicas
        if not anio.isdigit() or not mes.isdigit():
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Año y mes deben ser números."), bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        anio_int = int(anio)
        mes_int = int(mes)
        if not (1 <= mes_int <= 12):
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Mes debe estar entre 1 y 12."), bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Cargar datos
        asistencia_entrenamientos = self.cargar_asistencia_entrenamientos()
        asistencia_torneos = self.cargar_asistencia_torneos()
        dict_torneos = self.cargar_torneos()
        dict_entrenamientos = self.cargar_entrenamientos()

        # Cargar informes existentes
        try:
            with open("base_de_datos/informes.json", "r") as f:
                content = f.read().strip()
                if content:
                    informes_existentes = json.loads(content)
                else:
                    informes_existentes = []
        except:
            informes_existentes = []

        # Remover informes existentes para este mes/año
        informes_nuevos = [inf for inf in informes_existentes
                           if not (str(inf["anio"]) == str(anio_int) and str(inf["mes"]).zfill(2) == str(mes_int).zfill(2))]

        usuarios_matriculados = self.controller.filtrar_usuarios("matriculado")

        for usuario in usuarios_matriculados:
            user_id = usuario.id

            # Calcular clases del mes y clases asistidas
            clases_del_mes = 0
            clases_asistidas = 0

            for a_e in asistencia_entrenamientos:
                if a_e["usuario_id"] == user_id:
                    ent_id = a_e["entrenamiento_id"]
                    fecha_ent = dict_entrenamientos.get(ent_id, None)
                    if fecha_ent:
                        ent_anio, ent_mes = self.extraer_mes_anio_de_fecha(fecha_ent)
                        if ent_anio == anio_int and ent_mes == mes_int:
                            clases_del_mes += 1
                            if a_e.get("estado", "") == "presente":
                                clases_asistidas += 1

            # Calcular torneos asistidos y top 3 torneos
            torneos_asistidos = 0
            torneos_del_usuario = []

            for a_t in asistencia_torneos:
                if a_t["usuario_id"] == user_id:
                    t_id = a_t["torneo_id"]
                    torneo_data = dict_torneos.get(t_id, None)
                    if not torneo_data:
                        continue
                    torneo_nombre, torneo_fecha = torneo_data
                    t_anio, t_mes = self.extraer_mes_anio_de_fecha(torneo_fecha)
                    if t_anio == anio_int and t_mes == mes_int:
                        torneos_asistidos += 1
                        torneos_del_usuario.append((a_t.get("puesto", 9999), torneo_nombre))

            # Ordenar por mejor puesto (menor es mejor)
            torneos_del_usuario.sort(key=lambda x: x[0])
            top_torneos_data = []
            for tupla in torneos_del_usuario[:3]:
                puesto, nombre_t = tupla
                top_torneos_data.append([nombre_t, puesto])

            nuevo_informe = {
                "id": self.generar_id_informe(informes_nuevos),
                "usuario_id": user_id,
                "mes": str(mes_int).zfill(2),
                "anio": str(anio_int),
                "clases_mes": clases_del_mes,
                "clases_asistidas": clases_asistidas,
                "torneos_asistidos": torneos_asistidos,
                "top_torneos": top_torneos_data
            }
            informes_nuevos.append(nuevo_informe)

        with open("base_de_datos/informes.json", "w") as f:
            json.dump(informes_nuevos, f, indent=4)

        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Informes generados para {mes_int:02d}/{anio_int}."),
            bgcolor=ft.colors.GREEN
        )
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_informes_en_container(self, anio, mes, user_id_filter=None):
        self.informe_container.controls.clear()

        try:
            with open("base_de_datos/informes.json", "r") as file:
                content = file.read().strip()
                if not content:
                    informes = []
                else:
                    informes = json.loads(content)
        except Exception as ex:
            print("Error al cargar informes:", ex)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al cargar informes: {str(ex)}"), 
                bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if anio and mes:
            mes = mes.zfill(2)
            informes_filtrados = [inf for inf in informes if str(inf["anio"]) == str(anio) and str(inf["mes"]) == str(mes)]
            if user_id_filter:
                informes_filtrados = [inf for inf in informes_filtrados if inf["usuario_id"] == user_id_filter]
        elif not anio and not mes and user_id_filter:
            informes_filtrados = [inf for inf in informes if inf["usuario_id"] == user_id_filter]
        else:
            informes_filtrados = []

        if user_id_filter is not None:
            informes_filtrados = [inf for inf in informes_filtrados if inf["usuario_id"] == user_id_filter]

        dict_usuarios = {u.id: u.nombre for u in self.controller.usuarios}

        for inf in informes_filtrados:
            self.display_informe(inf, dict_usuarios)

        self.page.update()

    def display_informe(self, inf, dict_usuarios):
        user_name = dict_usuarios.get(inf["usuario_id"], f"ID {inf['usuario_id']}")
        top_torneos_str = "\n".join([f"- {t[0]} (puesto {t[1]})" for t in inf["top_torneos"]])
        clases_del_mes = inf['clases_mes']
        clases_asistidas = inf['clases_asistidas']
        porcentaje_asistencia = (clases_asistidas / clases_del_mes * 100) if clases_del_mes > 0 else 0

        card = ft.Card(
            content=ft.Container(
                ft.Column([
                    ft.Text(f"Informe ID: {inf['id']}"),
                    ft.Text(f"Usuario: {user_name} (ID: {inf['usuario_id']})"),
                    ft.Text(f"Mes/Año: {inf['mes']}/{inf['anio']}"),
                    ft.Text(f"Clases del Mes: {inf['clases_mes']}"),
                    ft.Text(f"Clases Asistidas: {clases_asistidas} - {porcentaje_asistencia:.1f}%"),
                    ft.Text(f"Torneos Asistidos: {inf['torneos_asistidos']}"),
                    ft.Text("Top Torneos:"),
                    ft.Text(top_torneos_str if top_torneos_str else "Ninguno"),
                ]),
                padding=10
            ),
            width=300,
        )
        self.informe_container.controls.append(card)

    # -----------------------------------------------------------
    # Callbacks de UI (métodos de evento)
    # -----------------------------------------------------------
    def on_generar_informes_click(self, e):
        anio_val = self.input_anio_col1.value
        mes_val = self.input_mes_col1.value
        if not anio_val or not mes_val:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Debe ingresar año y mes"), bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not anio_val.isdigit() or not mes_val.isdigit():
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Año y mes deben ser números enteros."), bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        mes_val = mes_val.zfill(2)
        if not (1 <= int(mes_val) <= 12):
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Mes debe estar entre 1 y 12."), bgcolor=ft.colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.crear_informes(anio_val, mes_val)
        self.mostrar_informes_en_container(anio_val, mes_val, user_id_filter=None)

    def on_user_click(self, e, user_id):
        self.selected_user_id = user_id
        anio_val = self.input_anio.value
        mes_val = self.input_mes.value
        if not anio_val or not mes_val:
            return
        self.mostrar_informes_en_container(anio_val, mes_val, user_id_filter=self.selected_user_id)

    def limpiar_filtro_usuario(self, e):
        self.selected_user_id = None
        anio_val = self.input_anio.value
        mes_val = self.input_mes.value
        if anio_val and mes_val:
            self.mostrar_informes_en_container(anio_val, mes_val, user_id_filter=None)

    # En ContenedorInformeView, reemplaza el método get_contenedor existente por:
    def get_contenedor(self):
        """Retorna el contenedor principal para integrarlo en la vista."""
        return self.informes_view
class ContenedorInformeView:
    def __init__(self, controller, page, user_id):
        print("ContenedorInformeView")
        self.controller = controller
        self.page = page
        self.user_id = user_id

        # Dropdown para seleccionar el año
        self.dropdown_anio = ft.Dropdown(
            label="Seleccione el Año",
            options=[],
            on_change=self.on_anio_change
        )

        # Obtener años de los informes existentes para este usuario
        self.dropdown_anio.options = self.obtener_anios_disponibles()

        # Contenedor para los informes usando una Column que contendrá varias Row
        self.informes_container = ft.Column(
            controls=[],
            spacing=10
        )

        # Layout principal de la vista
        self.layout = ft.Column(
            controls=[
                self.dropdown_anio,
                self.informes_container
            ],
            spacing=10,
            expand=True
        )

    def obtener_anios_disponibles(self):
        """Retorna los años disponibles para los informes de este usuario."""
        try:
            with open("base_de_datos/informes.json", "r") as file:
                informes = json.load(file)
            anios = {str(inf["anio"]) for inf in informes if inf["usuario_id"] == self.user_id}
            # Usar ft.DropdownOption para crear las opciones
            return [ft.dropdown.Option(text=anio) for anio in sorted(anios, reverse=True)]
        except Exception as e:
            print(f"Error al cargar los informes: {e}")
            return []

    def cargar_informes_del_usuario(self, anio):
        """Carga y retorna informes del usuario específico para el año seleccionado."""
        try:
            with open("base_de_datos/informes.json", "r") as file:
                informes = json.load(file)
            informes_filtrados = [
                inf for inf in informes
                if inf["usuario_id"] == self.user_id and str(inf["anio"]) == anio
            ]
            return informes_filtrados
        except Exception as e:
            print(f"Error al cargar informes del usuario: {e}")
            return []

    def mostrar_informes(self, informes):
        """Muestra informes en filas de 4 tarjetas cada una."""
        self.informes_container.controls.clear()
        chunk_size = 4  # Número de tarjetas por fila
        for i in range(0, len(informes), chunk_size):
            chunk = informes[i:i + chunk_size]
            row_controls = [self.crear_informe_card(informe) for informe in chunk]
            row = ft.Row(
                controls=row_controls,
                spacing=10
            )
            self.informes_container.controls.append(row)
        self.page.update()

    def crear_informe_card(self, informe):
        """Crea una tarjeta visual para un informe, incluyendo toda la información:
           mes, anio, clases_mes, clases_asistidas, torneos_asistidos y top_torneos."""
        return ft.Card(
            content=ft.Column([
                ft.Text(f"Mes: {informe['mes']}/{informe['anio']}"),
                ft.Text(f"Clases Mes: {informe['clases_mes']}"),
                ft.Text(f"Clases Asistidas: {informe['clases_asistidas']}"),
                ft.Text(f"Torneos Asistidos: {informe['torneos_asistidos']}"),
                ft.Text(f"Top Torneos: {', '.join([f'{t[0]} (Puesto {t[1]})' for t in informe['top_torneos']])}")
            ]),
            width=300,
            height=200
        )

    def on_anio_change(self, event):
        """Evento al cambiar el año en el dropdown."""
        anio_seleccionado = event.control.value
        if anio_seleccionado:
            informes = self.cargar_informes_del_usuario(anio_seleccionado)
            self.mostrar_informes(informes)
    
    def get_contenedor(self):
        """Retorna el contenedor principal para integrarlo en la vista."""
        return self.layout




