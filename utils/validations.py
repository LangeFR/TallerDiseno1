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

def validar_fecha(fecha_input):
    """
    Valida que la fecha ingresada tenga un formato correcto 'YYYY-MM-DD' y que el mes y día sean válidos.
    
    Args:
        fecha_input (ft.TextField): Campo de entrada de la fecha.
    """
    fecha = fecha_input.value
    try:
        partes = fecha.split('-')
        if len(partes) != 3:
            raise ValueError("Formato debe ser YYYY-MM-DD.")
        año, mes, dia = map(int, partes)
        if not (1 <= mes <= 12):
            raise ValueError("Mes debe estar entre 1 y 12.")
        if not es_dia_valido(dia, mes):
            raise ValueError("Día no válido para el mes.")
        fecha_input.error_text = None
    except ValueError as ve:
        fecha_input.error_text = str(ve)
    fecha_input.update()


def es_dia_valido(dia, mes):
    """
    Valida que el día sea adecuado para el mes dado, asumiendo febrero con 28 días.
    
    Args:
        dia (int): Día a validar.
        mes (int): Mes a validar.
    
    Returns:
        bool: True si el día es válido para el mes, False de lo contrario.
    """
    # Diccionario con los días máximos por mes
    dias_por_mes = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    return 1 <= dia <= dias_por_mes.get(mes, 31)  # Devuelve 31 por defecto si el mes no es válido

