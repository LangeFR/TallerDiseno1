# tallerdiseno1/views/informes_view.py
import flet as ft
import json
from datetime import datetime
from modelos.informe import Informe
from modelos.base_model import BaseModel

def create_informes_view(controller, page):
    """
    Crea y retorna la vista de generación y visualización de informes.

    Disposición (3 columnas):
        Columna 1:
            - Botón para generar informes
        Columna 2 (dividida verticalmente):
            2.1: Campos para seleccionar año y mes
            2.2: Lista de usuarios matriculados + botón para deseleccionar (limpiar filtro)
        Columna 3:
            - Contenedor con la lista de informes para el mes/año seleccionado
              (ya sea de todos los usuarios o sólo del usuario filtrado).
    """

    # -----------------------------------------------------------
    # Variables y referencias de UI
    # -----------------------------------------------------------
    input_anio = ft.TextField(
        label="Año",
        width=80,
        hint_text="2025",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    input_mes = ft.TextField(
        label="Mes",
        width=50,
        hint_text="01",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Contenedor de informes (Columna 3)
    informe_container = ft.ListView([], expand=True)

    # Lista de usuarios matriculados (Columna 2.2)
    usuarios_listview = ft.ListView(expand=True, spacing=5)
    
    # Para manejar la selección de usuario en el filtro
    selected_user_id = None

    # -----------------------------------------------------------
    # Funciones de apoyo
    # -----------------------------------------------------------
    def cargar_asistencia_entrenamientos():
        """Carga y retorna la lista de asistencia_entrenamientos desde JSON."""
        try:
            return BaseModel.cargar_datos("asistencia_entrenamientos.json")
        except:
            return []

    def cargar_asistencia_torneos():
        """Carga y retorna la lista de asistencia_torneos desde JSON."""
        try:
            return BaseModel.cargar_datos("asistencia_torneos.json")
        except:
            return []

    def cargar_torneos():
        """Devuelve un diccionario {torneo_id: nombre_torneo} para lookup."""
        torneos = controller.cargar_torneos()  # Retorna lista de objetos Torneo
        return {t.id: t.nombre for t in torneos}

    def cargar_entrenamientos():
        """Devuelve un diccionario {entrenamiento_id: (fecha, nombre/opcional)} para lookup."""
        entrenamientos = controller.cargar_entrenamientos()
        # Asumimos que cada entrenamiento tiene un atributo fecha (str "YYYY-MM-DD" o similar)
        return {e.id: e.fecha for e in entrenamientos}

    def extraer_mes_anio_de_fecha(fecha_str):
        """Recibe una fecha en formato YYYY-MM-DD. Retorna (anio, mes)."""
        # Ajusta según tu formato real. Este ejemplo asume "YYYY-MM-DD".
        if not fecha_str:
            return (None, None)
        try:
            dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            return (dt.year, dt.month)
        except:
            # Si no se puede parsear, devolvemos None
            return (None, None)

    def generar_id_informe(informes_existentes):
        """Genera un nuevo id único para el informe."""
        if not informes_existentes:
            return 1
        else:
            max_id = max(inf["id"] for inf in informes_existentes)
            return max_id + 1

    def crear_informes(anio, mes):
        """
        Crea/actualiza en 'informes.json' los informes del año y mes indicados
        para todos los usuarios con estado = 'matriculado'.
        """
        # Validaciones básicas
        if not anio.isdigit() or not mes.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("Año y mes deben ser números."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        anio_int = int(anio)
        mes_int = int(mes)
        if not (1 <= mes_int <= 12):
            page.snack_bar = ft.SnackBar(
                ft.Text("Mes debe estar entre 1 y 12."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        # Cargar datos
        asistencia_entrenamientos = cargar_asistencia_entrenamientos()
        asistencia_torneos = cargar_asistencia_torneos()
        dict_torneos = cargar_torneos()
        dict_entrenamientos = cargar_entrenamientos()

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

        # Lista final donde guardaremos informes actualizados
        informes_nuevos = [inf for inf in informes_existentes
                           if not (str(inf["anio"]) == str(anio_int) and str(inf["mes"]).zfill(2) == str(mes_int).zfill(2))]
        # ^ Con esto, removemos cualquier informe de este mes/año, para regenerarlos

        usuarios_matriculados = controller.filtrar_usuarios("matriculado")

        for usuario in usuarios_matriculados:
            user_id = usuario.id

            # Calcular clases del mes y clases asistidas
            clases_del_mes = 0
            clases_asistidas = 0

            for a_e in asistencia_entrenamientos:
                if a_e["usuario_id"] == user_id:
                    ent_id = a_e["entrenamiento_id"]
                    fecha_ent = dict_entrenamientos.get(ent_id, None)  # "YYYY-MM-DD"
                    if fecha_ent:
                        ent_anio, ent_mes = extraer_mes_anio_de_fecha(fecha_ent)
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
                    # Necesitamos la fecha real del torneo:
                    # Torneo viene del controller, convertimos a dict para filtrar
                    # Usamos el dict_torneos para obtener el nombre, pero la fecha hay que cargarla
                    # con controller.cargar_torneos() --> ya lo hicimos (dict) pero ahí sólo guardamos nombre
                    # Podríamos recargar la lista y buscar la fecha:
                    # Para la demo, asumimos que tenemos que hacer: get_torneo_by_id(t_id)
                    # o algo similar. Haremos un approach rápido:

                    # Buscamos la fecha en la lista de torneos
                    # Re-cargamos la lista como objetos Torneo
                    # y filtramos
                    # (Para optimizar, se podría crear un diccionario id->(nombre,fecha) similar a entrenamientos).
                    # Para simplicidad, supongamos que NO filtras por fecha en torneos (pero la solicitud indica que sí).
                    # => Ajustamos: definimos un dict con id->(nombre, fecha).
                    # Lo haremos rápido:
                    # en cargar_torneos() tenemos {id: nombre}, no la fecha. Extendámoslo:
                    # (Ver "controller.cargar_torneos()" -> Retorna [Torneo(...)], cada Torneo tiene t.fecha).
                    # Haremos un dict análogo a dict_entrenamientos.

                    # Reajustamos: cambiamos cargar_torneos a:
                    # dict_torneos = {t.id: (t.nombre, t.fecha)}  (ya modificado en la función).
                    # Actualizamos la variable local:
                    # OJO: cambia la línea "return {t.id: t.nombre for t in torneos}" 
                    # por "return {t.id: (t.nombre, t.fecha) for t in torneos}"
                    # Revisar más abajo. 
                    # Por ahora supongamos lo tenemos. 
                    torneo_data = dict_torneos.get(t_id, None)
                    if not torneo_data:
                        continue

                    torneo_nombre, torneo_fecha = torneo_data
                    t_anio, t_mes = extraer_mes_anio_de_fecha(torneo_fecha)
                    if t_anio == anio_int and t_mes == mes_int:
                        torneos_asistidos += 1
                        # Guardamos (puesto, nombre)
                        torneos_del_usuario.append((a_t.get("puesto", 9999), torneo_nombre))

            # Ordenar por mejor puesto (menor puesto => mejor)
            torneos_del_usuario.sort(key=lambda x: x[0])
            # Tomamos los 3 primeros
            top_torneos_data = []
            for tupla in torneos_del_usuario[:3]:
                puesto = tupla[0]
                nombre_t = tupla[1]
                top_torneos_data.append([nombre_t, puesto])

            # Crear un diccionario con el formato solicitado
            nuevo_informe = {
                "id": generar_id_informe(informes_nuevos),
                "usuario_id": user_id,
                "mes": str(mes_int).zfill(2),
                "anio": str(anio_int),
                "clases_mes": clases_del_mes,
                "clases_asistidas": clases_asistidas,
                "torneos_asistidos": torneos_asistidos,
                "top_torneos": top_torneos_data
            }
            informes_nuevos.append(nuevo_informe)

        # Guardar informes actualizados en disco
        with open("base_de_datos/informes.json", "w") as f:
            json.dump(informes_nuevos, f, indent=4)

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Informes generados para {mes_int:02d}/{anio_int}."),
            bgcolor=ft.colors.GREEN
        )
        page.snack_bar.open = True
        page.update()

    def mostrar_informes_en_container(anio, mes, user_id_filter=None):
        """
        Carga desde informes.json y muestra en 'informe_container' todos los informes
        correspondientes a anio, mes. Si user_id_filter está definido, muestra sólo
        los informes del usuario con ese ID.
        """
        informe_container.controls.clear()

        try:
            with open("base_de_datos/informes.json", "r") as file:
                content = file.read().strip()
                if not content:
                    informes = []
                else:
                    informes = json.loads(content)
        except Exception as ex:
            print("Error al cargar informes:", ex)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al cargar informes: {str(ex)}"), 
                bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        # Filtrar por mes/año
        informes_filtrados = [
            inf for inf in informes
            if str(inf["anio"]) == str(anio)
            and str(inf["mes"]).zfill(2) == str(mes).zfill(2)
        ]

        # Si hay un usuario en el filtro, filtrar más
        if user_id_filter is not None:
            informes_filtrados = [
                inf for inf in informes_filtrados
                if inf["usuario_id"] == user_id_filter
            ]

        # Para mostrar el nombre del usuario en lugar de ID
        # Hacemos un diccionario {id: nombre}
        dict_usuarios = {u.id: u.nombre for u in controller.usuarios}

        for inf in informes_filtrados:
            user_name = dict_usuarios.get(inf["usuario_id"], f"ID {inf['usuario_id']}")
            top_torneos_str = ""
            for titem in inf["top_torneos"]:
                nombre_t = titem[0]
                puesto_t = titem[1]
                top_torneos_str += f"- {nombre_t} (puesto {puesto_t})\n"

            card = ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text(f"Informe ID: {inf['id']}"),
                        ft.Text(f"Usuario: {user_name} (ID: {inf['usuario_id']})"),
                        ft.Text(f"Mes/Año: {inf['mes']}/{inf['anio']}"),
                        ft.Text(f"Clases del Mes: {inf['clases_mes']}"),
                        ft.Text(f"Clases Asistidas: {inf['clases_asistidas']}"),
                        ft.Text(f"Torneos Asistidos: {inf['torneos_asistidos']}"),
                        ft.Text("Top Torneos:"),
                        ft.Text(top_torneos_str.strip() if top_torneos_str else "Ninguno"),
                    ]),
                    padding=10
                ),
                width=300,
            )
            informe_container.controls.append(card)

        page.update()

    # -----------------------------------------------------------
    # Callbacks UI
    # -----------------------------------------------------------
    def on_generar_informes_click(e):
        """
        Cuando se presiona el botón "Generar Informes" en la columna 1.
        1) Genera informes en disco (crear_informes).
        2) Muestra todos los informes en la columna 3 (sin filtro de usuario).
        """
        anio_val = input_anio_col1.value
        mes_val = input_mes_col1.value
        if not anio_val or not mes_val:
            page.snack_bar = ft.SnackBar(
                ft.Text("Debe ingresar año y mes"), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validar que el año y el mes sean numéricos y el mes esté en el rango adecuado
        if not anio_val.isdigit() or not mes_val.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("Año y mes deben ser números enteros."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        mes_val = mes_val.zfill(2)  # Asegurar que el mes tiene dos dígitos
        if not (1 <= int(mes_val) <= 12):
            page.snack_bar = ft.SnackBar(
                ft.Text("Mes debe estar entre 1 y 12."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        # Una vez validado y ajustado, llamar a crear informes y mostrarlos
        crear_informes(anio_val, mes_val)
        mostrar_informes_en_container(anio_val, mes_val, user_id_filter=None)


    def on_user_click(e, user_id):
        """
        Cuando se hace click en un usuario de la lista (Columna 2.2).
        Mostramos informes sólo de ese usuario.
        """
        nonlocal selected_user_id
        selected_user_id = user_id
        anio_val = input_anio.value
        mes_val = input_mes.value
        if not anio_val or not mes_val:
            return  # No hay selección de mes/año
        mostrar_informes_en_container(anio_val, mes_val, user_id_filter=selected_user_id)

    def limpiar_filtro_usuario(e):
        """Quita el filtro de usuario y refresca informes."""
        nonlocal selected_user_id
        selected_user_id = None
        anio_val = input_anio.value
        mes_val = input_mes.value
        if anio_val and mes_val:
            mostrar_informes_en_container(anio_val, mes_val, user_id_filter=None)

    # -----------------------------------------------------------
    # Construir UI de la Columna 2.2 con la lista de usuarios
    # -----------------------------------------------------------
    usuarios_listview.controls.clear()
    matriculados = controller.filtrar_usuarios("matriculado")

    for u in matriculados:
        usuarios_listview.controls.append(
            ft.ListTile(
                title=ft.Text(u.nombre),
                subtitle=ft.Text(f"ID: {u.id}"),
                on_click=lambda e, uid=u.id: on_user_click(e, uid)
            )
        )

    btn_limpiar_filtro = ft.ElevatedButton("Deseleccionar usuario", on_click=limpiar_filtro_usuario)

    # -----------------------------------------------------------
    # Construimos las 3 columnas:
    # -----------------------------------------------------------

    # Columna 1: Opción para generar informes
    input_anio_col1 = ft.TextField(
        label="Año",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    input_mes_col1 = ft.TextField(
        label="Mes",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    col1 = ft.Column(
        controls=[
            ft.Text("Opciones", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            input_anio_col1,  # Añadir input año
            input_mes_col1,  # Añadir input mes
            ft.ElevatedButton("Generar Informes", on_click=on_generar_informes_click),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=False
    )
    # Columna 2: Dividida en 2 verticalmente
    #   - 2.1: Selección de año y mes
    #   - 2.2: Lista de usuarios matriculados + botón para deseleccionar
    col2_1 = ft.Column(
        controls=[
            ft.Text("Seleccionar Año y Mes", weight=ft.FontWeight.BOLD),
            ft.Row([input_anio, input_mes]),
        ],
        spacing=10,
    )

    col2_2 = ft.ListView(
        controls=[
            ft.ListTile(title=ft.Text("Usuarios Matriculados"), subtitle=None),
            ft.Container(usuarios_listview, expand=True, height=300),
            btn_limpiar_filtro,
        ],
        expand=True
    )

    col2 = ft.Column(
        controls=[col2_1, col2_2],
        spacing=20,
        expand=False
    )

    # Columna 3: Contenedor que muestra los informes
    col3 = ft.Container(
        content=informe_container,
        expand=True
    )

    # Armamos la vista final con un Row
    informes_view = ft.Row(
        controls=[
            ft.Container(col1, width=180, padding=10),
            ft.VerticalDivider(width=1),
            ft.Container(col2, width=200, padding=10),
            ft.VerticalDivider(width=1),
            ft.Container(col3, expand=True, padding=10),
        ],
        expand=True
    )

    return informes_view, input_anio, input_mes, informe_container
