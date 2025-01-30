# tallerdiseno1/utils/validations.py

import re
import flet as ft

# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validar_identificacion(e: ft.ControlEvent):
    """
    Valida que el campo de identificación contenga solo números.
    
    Args:
        e (ft.ControlEvent): Evento de cambio en el control.
    """
    if not e.control.value.isdigit():
        e.control.error_text = "Solo se permiten números."
        # Remueve cualquier carácter no numérico
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
    else:
        e.control.error_text = None
    e.control.update()

def validar_email(e: ft.ControlEvent):
    """
    Valida que el campo de correo electrónico tenga un formato válido.
    
    Args:
        e (ft.ControlEvent): Evento de cambio en el control.
    """
    if not re.match(EMAIL_REGEX, e.control.value):
        e.control.error_text = "Ingrese un correo válido."
    else:
        e.control.error_text = None
    e.control.update()

def validar_apellidos(e: ft.ControlEvent):
    """
    Valida que el campo de apellidos no esté vacío.
    
    Args:
        e (ft.ControlEvent): Evento de cambio en el control.
    """
    if not e.control.value.strip():
        e.control.error_text = "Los apellidos son requeridos."
    else:
        e.control.error_text = None
    e.control.update()
