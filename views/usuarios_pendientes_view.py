#Obtener usuario pendiente
def mostrar_lista_usuarios_pendientes():
    usuarios_pendientes = ClubController.obtener_usuarios_pendientes()
    print(json.dumps(usuarios_pendientes, indent=4))


    usuarios_view.controls.clear()

    for usuario in usuarios_pendientes:
        usuarios_view.controls.append(
            ft.Row([
                ft.Text(f"{usuario['nombre']} - {usuario['correo']}"),
                ft.ElevatedButton(
                    "Rellenar datos",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda e, u=usuario: (
                        llenar_campos_inscripcion(
                            u, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field
                        ),  # Llenar los campos de inscripción
                        destination_change(ft.ControlEvent(selected_index=0))  # Cambiar a la pestaña de inscripción
                    )
                )
            ])
        )

    page.update()


def llenar_campos_inscripcion(usuario, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field):
        """
        Llena los campos de inscripción con los datos del usuario seleccionado.
        """
        # Llenar los campos con la información del usuario
        nombre_field.value = usuario.get("nombre", "")
        apellidos_field.value = usuario.get("apellidos", "")
        edad_field.value = str(usuario.get("edad", ""))
        id_field.value = usuario.get("num_identificacion", "")
        correo_field.value = usuario.get("correo", "")
        telefono_field.value = usuario.get("telefono", "")
    
        # Actualizar los campos para reflejar los cambios en la interfaz
        nombre_field.update()
        apellidos_field.update()
        edad_field.update()
        id_field.update()
        correo_field.update()
        telefono_field.update()
    
        # Cambiar a la vista de inscripción automáticamente
        destination_change(ft.ControlEvent(selected_index=0))  # 0 es la pestaña de inscripción
    
        # Actualizar la página
        page.update()
