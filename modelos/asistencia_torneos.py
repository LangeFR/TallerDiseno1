# modelos/asistencia_torneos.py

from dataclasses import dataclass
import json
import os

@dataclass
class Asistencia_Torneo:
    id: int
    usuario_id: int
    torneo_id: int
    puesto: int

    ARCHIVO = "base_de_datos/asistencia_torneos.json"

    @staticmethod
    def nuevo_id():
        """
        Genera un nuevo ID único para una asistencia.
        """
        try:
            with open(Asistencia_Torneo.ARCHIVO, "r", encoding="utf-8") as archivo:
                asistencias = json.load(archivo)
                if asistencias:
                    return max(asistencia["id"] for asistencia in asistencias) + 1
                else:
                    return 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        """
        Guarda la asistencia actual en el archivo JSON.
        """
        try:
            with open(Asistencia_Torneo.ARCHIVO, "r", encoding="utf-8") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        asistencias.append(self.to_dict())
        with open(Asistencia_Torneo.ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(asistencias, archivo, indent=4, ensure_ascii=False)

    @staticmethod
    def crear_asistencia(torneo_id, usuario_id, puesto):
        """
        Crea y guarda una nueva asistencia para un torneo.
        """
        nueva_asistencia = Asistencia_Torneo(
            id=Asistencia_Torneo.nuevo_id(),
            usuario_id=usuario_id,
            torneo_id=torneo_id,
            puesto=puesto
        )
        nueva_asistencia.guardar()

    @classmethod
    def obtener_asistencias_por_torneo(cls, torneo_id):
        """
        Obtiene todas las asistencias para un torneo específico.

        Parámetros:
            torneo_id (int): El ID del torneo para el cual se desean obtener las asistencias.

        Retorna:
            List[Asistencia_Torneo]: Una lista de instancias de Asistencia_Torneo filtradas por torneo_id.
        """
        if not os.path.exists(cls.ARCHIVO):
            print(f"⚠️ El archivo {cls.ARCHIVO} no existe.")
            return []

        try:
            with open(cls.ARCHIVO, "r", encoding="utf-8") as archivo:
                asistencias = json.load(archivo)
        except json.JSONDecodeError:
            print(f"⚠️ Error al decodificar JSON en {cls.ARCHIVO}.")
            return []

        # Filtrar asistencias por torneo_id
        asistencias_filtradas = [a for a in asistencias if a.get("torneo_id") == torneo_id]

        # Convertir dicts a instancias de Asistencia_Torneo
        return [cls(**a) for a in asistencias_filtradas]

    @classmethod
    def actualizar_puesto(cls, torneo_id, usuario_id, nuevo_puesto):
        """
        Actualiza el puesto de un usuario en un torneo específico.
        """
        try:
            with open(cls.ARCHIVO, "r", encoding="utf-8") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        asistencia_actualizada = False

        for asistencia in asistencias:
            if asistencia['torneo_id'] == torneo_id and asistencia['usuario_id'] == usuario_id:
                asistencia['puesto'] = nuevo_puesto
                asistencia_actualizada = True
                break

        if asistencia_actualizada:
            with open(cls.ARCHIVO, "w", encoding="utf-8") as archivo:
                json.dump(asistencias, archivo, indent=4, ensure_ascii=False)
        else:
            raise ValueError("Asistencia no encontrada para actualizar.")

    def to_dict(self):
        """
        Convierte la instancia de Asistencia_Torneo a un diccionario.

        Retorna:
            dict: Representación en diccionario de la asistencia.
        """
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "torneo_id": self.torneo_id,
            "puesto": self.puesto
        }
