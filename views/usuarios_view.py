# views/usuarios_view.py
import flet as ft
class ContenedorUsuario:
    def __init__(self, controller, page, user_id):
        self.controller = controller
        self.page = page
        self.user_id = user_id

        # Creamos un contenedor (o Column) interno para evitar usar `content` del main
        self.layout = ft.Column()

    def mostrar_usuario(self):
        usuario = self.controller.get_user_by_id(self.user_id)
        usuario_info = ft.Column(
            [
                ft.Text("Información del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Text(f"Nombre: {usuario.nombre}"),
                ft.Text(f"Apellidos: {usuario.apellidos}"),
                ft.Text(f"Edad: {usuario.edad}"),
                ft.Text(f"Identificación: {usuario.num_identificacion}"),
                ft.Text(f"Correo: {usuario.correo}"),
                ft.Text(f"Teléfono: {usuario.telefono}"),
                ft.Text(f"Estado: {usuario.estado}"),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        # Limpiamos y agregamos a nuestro layout interno
        self.layout.controls.clear()
        self.layout.controls.append(usuario_info)
        # Si tuvieras que actualizar la página completa:
        self.page.update()

    def get_contenedor(self):
        """Retorna el contenedor principal (layout) de esta vista."""
        # Mostramos la info de entrada (o podrías llamarlo manualmente desde fuera)
        self.mostrar_usuario()
        return self.layout
class ContenedorUsuarioAdmin:
    def __init__(self, controller, page):
        self.controller = controller
        self.page = page

        # Creamos layout interno
        self.layout = ft.Column()

    def mostrar_inicial(self):
        vista_inicial = ft.Column(
            [
                ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Usuarios Inscritos",
                            on_click=lambda e: self.mostrar_usuarios("inscrito")
                        ),
                        ft.ElevatedButton(
                            "Usuarios Matriculados",
                            on_click=lambda e: self.mostrar_usuarios("matriculado")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=10
        )
        self.layout.controls.clear()
        self.layout.controls.append(vista_inicial)
        self.page.update()

        

    def mostrar_formulario_edicion(self, usuario):
        """
        Muestra un formulario para editar los datos de un usuario.
        """
        self.layout.controls.clear()
        
        nuevo_nombre = ft.TextField(label="Nuevo Nombre", value=usuario.nombre)
        nuevo_apellido = ft.TextField(label="Nuevo Apellido", value=usuario.apellidos)
        nuevo_telefono = ft.TextField(label="Nuevo Teléfono", value=usuario.telefono)
        nuevo_correo = ft.TextField(label="Nuevo Correo", value=usuario.correo)
        nueva_identificacion = ft.TextField(label="Nueva Identificación", value=usuario.num_identificacion)

        nuevo_estado = ft.Dropdown(
            label="Nuevo Estado",
            options=[
                ft.dropdown.Option("matriculado"),
                ft.dropdown.Option("pendiente"),
                ft.dropdown.Option("expulsado")
            ],
            value=usuario.estado
        )

        btn_guardar = ft.ElevatedButton(
            "Guardar Cambios",
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=lambda e: self.controller.editar_usuario(
                usuario.id, 
                nuevo_nombre.value, 
                nuevo_apellido.value, 
                nuevo_estado.value, 
                nuevo_telefono.value, 
                nuevo_correo.value,
                nueva_identificacion.value,
                callback=lambda: self.mostrar_usuarios("inscrito")  # Redirige después de editar
            )
        )


        btn_cancelar = ft.ElevatedButton(
            "Cancelar",
            on_click=lambda e: self.mostrar_info_usuario(usuario)
        )

        self.layout.controls.append(ft.Column([nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_correo, nueva_identificacion, nuevo_estado, btn_guardar, btn_cancelar]))
        self.page.update()

    def confirmar_eliminacion(self, usuario):
        """
        Muestra un cuadro de diálogo de confirmación antes de eliminar un usuario.
        """
        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar a {usuario.nombre}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.dialog.open == False),
                ft.TextButton(
                    "Eliminar",
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    on_click=lambda e: self.controller.eliminar_usuario(usuario.id)
                )
            ]  
        )  


        
        self.page.dialog = dialogo
        self.page.dialog.open = True
        self.page.update()


    def mostrar_usuarios(self, estado="inscrito"):
        usuarios_filtrados = self.controller.filtrar_usuarios(estado)
        usuarios_list = [
            ft.ListTile(
                title=ft.Text(f"{usuario.nombre} {usuario.apellidos}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Estado: {usuario.estado}"),
                leading=ft.Icon(ft.icons.PERSON),
                on_click=lambda e, u=usuario: self.mostrar_info_usuario(u)
            )
            for usuario in usuarios_filtrados
        ]
        vista_usuarios = ft.ListView(
            [
                ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                *usuarios_list,
            ],
            spacing=10,
            expand=True,
        )
        self.layout.controls.clear()
        self.layout.controls.append(vista_usuarios)
        self.page.update()

    def mostrar_info_usuario(self, usuario):
        usuario_info = ft.Column(
            [
                ft.Text("Información del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Text(f"Nombre: {usuario.nombre}"),
                ft.Text(f"Apellidos: {usuario.apellidos}"),
                ft.Text(f"Edad: {usuario.edad}"),
                ft.Text(f"Identificación: {usuario.num_identificacion}"),
                ft.Text(f"Correo: {usuario.correo}"),
                ft.Text(f"Teléfono: {usuario.telefono}"),
                ft.Text(f"Estado: {usuario.estado}"),

                #Botón para regresar 
                ft.ElevatedButton(
                    "Regresar",
                    on_click=lambda e: self.mostrar_usuarios("inscrito")
                ),

                # Botón para Editar
                ft.ElevatedButton(
                    "Editar",
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    on_click=lambda e: self.mostrar_formulario_edicion(usuario)
                ),

                # Botón para Eliminar
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    on_click=lambda e: self.confirmar_eliminacion(usuario)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        self.layout.controls.clear()
        self.layout.controls.append(usuario_info)
        self.page.update()

    def get_contenedor(self):
        """Retorna el contenedor principal (layout) de esta vista."""
        # Por defecto, cuando se llama, muestra la vista inicial
        self.mostrar_inicial()
        return self.layout
