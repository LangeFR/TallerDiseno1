# views/usuarios_view.py
import flet as ft

class ContenedorUsuario:
    def __init__(self, controller, page, content, usuario_id):
        self.controller = controller
        self.page = page
        self.content = content
        self.usuario_id = usuario_id

    def mostrar_usuario(self):
        usuario = self.controller.get_user_by_id(self.usuario_id)
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
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        self.content.controls.clear()
        self.content.controls.append(usuario_info)
        self.page.update()


class ContenedorUsuarioAdmin:
    def __init__(self, controller, page, content):
        self.controller = controller
        self.page = page
        self.content = content

    def mostrar_inicial(self):
        # Vista inicial con los dos botones para filtrar usuarios inscritos o matriculados
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
        self.content.controls.clear()
        self.content.controls.append(vista_inicial)
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
        self.content.controls.clear()
        self.content.controls.append(vista_usuarios)
        self.page.update()

    def mostrar_info_usuario(self, usuario):
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
                ft.ElevatedButton(
                    "Regresar",
                    on_click=lambda e: self.mostrar_usuarios("inscrito")
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        self.content.controls.clear()
        self.content.controls.append(usuario_info)
        self.page.update()
