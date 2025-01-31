import flet as ft
import json
from modelos.entrenamiento import Entrenamiento
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento
from modelos.base_model import BaseModel

def create_entrenamientos_view(controller, page):
    """
    Crea y retorna la vista de gestión de entrenamientos, incluyendo los componentes internos.
    
    Parámetros:
        controller (ClubController): Controlador que maneja la lógica de negocio.
        page (ft.Page): Página principal de Flet.
    
    Retorna:
        tuple: (entrenamientos_view, entrenamientos_list, dropdown_entrenamientos, actualizar_entrenamientos)
    """

    # ----------------------------------------------------------------
    #   Utilidades
    # ----------------------------------------------------------------

    def mostrar_snackbar(mensaje, tipo="INFO"):
        """Muestra un SnackBar con un mensaje y color dependiendo del tipo."""
        color = (
            ft.colors.GREEN
            if tipo == "SUCCESS" else
            ft.colors.RED
            if tipo == "ERROR" else
            ft.colors.BLUE_GREY
        )
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    # ----------------------------------------------------------------
    #   1. CREAR ENTRENAMIENTO
    # ----------------------------------------------------------------

    def crear_entrenamiento_dialog(e):
        """Abre un diálogo para que el usuario ingrese la fecha del entrenamiento."""
        fecha_input = ft.TextField(label="Fecha del Entrenamiento (YYYY-MM-DD)", autofocus=True)

        def confirmar_creacion_entrenamiento(ev):
            """Confirma la creación del entrenamiento al presionar el botón 'Crear'."""
            fecha_input_raw = fecha_input.value.strip()
            if not fecha_input_raw:
                mostrar_snackbar("Por favor, ingresa la fecha del entrenamiento.", "ERROR")
                return

            # Intentar dividir y validar la fecha ingresada
            partes_fecha = fecha_input_raw.split('-')
            if len(partes_fecha) == 3:
                anio, mes, dia = partes_fecha
                # Añadir ceros si son necesarios
                mes = mes.zfill(2)
                dia = dia.zfill(2)
                fecha = f"{anio}-{mes}-{dia}"

                # Validar formato de fecha
                try:
                    import datetime
                    datetime.datetime.strptime(fecha, "%Y-%m-%d")
                except ValueError:
                    mostrar_snackbar("Formato de fecha inválido. Usa YYYY-MM-DD.", "ERROR")
                    return
            else:
                mostrar_snackbar("Formato de fecha inválido. Debe ser AAAA-MM-DD.", "ERROR")
                return

            # Crear nuevo Entrenamiento y proceder como antes
            nuevo_id = Entrenamiento.nuevo_id()
            nuevo_entrenamiento = Entrenamiento(id=nuevo_id, fecha=fecha)
            nuevo_entrenamiento.guardar()

            # Para cada usuario MATRICULADO, crear asistencia con estado "pendiente"
            usuarios_matriculados = controller.filtrar_usuarios("matriculado")
            for u in usuarios_matriculados:
                nueva_asistencia = Asistencia_Entrenamiento(
                    id=Asistencia_Entrenamiento.nuevo_id(),
                    usuario_id=u.id,
                    entrenamiento_id=nuevo_id,
                    estado="pendiente"
                )
                nueva_asistencia.guardar()

            mostrar_snackbar(f"Entrenamiento '{fecha}' creado exitosamente.", "SUCCESS")
            page.dialog.open = False
            page.update()

            # Actualizar sets y dropdowns inmediatamente después de guardar el nuevo entrenamiento
            fecha_partes = fecha.split("-")
            if len(fecha_partes) == 3:
                anio, mes, _ = fecha_partes
                anios_disponibles.add(anio)
                meses_disponibles.add(mes)
                dropdown_anio.options = [ft.dropdown.Option(a) for a in sorted(anios_disponibles)]
                dropdown_mes.options = [ft.dropdown.Option(m) for m in sorted(meses_disponibles)]
                dropdown_anio.update()
                dropdown_mes.update()

            # Actualizar la lista y el dropdown de entrenamientos
            actualizar_entrenamientos()


        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Nuevo Entrenamiento"),
            content=ft.Column([fecha_input], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo_crear()),
                ft.TextButton("Crear", on_click=confirmar_creacion_entrenamiento),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def cerrar_dialogo_crear():
        page.dialog.open = False
        page.update()

    # ----------------------------------------------------------------
    #   2. TOMAR ASISTENCIA (seleccionando un entrenamiento en un dropdown)
    # ----------------------------------------------------------------

    entrenamientos_iniciales = controller.cargar_entrenamientos()  # Lista de objetos Entrenamiento

    dropdown_entrenamientos = ft.Dropdown(
        label="Seleccionar Entrenamiento para tomar asistencia",
        width=300,
        options=[ft.dropdown.Option(ent.fecha) for ent in entrenamientos_iniciales],
        on_change=lambda e: mostrar_asistencia_entrenamiento(e.control.value),
    )

    # Contenedor donde se mostrarán los usuarios y su asistencia (columna izquierda)
    asistencia_detalles_list = ft.ListView(expand=True, spacing=10)

    def mostrar_asistencia_entrenamiento(fecha_entrenamiento):
        """
        Cuando se selecciona un entrenamiento en el dropdown (columna izquierda),
        se listan los usuarios (pendientes, ausentes o presentes)
        y se permite cambiar el estado de asistencia.
        """
        if not fecha_entrenamiento:
            return

        # Encontrar el objeto Entrenamiento según la fecha
        try:
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos_data = json.load(archivo)
            entrenamiento_data = next((t for t in entrenamientos_data if t["fecha"] == fecha_entrenamiento), None)
        except (FileNotFoundError, json.JSONDecodeError):
            entrenamiento_data = None

        if not entrenamiento_data:
            mostrar_snackbar("No se encontró el entrenamiento seleccionado.", "ERROR")
            return

        entrenamiento_id = entrenamiento_data["id"]

        # Cargar asistencias y usuarios
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
            usuarios_dict = {u["id"]: u["nombre"] for u in usuarios}
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios_dict = {}

        # Filtrar la asistencia del entrenamiento seleccionado
        asistencia_entrenamiento = [a for a in asistencias if a["entrenamiento_id"] == entrenamiento_id]

        asistencia_detalles_list.controls.clear()

        if not asistencia_entrenamiento:
            asistencia_detalles_list.controls.append(
                ft.Text("No hay asistencias registradas para este entrenamiento.")
            )
        else:
            for a in asistencia_entrenamiento:
                usuario_id = a["usuario_id"]
                estado_actual = a["estado"]
                usuario_nombre = usuarios_dict.get(usuario_id, "Usuario no encontrado")

                # Dropdown para cambiar el estado (ausente, presente, pendiente)
                estado_dropdown = ft.Dropdown(
                    width=100,
                    options=[
                        ft.dropdown.Option("pendiente"),
                        ft.dropdown.Option("ausente"),
                        ft.dropdown.Option("presente"),
                    ],
                    value=estado_actual,
                    on_change=lambda e, asistencia_id=a["id"]: actualizar_estado_asistencia(e, asistencia_id),
                )

                asistencia_detalles_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(usuario_nombre, width=200),
                            estado_dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )

        page.update()

    def actualizar_estado_asistencia(e, asistencia_id):
        """
        Actualiza el estado (ausente, presente, pendiente) de la asistencia
        en el archivo JSON correspondiente.
        """
        nuevo_estado = e.control.value
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        for a in asistencias:
            if a["id"] == asistencia_id:
                a["estado"] = nuevo_estado
                break

        BaseModel.guardar_datos("asistencia_entrenamientos.json", asistencias)
        mostrar_snackbar(f"Estado de la asistencia actualizado a '{nuevo_estado}'.", "SUCCESS")
        page.update()

    # ----------------------------------------------------------------
    #   3. ASISTENCIAS POR ENTRENAMIENTO (columna derecha)
    #       * Inicialmente vacía *
    #       * Solo se llena al hacer clic en un entrenamiento del centro *
    # ----------------------------------------------------------------

    asistencias_por_entrenamiento_list = ft.ListView(expand=True, spacing=10)

    def mostrar_asistencia_entrenamiento_derecha(entrenamiento_id):
        """
        Muestra las asistencias de un entrenamiento específico (columna derecha),
        usando la misma lógica de carga, pero filtrado por ID de entrenamiento.
        """
        # Cargar entrenamientos
        try:
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos_data = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            entrenamientos_data = []

        ent_obj = next((e for e in entrenamientos_data if e["id"] == entrenamiento_id), None)
        if not ent_obj:
            mostrar_snackbar("Entrenamiento no encontrado.", "ERROR")
            return

        fecha_entrenamiento = ent_obj["fecha"]

        # Cargar asistencias y usuarios
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias_data = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias_data = []

        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios_data = json.load(archivo)
            usuarios_dict = {u["id"]: u["nombre"] for u in usuarios_data}
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios_dict = {}

        # Filtrar solo las asistencias del entrenamiento seleccionado
        asistencia_entrenamiento = [
            a for a in asistencias_data if a["entrenamiento_id"] == entrenamiento_id
        ]

        # Limpiar la vista antes de llenar
        asistencias_por_entrenamiento_list.controls.clear()

        if not asistencia_entrenamiento:
            asistencias_por_entrenamiento_list.controls.append(
                ft.Text("No hay asistencias registradas para este entrenamiento.")
            )
        else:
            for a in asistencia_entrenamiento:
                usuario_id = a["usuario_id"]
                estado_actual = a["estado"]
                usuario_nombre = usuarios_dict.get(usuario_id, "Usuario no encontrado")

                # Mismo dropdown para permitir cambiar el estado
                estado_dropdown = ft.Dropdown(
                    width=100,
                    options=[
                        ft.dropdown.Option("pendiente"),
                        ft.dropdown.Option("ausente"),
                        ft.dropdown.Option("presente"),
                    ],
                    value=estado_actual,
                    on_change=lambda e, asistencia_id=a["id"]: actualizar_estado_asistencia(e, asistencia_id),
                )

                asistencias_por_entrenamiento_list.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{usuario_nombre}"),
                            estado_dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )

        page.update()

    # ----------------------------------------------------------------
    #   4. FILTRAR ENTRENAMIENTOS POR AÑO Y MES (columna central)
    # ----------------------------------------------------------------

    # Dropdowns para año y mes
    anios_disponibles = set()
    meses_disponibles = set()

    # Extraer año y mes de cada entrenamiento
    for ent in controller.cargar_entrenamientos():
        fecha_partes = ent.fecha.split("-")  # asumiendo formato YYYY-MM-DD
        if len(fecha_partes) == 3:
            anio, mes, _ = fecha_partes
            anios_disponibles.add(anio)
            meses_disponibles.add(mes)

    # Convertir a listas ordenadas
    anios_ordenados = sorted(list(anios_disponibles))
    meses_ordenados = sorted(list(meses_disponibles))

    dropdown_anio = ft.Dropdown(
        label="Filtrar por Año",
        options=[ft.dropdown.Option(a) for a in anios_ordenados],
        width=120,
    )

    dropdown_mes = ft.Dropdown(
        label="Filtrar por Mes",
        options=[ft.dropdown.Option(m) for m in meses_ordenados],
        width=80,
    )

    # Lista donde se mostrarán los entrenamientos filtrados (columna central)
    entrenamientos_list = ft.ListView(expand=True, spacing=10)

    def filtrar_entrenamientos(e):
        """Filtra la lista de entrenamientos por el año y mes seleccionados."""
        anio = dropdown_anio.value
        mes = dropdown_mes.value

        entrenamientos_filtrados = []
        for ent in controller.cargar_entrenamientos():
            partes = ent.fecha.split("-")
            if len(partes) == 3:
                y, m, _ = partes
                if (not anio or y == anio) and (not mes or m == mes):
                    entrenamientos_filtrados.append(ent)

        # Actualizamos la lista
        entrenamientos_list.controls.clear()
        for ent in entrenamientos_filtrados:
            entrenamientos_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"ID: {ent.id} - Fecha: {ent.fecha}"),
                    on_click=lambda e, this_id=ent.id: click_entrenamiento_central(this_id),
                )
            )
        entrenamientos_list.update()

    def click_entrenamiento_central(entrenamiento_id):
        """
        Al hacer clic en un entrenamiento de la lista central,
        mostrar la asistencia correspondiente en la columna derecha.
        """
        mostrar_asistencia_entrenamiento_derecha(entrenamiento_id)

    # Botón para aplicar el filtro
    btn_filtrar = ft.ElevatedButton(
        text="Aplicar Filtro",
        icon=ft.icons.SEARCH,
        on_click=filtrar_entrenamientos
    )

    def actualizar_entrenamientos():
        """
        Refresca la lista de entrenamientos sin filtro y actualiza los dropdowns de año y mes.
        """
        # Limpia los sets para recalcular con los datos actualizados
        anios_disponibles.clear()
        meses_disponibles.clear()

        entrenamientos_list.controls.clear()
        for ent in controller.cargar_entrenamientos():
            fecha_partes = ent.fecha.split("-")
            if len(fecha_partes) == 3:
                anio, mes, _ = fecha_partes
                anios_disponibles.add(anio)
                meses_disponibles.add(mes)

            entrenamientos_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"ID: {ent.id} - Fecha: {ent.fecha}"),
                    on_click=lambda e, this_id=ent.id: click_entrenamiento_central(this_id),
                )
            )

        # Actualizar opciones del dropdown
        dropdown_anio.options = [ft.dropdown.Option(a) for a in sorted(anios_disponibles)]
        dropdown_mes.options = [ft.dropdown.Option(m) for m in sorted(meses_disponibles)]

        entrenamientos_list.update()


    # ----------------------------------------------------------------
    #   5. CONSTRUCCIÓN DE LA VISTA PRINCIPAL
    # ----------------------------------------------------------------

    # BOTÓN PARA CREAR ENTRENAMIENTO
    crear_entrenamiento_button = ft.ElevatedButton(
        text="Crear Entrenamiento",
        icon=ft.icons.ADD,
        on_click=crear_entrenamiento_dialog
    )

    # BOTÓN PARA REFRESCAR TODA LA LISTA DE ENTRENAMIENTOS (sin filtro)
    refrescar_entrenamientos_button = ft.ElevatedButton(
        text="Refrescar Entrenamientos",
        icon=ft.icons.REFRESH,
        on_click=lambda e: actualizar_entrenamientos()
    )

    # Columna izquierda: Crear y tomar asistencia
    izquierda = ft.Container(
        ft.Column(
            [
                ft.Text("GESTIÓN DE ENTRENAMIENTOS", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                crear_entrenamiento_button,
                refrescar_entrenamientos_button,
                ft.Divider(),
                ft.Text("Tomar Asistencia", size=16, weight=ft.FontWeight.BOLD),
                dropdown_entrenamientos,
                ft.Divider(height=2, thickness=1),
                ft.Text("Usuarios en este entrenamiento:", size=14),
                ft.Container(asistencia_detalles_list, expand=True),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
        width=350,
        padding=20,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=10,
    )

    # Columna central: Filtrar entrenamientos y ver lista
    centro = ft.Container(
        ft.Column(
            [
                ft.Text("Entrenamientos Disponibles", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row(
                    [
                        dropdown_anio,
                        dropdown_mes,
                        btn_filtrar,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(),
                ft.Container(entrenamientos_list, expand=True),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
        expand=True,
        padding=20,
    )

    # Columna derecha: Asistencias por Entrenamiento (inicialmente vacía)
    asistencias_view = ft.Container(
        ft.Column(
            [
                ft.Text("Asistencias por Entrenamiento", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(asistencias_por_entrenamiento_list, expand=True),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
        expand=True,
        padding=20,
    )

    entrenamientos_view = ft.Row(
        [
            izquierda,
            ft.VerticalDivider(width=1),
            centro,
            ft.VerticalDivider(width=1),
            asistencias_view,
        ],
        expand=True,
    )

    # Cargamos inicialmente la lista de entrenamientos
    #actualizar_entrenamientos()

    # Devolver la vista y elementos clave, incluyendo actualizar_entrenamientos
    return entrenamientos_view, entrenamientos_list, dropdown_entrenamientos, actualizar_entrenamientos
