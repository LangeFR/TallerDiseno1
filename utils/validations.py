import re
import flet as ft

# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

# Expresión regular para validar que solo se permiten letras y espacios
ALPHABETIC_REGEX = r'^[A-Za-záéíóúÁÉÍÓÚñÑ0-9 ]+$'

def validar_identificacion(e: ft.ControlEvent):
    """Valida que el campo de identificación contenga solo números y no más de 10 dígitos."""
    if not e.value.isdigit() or len(e.value) < 8 or len(e.value) > 10:
        e.error_text = "La identificación debe ser numérica y tener máximo 10 dígitos."
        e.update()
        return False
    e.error_text = None
    e.update()
    return True

def validar_email(e: ft.ControlEvent):
    """Valida que el campo de correo electrónico tenga un formato válido."""
    if not re.match(EMAIL_REGEX, e.value):
        e.error_text = "Ingrese un correo válido."
        e.update()
        return False
    e.error_text = None
    e.update()
    return True

def validar_apellidos(e: ft.ControlEvent):
    """Valida que el campo de apellidos no contenga caracteres especiales."""
    if not re.match(ALPHABETIC_REGEX, e.value):
        e.error_text = "Los apellidos no pueden contener carácteres especiales."
        e.update()
        return False
    e.error_text = None
    e.update()
    return True

def validar_nombre(e: ft.ControlEvent):
    """Valida que el campo de nombre no contenga caracteres especiales."""
    if not re.match(ALPHABETIC_REGEX, e.value):
        e.error_text = "El nombre no puede contener carácteres especiales."
        e.update()
        return False
    e.error_text = None
    e.update()
    return True

def validar_telefono(e: ft.ControlEvent):
    """Valida que el número de celular tenga entre 8 y 12 dígitos y solo contenga números."""
    if not e.value.isdigit() or len(e.value) < 8 or len(e.value) > 12:
        e.error_text = "El número de celular debe tener entre 8 y 12 dígitos y solo contener números."
        e.update()
        return False
    e.error_text = None
    e.update()
    return True

def validar_edad(edad):
    """Valida que la edad esté en un rango aceptable (por ejemplo, entre 0 y 116 años)."""
    if edad < 0 or edad > 116:
        return False
    return True



def validar_fecha(fecha_input):
    """Valida que la fecha ingresada tenga un formato correcto 'YYYY-MM-DD' y que el mes y día sean válidos."""
    fecha = fecha_input.value
    print(fecha)
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
    """Valida que el día sea adecuado para el mes dado, asumiendo febrero con 28 días."""
    dias_por_mes = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    return 1 <= dia <= dias_por_mes.get(mes, 31)  # Devuelve 31 por defecto si el mes no es válido
