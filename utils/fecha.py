# fecha.py
def formatear_fecha(fecha):
    """
    Formatea la fecha para asegurarse de que el día y el mes son de dos dígitos.
    Retorna una tupla (fecha_formateada, error_message).
    """
    try:
        partes = fecha.split('-')
        if len(partes) == 3:
            año, mes, dia = partes
            mes = f"{int(mes):02}"  # Asegura que el mes tenga dos dígitos
            dia = f"{int(dia):02}"  # Asegura que el día tenga dos dígitos
            fecha_formateada = f"{año}-{mes}-{dia}"
            return fecha_formateada, None
        else:
            return None, "Formato de fecha incorrecto. Use YYYY-MM-DD"
    except ValueError:
        return None, "Fecha inválida. Asegúrese de que el año, mes y día sean números."
